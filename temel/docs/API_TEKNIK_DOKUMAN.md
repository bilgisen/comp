# Temel Analiz API — Teknik Doküman

## 1. Mimari Genel Bakış

```
┌─────────────────────────────────────────────────────┐
│                Cloudflare Workers (Python)           │
│                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌───────────┐│
│  │ ratio-worker │   │ score-worker │   │price-worker││
│  │  (v2 ratios) │   │ (benchmarks  │   │ (fiyat    ││
│  │              │   │  + scoring)  │   │  çekme)   ││
│  └──────┬───────┘   └──────┬───────┘   └─────┬─────┘│
│         │                  │                  │       │
│         └────────┬─────────┘──────────────────┘       │
│                  │                                    │
│         ┌────────▼────────┐                           │
│         │  Cloudflare D1  │                           │
│         │  (SQLite)       │                           │
│         │  temel-db       │                           │
│         └─────────────────┘                           │
│                                                      │
│  ┌──────────────────┐                                │
│  │  KV (TEMEL_CACHE) │  ← ratio-worker cursor        │
│  └──────────────────┘                                │
└─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────┐   ┌───────────────────┐
│  Hono API        │   │  TanStack Ön Yüz  │
│  (Orchestrator)  │──▶│  (React Router 7) │
│  /api/v1/...     │   │  BIST Analiz      │
└──────────────────┘   └───────────────────┘
```

### 1.1 Worker'lar

| Worker | Worker adı | URL | Dil |
|--------|-----------|-----|-----|
| Ratio | `temel-ratio-worker` | `https://temel-ratio-worker.paraanaliz.workers.dev` | Python (Pyodide) |
| Score | `temel-score-worker` | `https://temel-score-worker.paraanaliz.workers.dev` | Python (Pyodide) |
| Price | `temel-price-worker` | Yok (yedekte) | Python |
| Fetcher | `temel-fetcher` | Yok (seed scripts) | Python |

### 1.2 Altyapı

