# Mali Tablo Fetch ve Dönüşüm Planı

## Mevcut Durum (PostgreSQL)

| Tablo | Satır | Detay |
|-------|-------|-------|
| companies | 610 | 610 aktif şirket |
| financial_statements_raw | 332,838 | 579 ticker, 4 dönem (2025Q2-2026Q1) |
| company_ratios | 22,988 | Hesaplanmış rasyolar |
| item_code_mappings | 130 | Kod eşleme |
| company_metrics | 609 | Piyasa verileri |
| company_scores | 1,110 | Skorlar (opsiyonel) |
| fetch_logs | ~3,000+ | Fetch geçmişi |

## Strateji: Export + Incremental Fetch

**Öneri:** Eski PostgreSQL'den export yapıp D1'e yüklemek (hızlı seed) + cron ile incremental fetch.

---

## Aşama 1: PostgreSQL → D1 Export

### 1.1 Export Edilecek Tablolar (öncelik sırası)

1. **companies** (610 row) → `seed_companies.sql` (zaten hazır, güncellenebilir)
2. **financial_statements_raw** (332K row) → `seed_statements.sql` (en önemli)
3. **item_code_mappings** (130 row) → `seed_item_codes.sql` (zaten hazır)
4. **company_metrics** (609 row) → `seed_metrics.sql`
5. **company_ratios** (22,988 row) → `seed_ratios.sql` (opsiyonel, tekrar hesaplanabilir)
6. **company_scores** (1,110 row) → `seed_scores.sql` (opsiyonel, phase 2)

### 1.2 Export Script

Python script ile PostgreSQL → D1 SQL formatına çevirme:
- Her tablo için `SELECT *` + `INSERT OR REPLACE` oluştur
- value_try alanlarını REAL/NUMERIC forma cast et
- Period anahtarlarını string olarak koru
- Batch boyutu: 500 row/INSERT (D1 limiti)
- Çıktı: `.sql` dosyaları

### 1.3 Tahmini D1 Boyutu

- financial_statements_raw: 332K satır × ~80 byte ≈ 26 MB (D1 limiti 100MB/gratis)
- Diğer tablolar: ~5 MB
- **Toplam: ~31 MB** ✅ D1 ücretsiz limiti içinde

---

## Aşama 2: Mali Tablo Fetch Sistemi

### 2.1 Mimari

```
┌─────────────────────────────────────────────────────┐
│  Cron Trigger (temel-fetcher)                        │
│  ─────────────────────────────                       │
│  Daily 04:00 UTC (07:00 TR)  → KAP window companies │
│  Sunday 01:00 UTC (04:00 TR) → ALL active companies │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  _fetch_single_company(ticker)                       │
│  ─────────────────────────────                       │
│  1. Rate limit (20 req/min, 3s delay)               │
│  2. MaliTablo GET (4 periods)                        │
│  3. MD5 checksum hesapla                             │
│  4. FetchLog'dan son checksum'u oku                  │
│  5. if checksum != last_checksum:                    │
│       → D1 upsert                                    │
│       → Trigger ratio calculation                    │
│  6. FetchLog entry oluştur                           │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  D1 Database                                         │
│  ───────────                                         │
│  financial_statements_raw (upsert)                   │
│  company_ratios (calculate + insert)                 │
│  fetch_logs (always insert)                          │
└─────────────────────────────────────────────────────┘
```

### 2.2 Hangi Şirketler Ne Zaman Çekilecek?

| Zaman | Seçim Kriteri | Amaç |
|-------|--------------|------|
| **Günlük 07:00 TR** | KAP bildirim dönemindeki aylar: Oca-Şub-Mar (Q4), Nis-May (Q1), Tem-Ağu (Q2), Eki-Kas (Q3) | Yoğun dönemde güncel veri |
| **Günlük 07:00 TR** | Diğer aylar (Haz, Eyl, Ara): **hiçbir şirket** çekilmez | Rapor dönemi dışı |
| **Pazar 04:00 TR** | **Tüm** aktif şirketler | Haftalık safety net + diff check |
| **Manuel (POST)** | Belirtilen ticker'lar veya "ALL" | Acil durum / test |

### 2.3 Hangi Dönemler Çekilecek?

Her zaman **4 ardışık çeyrek** (son 4 quarter):

