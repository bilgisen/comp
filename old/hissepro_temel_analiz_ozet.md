# HissePro — Temel Analiz & Sektör Medyanı: Proje Özeti

---

## 1. KAPSAM

Bu belge, HissePro platformunun `/comp` (company engine) bileşeni için yapılan mimari ve metodoloji çalışmasını özetler. Kapsam: İş Yatırım'dan mali tablo çekme, rasyo hesaplama, sektör medyanı üretme ve F1–F5 outlier filtre pipeline'ı.

---

## 2. SEKTÖR YAPISI — İKİ KATMANLI MODEL

### Karar
Ham sektör sayısı ~53 (İş Yatırım/KAP kaynaklı) → **14 Ana Sektörde** konsolide edildi.

### Gerekçe
- Tek şirketli sektörlerde medyan = şirketin kendi değeri → peer comparison işlevsiz
- İstatistiki güvenilirlik için minimum n≥5 peer gerekiyor
- UI'da 53 sektör yerine 14 sektör → temiz kullanıcı deneyimi

### Veritabanı Yapısı
```
companies.sektor_ham  → "Kırtasiye"  (KAP'tan gelen orijinal, korunur)
companies.sektor_ana  → "Tüketim & Perakende & Tekstil"  (medyan + UI için)
```

### 14 Ana Sektör

| # | Ana Sektör | financial_group | Not |
|---|---|---|---|
| 1 | Bankacılık & Finans | UFRS_K / UFRS_F | Ayrı rasyo seti |
| 2 | Sigortacılık | UFRS_S | Ayrı rasyo seti |
| 3 | GYO | XI_29 | Cari oran hesaplanmaz |
| 4 | Enerji & Altyapı | XI_29 | |
| 5 | Sanayi & Metal & Kimya | XI_29 | |
| 6 | İnşaat & Yapı Malzemeleri | XI_29 | |
| 7 | Otomotiv & Savunma & Makine | XI_29 | |
| 8 | Sağlık & İlaç | XI_29 | Yüksek F/K toleransı |
| 9 | Teknoloji & İletişim | XI_29 | Derin zarar olabilir |
| 10 | Gıda & İçecek & Tarım | XI_29 | |
| 11 | Tüketim & Perakende & Tekstil | XI_29 | |
| 12 | Ulaştırma & Lojistik | XI_29 | |
| 13 | Turizm & Medya & Eğlence | XI_29 | Sezonsal |
| 14 | Holdingler | XI_29 | Heterojen yapı |
| — | Diğer / Spor | — | Medyan hesap dışı |

---

## 3. VERİ KAYNAĞI — İŞ YATIRIM API

### Endpoint
```
https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo
  ?companyCode=GARAN
  &exchange=TRY
  &financialGroup=UFRS_K
  &year1=2026&period1=3    ← value1
  &year2=2025&period2=12   ← value2 (yıllık)
  &year3=2025&period3=9    ← value3
  &year4=2025&period4=6    ← value4
  &_={timestamp}
```

### Kritik: Dönem Davranışı Farkı

| financialGroup | Gelir Tablosu Davranışı | TTM Hesabı |
|---|---|---|
| UFRS_K (Bankalar) | **Kümülatif** (yıl başından) | value2 (period=12) direkt kullan |
| XI_29 (Sanayi vb.) | **Çeyreklik** (sadece o çeyrek) | value1+v2+v3+v4 toplamı |

---

## 4. UFRS_K ITEM CODE MAPPING (GARAN ile doğrulandı)

### Hiyerarşi Kuralı
```
Prefix:  1x=Aktif  2x=Pasif  3x=Gelir Tablosu
Suffix uzunluğu: 1 karakter = özet/toplam, 2+ karakter = alt detay
Kural: Rasyo hesabında daima en kısa (en üst) code kullan.
```

### Kritik Kodlar

**Bilanço:**
- `1Z` Toplam Aktif, `2Z` Toplam Pasif (kontrol: eşit olmalı)
- `2O` Özkaynaklar, `2OV` Dönem Net Karı, `2OVA` Azınlık Payları
- `2A` Mevduat, `1AF` Toplam Krediler
- `2C` Alınan Krediler, `2D` Para Piyasası Borçları, `2E` İhraç Edilen Menkul, `2NBA` Sermaye Benzeri

**Gelir Tablosu:**
- `3A` Faiz Gelirleri, `3B` Faiz Giderleri, `3C` Net Faiz Geliri (NII)
- `3CA` Net Komisyon, `3CE` Toplam Faaliyet Geliri
- `3CF` Karşılık Gideri, `3CG` Opex
- `3Z` Konsolide Net Kar, `3ZA` Ana Ortaklık Net Karı ← **rasyo hesabında bu**