- **Cloudflare D1** — Worker'larla aynı bölgede SQLite, tek veritabanı (`temel-db`)
- **Cloudflare KV** — ratio-worker cursor state tutar (`TEMEL_CACHE`)
- **Python Workers** — `compatibility_flags = ["python_workers"]` ile Pyodide, numpy/scipy yok, tüm istatistik saf Python
- **Cron Triggers** (Dashboard'da manuel):
  - ratio-worker: `0 6 * * 0` (Pazar 06:00 UTC)
  - score-worker: `0 8 * * 0` (Pazar 08:00 UTC)

---

## 2. Veri Akışı

```
İş Yatırım API
     │
     ▼
fetcher/ (seed script, local Python)
     │  JSON çek → financial_statements_raw tablosuna yaz
     │
     ▼
ratio-worker (cron: Pazar 06:00)
     │  raw veriden 13 item_code okur
     │  17 rasyo hesaplar → company_ratios tablosu
     │  Sektör profiline göre hangi rasyolar hesaplanır
     │
     ▼
score-worker (cron: Pazar 08:00)
     │  1. Benchmark hesaplama (sektör/grup/market medyanları)
     │  2. Skor hesaplama (3 pillar, sigmoid, F1-F5 filtreleri)
     │
     ▼
Hono API / TanStack Frontend
     │  score-worker endpoint'lerini tüketir
     │  ranking, score card, comparison, sector pages
```

---

## 3. Veritabanı Şeması (D1 / SQLite)

### 3.1 Ana Tablolar

| Tablo | İçerik | Satır |
|-------|--------|-------|
| `companies` | 614 BIST hissesi, sektör, market_cap | 614 |
| `financial_statements_raw` | Mali tablo item kodları ve değerleri | ~60K |
| `company_ratios` | Hesaplanmış rasyolar (TTM, v2 metodu) | ~7000 |
| `company_metrics` | Fiyat, piyasa değeri, lot bilgisi | 614 |
| `company_financial_summary` | Özet: equity, paid_capital, net_income | ~1800 |
| `isyatirim_ratios` | İş Yatırım referans rasyoları (bootstrapping) | 614 |
| `company_sector_profiles` | Sektör grubu sınıflandırması | 614 |
| `sector_benchmarks` | Medyan, p25, p75 (sektör/grup/market) | 845 |
| `company_scores` | Kompozit skor, 3 pillar, absolute | 578 |
| `company_score_details` | Rasyo bazında skor kırılımı + pillar etiketi | ~3600 |
| `sector_consolidation` | 54 raw sektör → 14 grup mapping | 54 |
| `fetch_logs` | Çekme logları | - |
| `item_code_mappings` | İş Yatırım kod → semantic isim | - |

### 3.2 Kritik Kolonlar

**company_ratios:**
- `ticker, period_key, ratio_code, ratio_value` — unique constraint
- `calculation_method = 'v2'` — güncel metod
- `is_ttm = 1` — trailing twelve months

**sector_benchmarks:**
- `sector_name, benchmark_type('sector'/'group'/'market'), ratio_code, period_key` — unique
- `median_ew, median_mc, p25, p75, n_peers, reliability`

**company_scores:**
- `ticker, period_key='TTM', score_version='v1'` — unique
- `composite_score, pillar_finansal_saglik, pillar_karlilik_buyume, pillar_degerleme`
- `benchmark_source('sector'/'group'/'market'), n_peers, data_completeness`
- `absolute_score, absolute_label`
- `upper_sector_name, upper_benchmark_type`

**company_score_details:**
- `score_id → company_scores.id` FK
- `ratio_code, ratio_value, peer_median, raw_score, final_score`
- `pillar TEXT` — hangi pilde kullanıldığı

### 3.3 Sektör Konsolidasyonu

54 İş Yatırım raw sektörü → 14 consolidated grup:

| Consolidated Key | Örnek Sektörler |
|----------------|-----------------|
| `Bankacilik_Finans` | Bankacılık, Yatırım Ort., Aracı Kurum, Fin.Kiralama, Varlık Yönetim |
| `Sigortacilik` | Sigorta |
| `GYO` | GYO |
| `Enerji_Altyapi` | Elektrik Üretim, Doğalgaz Dağ., Petrol |
| `Sanayi_Metal_Kimya` | Demir-Çelik, Kimyasal, Çimento, Seramik, Boya, Makine |
| `Insaat_Yapi` | İnşaat Malz., İnşaat-Taahhüt |
| `Otomotiv_Savunma_Makine` | Otomotiv, Savunma, Lastik |
| `Teknoloji_Iletisim` | Teknoloji, İletişim, Bilgisayar |
| `Gida_Icecek_Tarim` | Gıda, İçecek, Tarım Kimyasalları |
| `Tuketim_Perakende_Tekstil` | Tekstil, Perakende, Kağıt, Mobilya, Deri |
| `Ulastirma_Lojistik` | Ulaştırma, Havayolları |
| `Turizm_Medya_Eglence` | Turizm, Medya, Eğlence |
| `Holdingler` | Holdingler, Madencilik |
| `Diğer` / `Spor` | Consolidated = null, market benchmark kullanır |

---

## 4. Ratio Worker (`temel-ratio-worker`)

### 4.1 Endpoints

| Method | Path | Açıklama |
|--------|------|----------|
| GET/POST | `/compute` | 15 şirketlik batch hesapla (cursor KV'de) |
| GET | `/compute?ticker=GARAN` | Tek hisse hesapla |
| GET | `/validate` | company_ratios vs isyatirim_ratios karşılaştır |
| GET | `/ticker/GARAN` | Bir hisse için tüm veri |

### 4.2 Rasyo Hesaplama

13 İş Yatırım item_code'undan 17 rasyo hesaplanır:

| item_code | Açıklama | Kullanıldığı Rasyo |
|-----------|----------|-------------------|
| `3Z` | Net Kar (TTM) | pe, roe, roa, net_margin, eps, profit_growth |
| `2O` | Özkaynak | roe, pb, book_per_share, debt_equity |
| `3C` | Hasılat (TTM) | ev_sales, net_margin, gross_margin |
| `3CA` | COGS/SMM (TTM) | inventory_turnover (abs ile) |
| `3DF` | Faaliyet Karı/EBIT (TTM) | interest_coverage |
| `1BL` | Toplam Aktifler | roa |
| `1AI` | Dönen Varlıklar | current_ratio, cash_ratio |
| `2A` | Kısa Vadeli Yük. | current_ratio, cash_ratio |
| `1AA` | Nakit | cash_ratio |
| `1AF` | Stoklar | inventory_turnover |
| `1AC` | Ticari Alacaklar | (yedek) |
| `2AA` | Kısa Vadeli Borç | debt_equity |
| `2BA` | Uzun Vadeli Borç | debt_equity |
| `3D` | Brüt Kar (TTM) | gross_margin |
| `3HC` | Finansman Gideri (TTM) | interest_coverage (abs ile) |

### 4.3 Sektör Grubuna Göre Rasyo Listesi

```python
SECTOR_RATIOS = {
    "industrial":   [pe, pb, ev_ebitda, ev_sales, roe, roa, net_margin, gross_margin, eps, book_per_share, profit_growth, current_ratio, cash_ratio, debt_equity, inventory_turnover, interest_coverage, forward_pe, forward_ev_ebitda, forward_pb],
    "financial":    [pe, pb, roe, roa, net_margin, eps, book_per_share, profit_growth, forward_pe, forward_pb],
    "holding":      [pe, pb, ev_ebitda, ev_sales, roe, roa, net_margin, eps, book_per_share, profit_growth, debt_equity, forward_pe, forward_ev_ebitda, forward_pb],
    "reit":         [pe, pb, roe, net_margin, eps, book_per_share, profit_growth, forward_pe, forward_pb],
    "insurance":    [pe, pb, roe, roa, net_margin, eps, book_per_share, profit_growth, forward_pe, forward_pb],
    "brokerage":    [pe, pb, roe, roa, net_margin, eps, book_per_share, profit_growth],
    "banking":      [pe, pb, roe, roa, net_margin, eps, book_per_share, profit_growth, forward_pe, forward_pb],
}
```

### 4.4 Fallback Mekanizması

- Fiyat (`last_price`) ve shares → `company_metrics` tablosu
- EV/EBITDA, EV/Sales, forward rasyolar → `isyatirim_ratios` referansı
- Net kar/özkaynak → `financial_summary` (ShortTable) yedek
- İş Yatırım referans PE/PB → computed None ise referans kullanılır

### 4.5 Cron'da Çalışma

```python
async def scheduled(self, event):
    # KV cursor'ı sıfırla
    # compute_ratios()'u loop'la cursor 0 olana kadar çağır
    # Her batch = 15 şirket, ~610 şirket = ~41 batch
```

---

## 5. Score Worker (`temel-score-worker`)

### 5.1 Endpoints

| Method | Path | Açıklama |
|--------|------|----------|
| GET/POST | `/scores/compute?cursor=N` | Skor hesapla (20'lik batch) |
| GET/POST | `/benchmarks/compute?cursor=N` | Benchmark hesapla (cursor-based) |
| GET | `/score/{TICKER}` | Hisse skor kartı |
| GET | `/compare/{T1},{T2},{T3}` | 2-5 hisse karşılaştırma |
| GET | `/rankings/sector/{name}` | Sektör sıralaması |
| GET | `/rankings/group/{name}` | Grup sıralaması |
| GET | `/rankings/market` | Pazar sıralaması |
| GET | `/sectors` | Tüm sektörler + consolidated group listesi |
| GET | `/sectors/{name}` | Sektör/grup detayı (benchmark + leaderboard) |
| GET | `/absolute/{TICKER}` | Benchmark bağımsız absolute skor |
| GET | `/seed_consolidation` | sector_consolidation tablosunu doldur |

### 5.2 Benchmark Sistemi (3 Tier)

```
Sektör (n ≥ 5)
  → Grup (consolidated, n ≥ 3, "Diğer"/"Spor" atlar)
    → Pazar (bist_all, tüm 600+ hisse, sadece 4 rasyo: pe/pb/ev_ebitda/ev_sales)
```

Her tier için:
- `median_ew` — eşit ağırlıklı medyan
- `median_mc` — piyasa değeri ağırlıklı medyan
- `p25`, `p75` — çeyreklikler
- `n_peers`, `reliability`
- **F3 ekonomik sınır filtresi** — sektöre özgü min/max bound'lar (ör: banka pe max 25x, teknoloji pe max 200x)
- **Winsorize** %5-%95 — aykırı değer kırpma (n ≥ 5 ise)
- Tüm istatistikler saf Python (numpy yok)

### 5.3 Skorlama Modeli (3 Pillar)

Her sektör grubu için ayrı PILLAR_CONFIG:

```
_finansal_saglik (weight varies)
   ├── current_ratio, cash_ratio, debt_equity, interest_coverage
   └── Banks: roe (tek rasyo)
       GYO: roe + profit_growth
       Teknoloji: current_ratio + cash_ratio + debt_equity

_karlilik_buyume (weight varies)
   ├── roe, roa, net_margin, gross_margin, profit_growth
   └── Banks: roe + net_margin + profit_growth

_degerleme (weight varies)
   ├── pe, pb, ev_ebitda, ev_sales
   └── Banks/Teknoloji/GYO: sadece pe + pb
```

**Puanlama Adımları:**
1. **F1**: Eksik rasyo? → skip
2. **F2**: Ekonomik bound dışı? → skip
3. **F3**: Peer < 3? → benchmark median'ı peer olarak kullan
4. **F4**: Sigmoid skor: `100 / (1 + exp(-steepness * z))` (z-score)
5. **F5**: Reliability dampening: HIGH=1.0, MEDIUM=0.80, LOW=0.55
6. **Pillar ağırlıklandırma** → composite score
7. **Absolute skor** — sabit eşiklerle, benchmark'tan bağımsız

### 5.4 Skor Kartı Çıktısı (`GET /score/GARAN`)

```json
{
  "ticker": "GARAN",
  "company_name": "Garanti Bankası",
  "sector": "Bankacılık",
  "composite_score": 60.77,
  "reliability": "HIGH",
  "pillars": {
    "finansal_saglik": { "score": 68.24, "details": [ ... ] },
    "karlilik_buyume":   { "score": 58.83, "details": [ ... ] },
    "degerleme":         { "score": 52.08, "details": [ ... ] }
  },
  "absolute": { "score": 82.1, "label": "GUCLU" },
  "benchmark": { "source": "sector", "name": "Bankacılık", "n_peers": 16 },
  "ranks": {
    "sector": { "percentile": 82.1, "n_peers": 14 },
    "group":  { "percentile": 79.0, "n_peers": 31 }
  },
  "ratios": { "pe": 1.91, "pb": 1.20, "roe": 0.62, ... }
}
```

### 5.5 Sıralama Çıktısı (`GET /rankings/sector/Bankacılık`)

```json
{
  "scope": "sector", "name": "Bankacılık",
  "total": 14, "limit": 50, "offset": 0,
  "results": [
    { "ticker": "ALBRK", "composite_score": 68.96, "pillar_finansal_saglik": 89.4, "rank": 1 },
    { "ticker": "TSKB",  "composite_score": 61.86, ... , "rank": 2 },
    ...
  ]
}
```

### 5.6 Sektör Detayı (`GET /sectors/GYO`)

```json
{
  "sector": "GYO", "company_count": 58,
  "benchmarks": {
    "pe": { "median_ew": 5.56, "p25": 2.87, "p75": 9.15, "n_peers": 38, "reliability": "HIGH" },
    "pb": { "median_ew": 0.57, "p25": 0.34, "p75": 1.01, "n_peers": 56, ... },
    "roe": { "median_ew": 0.072, ... }
  },
  "sector_score": { "equal_weight": 51.46, "market_cap_weighted": 55.37 },
  "leaderboard": [ ... ]
}
```

### 5.7 Karşılaştırma (`GET /compare/GARAN,AKBNK,ISCTR`)

```json
{
  "tickers": [
    {
      "ticker": "GARAN", "composite_score": 60.77,
      "pillars": { "finansal_saglik": 68.24, "karlilik_buyume": 58.83, "degerleme": 52.08 },
      "absolute": { "score": 82.1, "label": "GUCLU" },
      "key_ratios": { "pe": 1.91, "pb": 1.20, "roe": 0.62, "net_margin": 0.57, "current_ratio": null, "debt_equity": null }
    },
    ...
  ]
}
```

---

## 6. Teknik Detaylar

### 6.1 Pyodide Kısıtlamaları

- **numpy/scipy yok** → tüm istatistik saf Python:
  - `_median()`, `_percentile()`, `_robust_std()` (IQR/1.349)
  - `_winsorize()` (5-95)
  - `_weighted_quantile()` (piyasa değeri ağırlıklı)
  - `_sigmoid_score()` (exp ile manuel)
- **HttpClient yok** → sadece D1 + KV API'ları
- **scheduled handler** → `async def scheduled(self, event)` sınıf metodu
- **sınıf adı**: `Default`, `WorkerEntrypoint`'ten türet

### 6.2 D1 API Pattern'leri

```python
# Tek satır çekme
row = await db.prepare("SELECT * FROM companies WHERE ticker = ?").bind(ticker).first()
# first() → dict or None

# Çoklu satır
rows = await db.prepare("SELECT * FROM companies WHERE is_active = 1").all()
# all() → { results: [...] }

# Insert/Update
r = await db.prepare("INSERT OR REPLACE INTO ... VALUES (?, ?)").bind(v1, v2).run()
# run() → { success: bool, meta: { last_row_id, changes, ... } }

# JSON response
Response.json({"key": value})
```

### 6.3 URL Encoding (Türkçe Karakter)

Sektör isimlerinde Türkçe karakterler var (Bankacılık, İnşaat, Gıda, Çimento...):
- `path = unquote(parsed.path)` ile decode edilmeli
- Aksi halde `Bankac%C4%B1l%C4%B1k` ham string kalır

### 6.4 Önemli Sektör İstisnaları

- **Bankacılık**: `current_ratio`/`debt_equity` hesaplanmaz (bankalar için anlamsız) → finansal_saglik pillar'ı roe kullanır
- **GYO**: `current_ratio` hesaplanmaz → finansal_saglik pillar'ı roe + profit_growth kullanır
- **Sigorta**: `debt_equity` hesaplanmaz → finansal_saglik pillar'ı roe kullanır
- **"Diğer" ve "Spor"**: consolidated = null → benchmark market'e düşer (n<3 ise)
- **Sınırlı rasyo listesi**: financial/banking/reit grupları `ev_ebitda/ev_sales` hesaplamaz, `current_ratio` vs hesaplamaz

---

## 7. Hono API & Frontend Entegrasyonu

### 7.1 Önerilen Hono Route'ları

```typescript
// Proxy — score-worker'a yönlendir
GET  /api/v1/score/:ticker
GET  /api/v1/compare/:tickers
GET  /api/v1/rankings/:scope/:name
GET  /api/v1/sectors
GET  /api/v1/sectors/:name
GET  /api/v1/absolute/:ticker

// Cache — ratio-worker verileri
GET  /api/v1/ratios/:ticker

// Admin — sadece scheduled worker'lar çağırır
POST /api/v1/admin/refresh/ratios   // ratio-worker /compute
POST /api/v1/admin/refresh/scores   // score-worker /benchmarks + scores
```

### 7.2 Yanıt Formatı (Standart)

```typescript
// Success
{ "data": { ... } }

// Error
{ "error": "message", "code": "NOT_FOUND" }

// List
{ "data": [...], "meta": { "total": 578, "page": 1, "limit": 50 } }
```

### 7.3 Önbellekleme Stratejisi

- **Score/skor kartı**: 1 saat CDN cache (sadece haftalık değişir)
- **Rankings/sectors**: 1 saat
- **Sector detail**: 1 saat
- **Absolute**: 1 saat
- **Karşılaştırma**: 5 dk
- **Ratios**: 1 saat

### 7.4 TanStack Frontend Sayfaları

| Route | Component | Veri Kaynağı |
|-------|-----------|-------------|
| `/` | Landing, market overview | `/rankings/market` (ilk 10) |
| `/hisse/:ticker` | Hisse detay, skor kartı | `/score/{ticker}` |
| `/karsilastir?t=GARAN,AKBNK` | Karşılaştırma | `/compare/{tickers}` |
| `/sektorler` | Sektör listesi | `/sectors` |
| `/sektor/:name` | Sektör detayı, leaderboard, benchmark | `/sectors/{name}` |
| `/siralamalar/:scope/:name` | Sıralama tablosu | `/rankings/{scope}/{name}` |

### 7.5 Renk/Skor Etiketleri

| Absolute Label | Renk | Skor Aralığı |
|---------------|------|-------------|
| GÜÇLÜ | Green | ≥ 80 |
| SAĞLIKLI | Light green | ≥ 60 |
| ORTA | Yellow | ≥ 40 |
| ZAYIF | Orange | ≥ 20 |
| KRİTİK | Red | < 20 |

**Reliability**: HIGH, MEDIUM, LOW, INSUFFICIENT (renk kodlaması ile)

---

## 8. Cron Schedule (Dashboard)

Cloudflare Dashboard → Workers & Pages:

| Worker | Cron | İşlem |
|--------|------|-------|
| `temel-ratio-worker` | `0 6 * * 0` | Pazar 06:00 UTC — tüm hisseler için veri çek + rasyo hesapla |
| `temel-score-worker` | `0 8 * * 0` | Pazar 08:00 UTC — benchmark'ları + skorları yeniden hesapla |

Manuel tetikleme:
```bash
curl -X POST https://temel-score-worker.paraanaliz.workers.dev/benchmarks/compute
curl -X POST https://temel-score-worker.paraanaliz.workers.dev/scores/compute?cursor=0
```

---

## 9. Örnek Kullanım

```bash
# Score card
curl https://temel-score-worker.paraanaliz.workers.dev/score/GARAN

# Karşılaştırma
curl https://temel-score-worker.paraanaliz.workers.dev/compare/GARAN,AKBNK,ISCTR

# Sektör sıralaması (URL-encoded Türkçe)
curl https://temel-score-worker.paraanaliz.workers.dev/rankings/sector/Bankac%C4%B1l%C4%B1k

# Grup sıralaması
curl https://temel-score-worker.paraanaliz.workers.dev/rankings/group/Teknoloji_Iletisim

# Pazar sıralaması
curl https://temel-score-worker.paraanaliz.workers.dev/rankings/market

# Sektör listesi
curl https://temel-score-worker.paraanaliz.workers.dev/sectors

# Sektör detayı (GYO)
curl https://temel-score-worker.paraanaliz.workers.dev/sectors/GYO

# Absolute skor
curl https://temel-score-worker.paraanaliz.workers.dev/absolute/AGESA
```

---

## 10. Mevcut Durum (Temmuz 2026)

| Metrik | Değer |
|--------|-------|
| Toplam şirket | 610 aktif |
| Puanlanan şirket | 578 (32'si veri eksik) |
| Skor ortalaması | 48.6 |
| Skor aralığı | 20.1 – 80.0 |
| Benchmark sayısı | 845 (53 sektör + 14 grup + market) |
| Sektör sayısı | 53 raw |
| Consolidated grup | 14 |
| Pillar config varyantı | 6 (_default, Bankacilik_Finans, Sigortacilik, GYO, Teknoloji_Iletisim, Holdingler) |
| En yüksek skor | LMKDC 80.04 (Çimento) |
| En düşük skor | CMBTN 20.12 (Demir-Çelik Döküm) |

### 10.1 Neden null Score?

Bazı şirketler (32 adet) skor alamaz:
- Yeni halka arz → mali tablo yok (`DOCO`, `ENPRA`, `INFO`)
- Finansal olmayan holding/fon yapısı (`GARFA`, `ISMEN`, `ISFIN`)
- Veri toplanamamış (`TERA`, `UFUK`, `UNLU`, `VAKFA`)
- Brokerage/bank dışı finans (`GEDIK`, `GLCVY`, `ISKUR`, `ISFIN`, `QNBFK`)

---

## 11. Hata Yönetimi

Worker'larda hatalar:
```json
{ "error": "not found", "status": 404 }
{ "error": "invalid scope", "status": 400 }
{ "error": "at least 2 tickers required", "status": 400 }
{ "error": "max 5 tickers", "status": 400 }
{ "error": "sector not found", "status": 404 }
```

Hono orchestrator:
- 404 → `data: null, error: "not found"`
- 400 → validasyon hatasını ilet
- Worker timeout → retry (max 2)
- Worker 500 → 502 Bad Gateway

---

## 12. Kurulum & Deploy

```bash
# Worker deploy
cd temel/ratio-worker && npx wrangler deploy
cd temel/score-worker && npx wrangler deploy

# D1 sorgu
npx wrangler d1 execute temel-db --command "SELECT COUNT(*) FROM companies" --remote

# Seed consolidation
curl https://temel-score-worker.paraanaliz.workers.dev/seed_consolidation
```

---

## 13. Önemli Notlar

1. **Tüm skorlar TTM bazlı** — trailing twelve months, en son 4 çeyrek
2. **Rasyo hesaplama metodu**: `calculation_method = 'v2'`
3. **COGS ve faiz gideri** MaliTablo'da negatif saklanır → `abs()` ile çevrilir
4. **Forward rasyolar** İş Yatırım'dan referans olarak alınır, hesaplanmaz
5. **Worker'lar arası iletişim yok** — her worker D1'e direkt bağlanır
6. **Cron deploy** wrangler ile çalışmaz → Cloudflare Dashboard manuel