```
bugün Temmuz 2026 ise:
  → (2026, Q1), (2025, Q4), (2025, Q3), (2025, Q2)
  → period_key: 2026Q1
```

Reporting lag hesabı:
| Ay | Son Çeyrek |
|----|-----------|
| Oca-May | Önceki yıl Q4 |
| Haz-Ağu | Cari yıl Q1 |
| Eyl-Kas | Cari yıl Q2 |
| Ara | Cari yıl Q3 |

### 2.4 Checksum Diff Mekanizması (Değişiklik Tespiti)

```python
1. API'den gelen JSON'ın MD5'ini al:
   checksum = md5(json.dumps(response, sort_keys=True))
   
2. FetchLog'dan son checksum'u oku (ticker + period_key):
   SELECT checksum_md5 FROM fetch_logs 
   WHERE ticker=? AND period_key=?
   ORDER BY fetched_at DESC LIMIT 1

3. if checksum != last_checksum veya hiç fetch yok:
   → Veri değişmiş: D1'e yaz + rasyo hesapla
   
4. Her durumda FetchLog'a kaydet:
   → is_new_data = (checksum != last_checksum)
```

### 2.5 Rate Limiting

| Parametre | Değer |
|-----------|-------|
| İstek/dakika | 20 |
| İstekler arası bekleme | 3.0 saniye |
| Batch boyutu | 10 şirket |
| Batch arası mola | 120 saniye |
| Priority mode delay | 0.5 saniye (manuel fetch) |

**Toplam süre hesaplama:**
- 610 şirket × 3s = 1,830 saniye ≈ 30 dakika
- 61 batch × 120s mola = 7,320 saniye ≈ 122 dakika
- **Toplam: ~2.5 saat** (tam scan)
- Günlük window scan: birkaç şirket → çok daha hızlı

### 2.6 MaliTabloShortTable