### GARAN 2026Q1 Doğrulama Değerleri
```
Toplam Aktif (1Z):          4,783,750,292,000 TRY
Mevduat (2A):               3,166,804,452,000 TRY
Krediler (1AF):             2,768,109,767,000 TRY
Özkaynaklar (2O):             453,087,703,000 TRY
Net Kar Q1 2026 (3ZA):         33,154,454,000 TRY
Net Kar 2025 yıllık (3ZA):    109,816,312,000 TRY

Kontrol rasyoları:
  Kredi/Mevduat: 87.4%  |  ROE (2025): 26.4%  |  ROA (2025): 2.55%
  Cost/Income: 26.1%    |  NIM: ~7% (yaklaşık)
```

### Açık Kalan Sorunlar
- `1AFD` (Takipteki Krediler) GARAN'da 0 → NPL ayrı tabloda, endpoint araştırılacak
- `1AS` 2026Q1'de 221T (normal 5T) → Durdurulan faaliyet (sigorta iştiraki satışı)
- `2OVA` azınlık payları özkaynağa dahil → ROE/PD-DD için `2O - 2OVA` kullan

---

## 5. ÇEKME SİSTEMİ MİMARİSİ

### Karar: Diff-Based Yarı-Otomatik (hafta sonu manuel değil)

**Neden:** Şirketlerin ~%40'ı çeyrek sonrası 45-60. günde raporlar. Hafta sonu kontrolü bu şirketleri kaçırır. Diff-based sistemde değişmeyen şirket için maliyet sıfır.

### Üç Katmanlı Scheduler
```
Layer 1: Her gün 07:00 TSİ
         Kapsam: KAP raporlama penceresi içindeki şirketler (çeyrek+75 gün)

Layer 2: Pazar 04:00 TSİ  
         Kapsam: Tüm aktif şirketler (safety net)

Layer 3: Manuel tetikleme (Admin UI)
         Kapsam: Tek şirket veya sektör
```

### Raporlama Pencereleri
- Q1 (Mart): Nisan–Mayıs
- Q2 (Haziran): Temmuz–Ağustos
- Q3 (Eylül): Ekim–Kasım
- Q4 (Aralık): Ocak–Mart (en uzun)

### Rate Limiting
```python
requests_per_minute: 20
delay_between_requests: 3.0s (jitter: 2.5–4.0)
batch_size: 50 şirket
session_break: 120s (50 şirket sonrası)
max_retries: 3, backoff: [5, 15, 45]s
```

### Diff Mantığı
```
fetch_and_diff():
  1. İş Yatırım'dan çek
  2. MD5(raw_json) hesapla
  3. fetch_log'daki son checksum ile karşılaştır
  4. Aynıysa → DB'ye yazma, bitir
  5. Farklıysa → upsert raw + rasyo hesabı kuyruğa al + medyan invalidate
```

---

## 6. RASYO HESAPLAMA

### TTM Kuralı
- **Bilanço rasyoları** (Cari Oran, B/Ö): Son dönemin anlık değeri
- **Gelir tablosu rasyoları** (Net Marj, EBITDA Marjı): TTM zorunlu
  - Bankalar: `period=12` (yıllık) direkt
  - Sanayi/XI_29: Son 4 çeyrek toplamı
- TTM için eksik çeyrek varsa → `NULL` → F2 filtresiyle medyandan çıkar

### ROE/ROA için Ortalama Özkaynak
```
oz_ort = (2O_v1 + 2O_v2) / 2  ← dönem başı + dönem sonu ortalaması
```

### Sektöre Özel Rasyo Setleri
Her `sektor_ana` için `SEKTOR_RASYO_CONFIG` dict'i tanımlı:
- Bankacılık: NIM, Kredi/Mevduat, Sermaye Yeterlilik, NPL, ROE, ROA, F/K, PD/DD
- GYO: NAV İskonto, Kira Getirisi, Borçlanma, FAVOK Marjı (cari oran yok)
- Default (XI_29): Cari Oran, Asit Test, Net Borç/Özkaynak, Brüt/FAVOK/Net Marj, ROE, ROA, F/K, FD/FAVOK, PD/DD

---

## 7. SEKTÖR MEDYANI — F1–F5 FİLTRE PIPELINE'I

### Pipeline Akışı
```
Ham Rasyo Havuzu
  │
  ▼ F1: NULL / Infinity → DROP
  ▼ F2: Min. dönem verisi (son 4 çeyrekte ≥3 rapor) → DROP
  ▼ F3: Ekonomik geçerlilik (sektöre özel sınır tablosu) → DROP
  ▼ F4: Winsorization p5–p95 (uç değerleri sınır değere çek)
  ▼ F5: Min. peer sayısı kontrolü
        n≥10 → HIGH  |  n≥5 → MEDIUM  |  n≥3 → LOW  |  n<3 → hesaplanmaz
```