ShortTable endpoint'i (`MaliTabloShortTable?companyCode=THYAO&exchange=TRY&year1=2025&period1=12`):
- Sadece **3 kalem** döndürür:
  - `2O` = Özkaynaklar (Shareholders' Equity)
  - `2OA` = Ödenmiş Sermaye (Paid-in Capital)
  - `3Z` = Net Dönem Karı/Zararı (Net Income)
- Sadece **tek dönem** (`value1`), çoklu period parametresi işe yaramaz
- **Kullanım önerisi:**
  - Ayrı bir tabloda (`company_financial_summary`) hafif ve hızlı veri olarak tut
  - Frontend şirket özet kartları için kullan
  - Hesaplanan rasyolarımızı cross-check/doğrulama amaçlı kullan
  - Her gün tüm şirketler için fetch et (çok hafif, 3 item × 610 co ≈ 1,830 row)
  - D1'de `UNIQUE(ticker, period_key)` ile upsert

### 2.7 Financial Group Ataması

| Sektör (sector_main) | Financial Group |
|---------------------|----------------|
| Bankacılık & Finans | UFRS_K |
| Sigorta | UFRS_S |
| Fin.Kiralama ve Faktoring | UFRS_F |
| GYO | UFRS_K |
| Diğer tüm sektörler | XI_29 |

> **Not:** Temelozet.xlsx'deki sektör adları ile `sector_main` eşlemesi yapılacak.

---

## Aşama 3: Cron Worker (temel-fetcher)

### 3.1 Worker Yapısı

```
temel/fetcher/
├── wrangler.toml        # D1 + KV binding + cron
├── src/
│   ├── __init__.py
│   └── index.py         # Cron handler + fetch logic
└── SETUP.md
```

### 3.2 wrangler.toml Cron

```toml
[triggers]
crons = ["0 4 * * *", "0 1 * * 0"]
# 04:00 UTC = 07:00 TR (daily)
# 01:00 UTC = 04:00 TR (Sunday)
```

### 3.3 Çalışma Akışı

```
on_fetch(request, env):
  if cron trigger:
    1. Şirket listesini al (window veya all)
    2. Her batch için:
       a. Rate limit
       b. MaliTablo fetch
       c. Checksum comparison
       d. if new: D1 upsert + rasyo tetikle
       e. FetchLog kaydı
    3. ShortTable fetch (daily)
    4. Sonuçları döndür
```

---

## Aşama 4: Rasyo Hesaplama Tetikleme

### 4.1 Ne Zaman Tetiklenecek?

- Sadece `is_new_data == True` olduğunda
- `asyncio.create_task()` ile async fire-and-forget
- Aynı worker içinde D1'e yaz

### 4.2 Hangi Rasyolar?

Sektöre göre değişir (mevcut RatioCalculator mantığı):
- **XI_29**: cari oran, asit-test, borç/özkaynak, brüt marj, net marj, ROE, ROA, F/K, PD/DD, FD/FAVÖK, aktif devir
- **UFRS_K**: net faiz marjı, kredi/mevduat, NPL, maliyet/gelir + ROE, ROA
- **UFRS_S**: hasar oranı, gider oranı, birleşik oran + ROE, ROA, F/K, PD/DD
- **GYO**: NAD iskontosu, kira getirisi + temel rasyolar

### 4.3 TTM Hesaplama (Trailing 12 Months)

- **XI_29**: Son 4 çeyrek toplamı
- **UFRS_K/UFRS_S**: Yıllık (period=12) kümülatif veri direkt

---

## Aşama 5: ShortTable Değerlendirme

**Neden kullanmalıyız:**

| Artılar | Eksiler |
|---------|---------|
| Çok hızlı (3 item, single period) | Sadece 3 kalem (yetersiz) |
| Hafif payload (~200 byte/response) | Trend göstermez (tek period) |
| Önceden hesaplanmış (İş Yatırım) | Hesaplama metodolojisi kapalı |
| Cross-check için ideal | Rasyo hesaplamada kullanılamaz |

**Karar: Ekle, ama sadece tamamlayıcı olarak**

- Yeni tablo: `company_financial_summary`
- Schema: `(ticker, period_key, equity REAL, paid_capital REAL, net_income REAL, fetched_at TEXT)`
- Günlük cron'da tüm şirketler için çek
- Frontend özet kartı + doğrulama amaçlı
- Rasyo hesaplama için **kullanma** (yetersiz)

---

## Aşama 6: Uygulama Sırası

### Adım 1: Export Script
- Python script yaz: PostgreSQL → D1 SQL dump
- Tablolar: financial_statements_raw (332K) + company_metrics (609)
- Batch INSERT OR REPLACE ile

### Adım 2: D1'e Yükle
- `wrangler d1 execute temel-db --file=seed_statements.sql`
- `wrangler d1 execute temel-db --file=seed_metrics.sql`

### Adım 3: Fetcher Worker'ı Güncelle
- MaliTablo fetch + checksum diff + D1 upsert
- Rate limiting + batch processing
- ShortTable fetch (ek olarak)

### Adım 4: Rasyo Hesaplama Worker'ı
- Mevcut `temel-fetcher`'a entegre
- Fire-and-forget pattern

### Adım 5: KV Cache Invalidation
- Yeni veri geldiğinde ilgili KV key'leri temizle:
  - `company:{ticker}`
  - `ratios:{ticker}:{period}`
  - `ai_context:{ticker}:*`

---

## Tahmini Timeline

| Adım | Süre | Detay |
|------|------|-------|
| Export script yazımı | 1 saat | PostgreSQL'den SQL dump |
| D1'e yükleme | 5 dakika | wrangler d1 execute |
| Fetcher worker güncelleme | 2 saat | Checksum + diff + rate limit |
| Rasyo tetikleme entegrasyonu | 1 saat | Post-fetch calculation |
| ShortTable entegrasyonu | 30 dakika | Yeni tablo + endpoint |
| Test + Deploy | 1 saat | wrangler dev + wrangler deploy |
| **Toplam** | **~6 saat** | |

---

## Ek: Olası Sorunlar ve Çözümler

| Sorun | Çözüm |
|-------|-------|
| D1 100MB limiti aşılabilir | Sadece son 8 period tut, eski veriyi temizle |
| API rate limit | 20 req/dk, 3s delay ile korunuyor |
| Checksum her zaman aynı | Zaten redundant insert yapılmıyor |
| Şirket finansal grup değişikliği | Sektör bazlı atama, manuel override desteği |
| Yeni şirket eklenmesi | Haftalık scan'de otomatik keşif + temelozet.xlsx güncelleme |
| D1 sırasında timeout (30s) | Batch boyutunu küçült, chunked insert kullan |