### F3 Ekonomik Sınırlar — Önemli Örnekler
```python
"_default": {
    "fk_orani":         (0.0, 150.0),   # negatif F/K medyandan çıkar
    "net_kar_marji":    (-2.00, 0.60),  # tek seferlik zararlar
    "roe":              (-1.00, 1.50),
},
"Bankacılık & Finans": {
    "nfm":              (-0.02, 0.12),
    "sermaye_yeterlilik": (0.08, 0.40), # Basel min %8
    "npl_orani":        (0.0, 0.25),
},
"Teknoloji & İletişim": {
    "net_kar_marji":    (-5.00, 0.70),  # yazılım start-up derin zarar
    "fk_orani":         (0.0, 200.0),   # yüksek büyüme primi
},
```

### Neden Winsorization, Trim Değil?
BIST'te küçük gruplarda trim yapmak n'yi daha da düşürür. Winsorization uç değerleri silerek değil sınır değere çekerek hesaba katar — n korunur, outlier etkisi kırılır.

### Medyan Tipleri
```python
median_ew = np.median(values)                              # equal-weight (UI'da gösterilir)
median_wt = weighted_quantile(values, market_caps, q=0.5)  # market-cap weighted (saklanır)
```

### Güncelleme Tetikleyicisi: Event-Driven
```
Yeni mali tablo geldi
  → company_ratios güncellendi
  → sector_median_invalidation_queue'ya mesaj at
  → async worker medyanı yeniden hesapla
  → Redis cache güncelle (TTL: 24 saat)
```
Gece toplu job değil — bir şirket gelince sadece o sektörün medyanı yenilenir.

### Kullanıcıya Sunum: Persentil
```
Şirket Cari Oranı: 2.4  |  Sektör Medyanı: 1.6  |  IQR: [1.1 – 2.1]
→ Kullanıcıya gösterilen: 78. persentil

NOT: Z-score değil persentil — rasyo dağılımları sağa çarpık,
     persentil dağılımdan bağımsız çalışır.
```

---

## 8. VERİTABANI ŞEMASI (6 Tablo)

```
companies              → şirket meta verisi (sektor_ham, sektor_ana, financial_group)
fetch_log              → her çekim girişimi + checksum (diff sistemi)
financial_statements_raw → ham item_code satırları (normalize edilmemiş)
company_ratios         → hesaplanan rasyolar (TTM flag'li)
sector_medians         → hesaplanan medyanlar (equal-weight + weighted, reliability)
sector_median_peers    → hangi şirket dahil/hariç, neden (audit trail)
```

---

## 9. AÇIK KALAN İŞLER (Öncelik Sırasıyla)

| # | Görev | Bağımlılık |
|---|---|---|
| 1 | **XI_29 item code mapping** | BIMAS veya EREGL response'u çek, manuel onayla |
| 2 | **NPL endpoint araştırması** | 1AFD GARAN'da 0, ayrı tablo var |
| 3 | **company_ratios worker** | XI_29 mapping tamamlandıktan sonra |
| 4 | **TTM hesaplama mantığı** | UFRS_K (yıllık) vs XI_29 (4 çeyrek) ayrımı |
| 5 | **F1–F5 filtre pipeline implement** | company_ratios hazır olunca |
| 6 | **Sector median worker** | Filtre pipeline sonrası |
| 7 | **APScheduler scheduler** | Worker'lar hazır olunca |
| 8 | **Admin UI** | Manuel tetikleme + fetch_log görüntüleme |

---

## 10. KRİTİK PRENSİPLER (Değişmez Kararlar)

1. **LLM asla veri kaynağı değil.** Tüm finansal değerler İş Yatırım API'sinden gelir. LLM sadece sentez/yorum katmanında çalışır.

2. **Negatif F/K medyandan çıkar.** `fk_orani` için `min=0.0` — ekonomik anlamsız.

3. **GYO'da cari oran hesaplanmaz.** `SEKTOR_RASYO_CONFIG["GYO"]` listesinde yok.

4. **UFRS_K gelir tablosu kümülatif.** Q1 değerini yıllıklaştırma — `period=12` kullan.

5. **`2OVA` azınlık paylarını ROE/PD-DD'den çıkar.** Ana ortaklık özkaynak = `2O - 2OVA`.

6. **Diff olmadan yazma.** Checksum eşleşiyorsa rasyo ve medyan yeniden hesaplanmaz.

7. **Circuit breaker state Redis'te.** In-memory değil — Cloud Run multi-instance.
