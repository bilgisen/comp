# Antigravity IDE — Mali Tablo Çekme Sistemi & F3 Filtresi
## Uygulama Talimatı

---

## 1. GENEL MİMARİ KARAR

**Hafta sonu manuel tetiklemeli değil — yarı-otomatik diff-based sistem kuruyoruz.**

Gerekçe: KAP bildirim tarihleri önceden bilinmez. Şirketlerin ~%40'ı çeyrek sonrası 45-60. günlerde raporlar. Hafta sonu kontrolü bu şirketleri kaçırır. Aşağıdaki mimari hem otomasyonu sağlar hem de İş Yatırım'a aşırı yük bindirmez.

---

## 2. İŞ YATIRIM API — ENDPOINT ANATOMİSİ

```
https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo
  ?companyCode=GARAN
  &exchange=TRY
  &financialGroup=UFRS_K      ← UFRS_K | UFRS_F | UFRS_S | XI_29
  &year1=2026&period1=3       ← En güncel dönem (3=Q1, 6=Q2, 9=Q3, 12=Q4/Yıllık)
  &year2=2025&period2=12      ← 2. dönem
  &year3=2025&period3=9       ← 3. dönem
  &year4=2025&period4=6       ← 4. dönem
  &_=1779408457034            ← Cache-busting timestamp (her istekte yeni üret)
```

**financialGroup — Sektör Eşleştirmesi:**

| financialGroup | Kullanıldığı Ana Sektörler |
|---|---|
| `UFRS_K` | Bankacılık & Finans |
| `UFRS_F` | Fin. Kiralama & Faktoring |
| `UFRS_S` | Sigortacılık |
| `XI_29` | Diğer tüm sektörler (GYO dahil) |

Bu eşleştirme `company_metadata` tablosunda saklanır, her şirket için sabit.

---

## 3. VERİTABANI ŞEMASI

```sql
-- Şirket meta verisi (bir kez doldurulur, nadiren güncellenir)
CREATE TABLE companies (
    kod             TEXT PRIMARY KEY,         -- 'GARAN'
    hisse_adi       TEXT NOT NULL,
    sektor_ham      TEXT NOT NULL,            -- İş Yatırım'dan gelen orijinal
    sektor_ana      TEXT NOT NULL,            -- Konsolide grup (14 grup)
    financial_group TEXT NOT NULL,            -- 'UFRS_K', 'XI_29' vb.
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Her çekim girişiminin kaydı (audit + diff sistemi için)
CREATE TABLE fetch_log (
    id              BIGSERIAL PRIMARY KEY,
    kod             TEXT NOT NULL REFERENCES companies(kod),
    period_key      TEXT NOT NULL,            -- '2026Q1', '2025Q4' formatı
    fetched_at      TIMESTAMPTZ DEFAULT NOW(),
    http_status     INTEGER,
    row_count       INTEGER,                  -- API'den kaç satır geldi
    checksum        TEXT,                     -- MD5(raw_json) — diff için
    is_new_data     BOOLEAN,                  -- Önceki checksumdan farklı mı?
    error_msg       TEXT
);

-- Ham mali tablo satırları (normalize edilmemiş, kaynak verisi)
CREATE TABLE financial_statements_raw (
    id              BIGSERIAL PRIMARY KEY,
    kod             TEXT NOT NULL,
    period_key      TEXT NOT NULL,            -- '2025Q3'
    year            INTEGER NOT NULL,
    period          INTEGER NOT NULL,         -- 3,6,9,12
    financial_group TEXT NOT NULL,
    item_code       TEXT NOT NULL,            -- API'den gelen kalem kodu
    item_desc       TEXT,                     -- Kalem açıklaması
    value_try       NUMERIC,                  -- TRY cinsinden değer
    fetched_at      TIMESTAMPTZ NOT NULL,
    UNIQUE(kod, period_key, item_code)        -- Upsert için
);

-- Hesaplanan rasyolar (ham veriden türetilen)
CREATE TABLE company_ratios (
    id              BIGSERIAL PRIMARY KEY,
    kod             TEXT NOT NULL,
    period_key      TEXT NOT NULL,
    rasyo_kodu      TEXT NOT NULL,            -- 'cari_oran', 'net_marj' vb.
    rasyo_degeri    NUMERIC,
    is_ttm          BOOLEAN DEFAULT FALSE,    -- TTM hesabı mı?
    computed_at     TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(kod, period_key, rasyo_kodu)
);

-- Sektör medyanları (önceki konuşmadan)
CREATE TABLE sector_medians (
    id              BIGSERIAL PRIMARY KEY,
    sektor_ana      TEXT NOT NULL,
    rasyo_kodu      TEXT NOT NULL,
    period_key      TEXT NOT NULL,
    median_ew       NUMERIC,
    median_wt       NUMERIC,
    p25             NUMERIC,
    p75             NUMERIC,
    n_peers         INTEGER NOT NULL,
    n_excluded      INTEGER,
    reliability     TEXT CHECK (reliability IN ('HIGH','MEDIUM','LOW','INSUFFICIENT')),
    computed_at     TIMESTAMPTZ DEFAULT NOW(),
    is_stale        BOOLEAN DEFAULT FALSE,
    UNIQUE(sektor_ana, rasyo_kodu, period_key)
);

-- Hangi şirket medyana dahil/hariç (audit trail)
CREATE TABLE sector_median_peers (
    median_id       BIGINT REFERENCES sector_medians(id) ON DELETE CASCADE,
    kod             TEXT NOT NULL,
    rasyo_degeri    NUMERIC,
    is_included     BOOLEAN NOT NULL,
    exclusion_reason TEXT,    -- 'NULL_VALUE','BELOW_P5','ABOVE_P95','MIN_PERIODS','ECONOMIC_BOUNDS'
    PRIMARY KEY (median_id, kod)
);
```

---

## 4. ÇEKME SİSTEMİ — SCHEDULER MİMARİSİ

### 4a. Üç Katmanlı Zamanlama

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: Yoğun Dönem Taraması (Çeyrek Sonu Sonrası)   │
│  Çalışma: Her gün 07:00 (TSİ)                          │
│  Kapsam: Son çeyrek sonu + 75 gün içindeki tüm şirketler│
│  Mantık: KAP raporlama penceresi içindeyiz              │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: Haftalık Tam Tarama                           │
│  Çalışma: Pazar 04:00 (TSİ)                            │
│  Kapsam: Tüm aktif şirketler                            │
│  Mantık: Kaçırılan şirketler için safety net            │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: Manuel Tetikleme (Admin UI)                   │
│  Kapsam: Tek şirket veya sektör bazlı                  │
│  Mantık: Acil güncelleme ihtiyacı                       │
└─────────────────────────────────────────────────────────┘
```

**Raporlama Pencereleri (KAP mevzuatı):**
- Q1 (Mart): Nisan ve Mayıs boyunca
- Q2 (Haziran): Temmuz ve Ağustos boyunca  
- Q3 (Eylül): Ekim ve Kasım boyunca
- Q4/Yıllık (Aralık): Ocak-Mart arası (en uzun pencere)

Sistem bu pencerelerin dışında da çalışır — diff sistemli olduğu için maliyetsiz.

### 4b. Rate Limiting — İş Yatırım'a Saygılı Çekim

```python
FETCH_CONFIG = {
    "requests_per_minute": 20,      # Dakikada max 20 istek
    "delay_between_requests": 3.0,  # Saniye (jitter ile: 2.5-4.0)
    "batch_size": 50,               # Bir oturumda max şirket
    "timeout_seconds": 15,          # İstek timeout
    "max_retries": 3,               # 429/503 için retry
    "retry_backoff": [5, 15, 45],   # Retry bekleme süreleri (sn)
    "session_break": 120,           # 50 şirket sonrası 2 dk mola
}
```

### 4c. Diff-Based Güncelleme Mantığı

```python
async def fetch_and_diff(kod: str, period_key: str) -> FetchResult:
    """
    Yeni veri mi geldi yoksa değişmedi mi? Checksum ile anla.
    Değişmemişse DB'ye yazmadan geç.
    """
    raw_json = await fetch_from_isyatirim(kod, period_key)
    new_checksum = md5(raw_json)
    
    last_log = await db.fetch_one(
        "SELECT checksum FROM fetch_log WHERE kod=$1 AND period_key=$2 
         ORDER BY fetched_at DESC LIMIT 1",
        kod, period_key
    )
    
    is_new_data = (last_log is None) or (last_log.checksum != new_checksum)
    
    await db.insert("fetch_log", {
        "kod": kod,
        "period_key": period_key,
        "checksum": new_checksum,
        "is_new_data": is_new_data,
        "row_count": len(raw_json.get("items", []))
    })
    
    if is_new_data:
        await upsert_raw_statements(kod, period_key, raw_json)
        await trigger_ratio_calculation(kod, period_key)   # async queue
        await invalidate_sector_medians(kod)               # async queue
    
    return FetchResult(kod=kod, is_new=is_new_data, checksum=new_checksum)
```

### 4d. Dönem Parametresi Hesaplama

```python
from datetime import date

def get_periods_to_fetch(reference_date: date = None) -> list[dict]:
    """
    API'ye gönderilecek 4 dönem parametresini hesapla.
    Her zaman en güncel 4 çeyreği döndür.
    """
    if reference_date is None:
        reference_date = date.today()
    
    # Mevcut çeyreği bul
    month = reference_date.month
    year = reference_date.year
    
    # Raporlama gecikmesi: çeyrek bittikten 45+ gün sonra gelir
    # O yüzden "şu an hangi dönemin raporları yayında?" hesabı:
    if month <= 5:       # Ocak-Mayıs → Q4 önceki yıl + Q3, Q2, Q1
        current = (year-1, 12)
    elif month <= 8:     # Haziran-Ağustos → Q1 + Q4 önceki yıl + ...
        current = (year, 3)
    elif month <= 11:    # Eylül-Kasım → Q2 + Q1 + ...
        current = (year, 6)
    else:                # Aralık → Q3 + ...
        current = (year, 9)
    
    periods = []
    y, p = current
    quarter_map = {12: 9, 9: 6, 6: 3, 3: 12}
    
    for i in range(1, 5):
        periods.append({"year": y, "period": p, "idx": i})
        prev_p = quarter_map[p]
        if prev_p == 12:
            y -= 1
        p = prev_p
    
    return periods
```

---

## 5. F3 — EKONOMİK GEÇERLİLİK FİLTRESİ (DETAYLI)

### 5a. Sektöre Özel Sınır Tablosu

```python
# Tüm sınırlar: (min, max) — min/max dışı değerler medyandan hariç tutulur
# None = sınır uygulanmaz

ECONOMIC_BOUNDS: dict[str, dict[str, tuple]] = {

    # ── GENEL (tüm XI_29 sektörleri için default) ──────────────────────
    "_default": {
        "cari_oran":            (0.1, 15.0),
        "asit_test_orani":      (0.05, 12.0),
        "net_borclanma_orani":  (-2.0, 25.0),    # nakit zenginleri negatif olabilir
        "borclanma_orani":      (0.0, 15.0),
        "brut_kar_marji":       (-0.50, 0.95),
        "favok_marji":          (-0.50, 0.80),
        "net_kar_marji":        (-2.00, 0.60),   # tek seferlik zarar: -200% olabilir ama medyandan hariç
        "roe":                  (-1.00, 1.50),
        "roa":                  (-0.30, 0.40),
        "fk_orani":             (0.0, 150.0),    # negatif F/K medyandan çıkar
        "fd_favok":             (0.0, 60.0),
        "pd_dd":                (0.0, 20.0),
    },

    # ── BANKACILIK & FİNANS ────────────────────────────────────────────
    "Bankacılık & Finans": {
        # Bankalar için cari oran anlamsız — hesaplanmaz
        "nfm":                  (-0.02, 0.12),   # Net Faiz Marjı
        "kredi_mevduat_orani":  (0.30, 2.50),
        "sermaye_yeterlilik":   (0.08, 0.40),    # Basel minimum %8
        "npl_orani":            (0.0, 0.25),     # Takipteki kredi oranı
        "roe":                  (-0.30, 0.50),
        "roa":                  (-0.05, 0.08),
        "fk_orani":             (0.0, 25.0),
        "pd_dd":                (0.0, 5.0),
    },

    # ── SİGORTACILIK ──────────────────────────────────────────────────
    "Sigortacılık": {
        "hasarprim_orani":      (0.20, 1.20),    # >1.0 teknik zarar bölgesi
        "masraf_orani":         (0.05, 0.50),
        "bilesik_oran":         (0.40, 1.40),    # hasarprim + masraf
        "prim_artis_orani":     (-0.30, 3.00),
        "roe":                  (-0.30, 0.80),
        "fk_orani":             (0.0, 30.0),
    },

    # ── GYO ───────────────────────────────────────────────────────────
    "GYO": {
        # Cari oran GYO için hesaplanmaz (anlamsız)
        "nav_iskonto_orani":    (-0.85, 0.50),   # NAV'a iskonto/prim
        "kira_getiri_orani":    (0.01, 0.25),
        "borclanma_orani":      (0.0, 10.0),     # GYO'da leverage yüksek olabilir
        "favok_marji":          (-0.20, 0.95),
        "fk_orani":             (0.0, 50.0),
        "pd_dd":                (0.0, 5.0),
    },

    # ── ENERJİ (Üretim + Dağıtım + Petrol) ───────────────────────────
    "Enerji & Altyapı": {
        "cari_oran":            (0.1, 10.0),
        "net_borclanma_orani":  (-1.0, 20.0),    # Enerji altyapısı yüksek kaldıraç
        "favok_marji":          (-0.20, 0.85),
        "net_kar_marji":        (-1.00, 0.60),
        "fk_orani":             (0.0, 80.0),     # Enerji F/K yüksek olabilir
        "fd_favok":             (0.0, 25.0),
    },

    # ── SANAYİ & METAL & KİMYA ────────────────────────────────────────
    "Sanayi & Metal & Kimya": {
        "cari_oran":            (0.1, 12.0),
        "brut_kar_marji":       (-0.20, 0.80),
        "favok_marji":          (-0.30, 0.60),
        "net_kar_marji":        (-1.50, 0.50),
        "net_borclanma_orani":  (-2.0, 20.0),
    },

    # ── SAĞLIK & İLAÇ ─────────────────────────────────────────────────
    "Sağlık & İlaç": {
        "brut_kar_marji":       (0.0, 0.95),     # İlaç yüksek marj
        "favok_marji":          (-0.30, 0.70),
        "ar_ge_gider_orani":    (0.0, 0.40),
        "fk_orani":             (0.0, 100.0),    # Büyüme şirketleri yüksek F/K
    },

    # ── TEKNOLOJİ & İLETİŞİM ─────────────────────────────────────────
    "Teknoloji & İletişim": {
        "brut_kar_marji":       (-0.10, 0.99),
        "favok_marji":          (-1.00, 0.80),   # Erken aşama şirketler zarar olabilir
        "net_kar_marji":        (-5.00, 0.70),   # Yazılım start-up: derin zarar mümkün
        "fk_orani":             (0.0, 200.0),    # Yüksek büyüme primi
        "pd_dd":                (0.0, 30.0),
    },

    # ── GIDA & İÇECEK & TARIM ────────────────────────────────────────
    "Gıda & İçecek & Tarım": {
        "cari_oran":            (0.1, 8.0),
        "brut_kar_marji":       (-0.05, 0.70),
        "favok_marji":          (-0.20, 0.45),
        "stok_devir_hizi":      (1.0, 50.0),    # Gıda hızlı devir
    },

    # ── TÜKETİM & PERAKENDE & TEKSTİL ────────────────────────────────
    "Tüketim & Perakende & Tekstil": {
        "cari_oran":            (0.1, 8.0),
        "brut_kar_marji":       (-0.10, 0.80),
        "stok_devir_hizi":      (0.5, 30.0),
        "alacak_devir_hizi":    (1.0, 100.0),
    },

    # ── ULAŞTIRMA & LOJİSTİK ─────────────────────────────────────────
    "Ulaştırma & Lojistik": {
        "net_borclanma_orani":  (-1.0, 20.0),   # Filo finansmanı yüksek borç
        "favok_marji":          (-0.30, 0.60),
        "fk_orani":             (0.0, 50.0),
        "pd_dd":                (0.0, 10.0),
    },

    # ── TURİZM & MEDYA & EĞLENCE ─────────────────────────────────────
    "Turizm & Medya & Eğlence": {
        "favok_marji":          (-0.50, 0.70),   # Sezonsal şirketler
        "net_kar_marji":        (-2.00, 0.50),
        "net_borclanma_orani":  (-1.0, 15.0),
    },

    # ── HOLDİNGLER ───────────────────────────────────────────────────
    "Holdingler": {
        # Holdingler konsolide tabloda değişken yapı
        "pd_dd":                (0.0, 5.0),
        "net_borclanma_orani":  (-2.0, 15.0),
        "roe":                  (-0.50, 1.00),
        "fk_orani":             (0.0, 100.0),
    },

    # ── OTOMOTİV & SAVUNMA & MAKİNE ──────────────────────────────────
    "Otomotiv & Savunma & Makine": {
        "cari_oran":            (0.2, 10.0),
        "brut_kar_marji":       (-0.10, 0.65),
        "favok_marji":          (-0.20, 0.40),
        "net_borclanma_orani":  (-2.0, 15.0),
    },

    # ── İNŞAAT & YAPI MALZEMELERİ ───────────────────────────────────
    "İnşaat & Yapı Malzemeleri": {
        "cari_oran":            (0.1, 10.0),
        "net_borclanma_orani":  (-1.0, 20.0),
        "favok_marji":          (-0.30, 0.65),
        "proje_doluluğu":       (0.0, 1.0),     # İnşaat'a özel
    },
}
```

### 5b. F3 Filtre Fonksiyonu

```python
def f3_economic_validity(
    rasyo_kodu: str,
    rasyo_degeri: float | None,
    sektor_ana: str
) -> tuple[bool, str | None]:
    """
    Değer ekonomik olarak geçerli mi?
    
    Returns:
        (is_valid, exclusion_reason)
        exclusion_reason: None ise geçerli, string ise hariç tutulma sebebi
    """
    if rasyo_degeri is None or not math.isfinite(rasyo_degeri):
        return False, "NULL_OR_INFINITE"
    
    # Sektöre özel bounds varsa onu al, yoksa default'u
    sektor_bounds = ECONOMIC_BOUNDS.get(sektor_ana, ECONOMIC_BOUNDS["_default"])
    default_bounds = ECONOMIC_BOUNDS["_default"]
    
    bounds = sektor_bounds.get(rasyo_kodu) or default_bounds.get(rasyo_kodu)
    
    if bounds is None:
        # Bu sektör için bu rasyo tanımlı değil — hesaplanmaz
        return False, "RASYO_SEKTOR_UYUMSUZ"
    
    min_val, max_val = bounds
    
    if min_val is not None and rasyo_degeri < min_val:
        return False, f"BELOW_ECONOMIC_MIN({min_val})"
    
    if max_val is not None and rasyo_degeri > max_val:
        return False, f"ABOVE_ECONOMIC_MAX({max_val})"
    
    return True, None
```

### 5c. Tam Filtre Pipeline (F1 → F5)

```python
def run_filter_pipeline(
    peers: list[dict],          # [{"kod": "GARAN", "rasyo_degeri": 12.5}, ...]
    rasyo_kodu: str,
    sektor_ana: str,
    min_periods: int = 3        # Son kaç dönemde veri olmalı?
) -> FilterResult:

    included = []
    excluded = []

    for peer in peers:
        kod = peer["kod"]
        value = peer["rasyo_degeri"]
        available_periods = peer["available_periods"]  # kaç dönem verisi var

        # F1: NULL / Sonsuz
        if value is None or not math.isfinite(value):
            excluded.append({"kod": kod, "reason": "F1_NULL_OR_INFINITE"})
            continue

        # F2: Minimum dönem verisi
        if available_periods < min_periods:
            excluded.append({"kod": kod, "reason": f"F2_INSUFFICIENT_PERIODS({available_periods})"})
            continue

        # F3: Ekonomik geçerlilik
        is_valid, reason = f3_economic_validity(rasyo_kodu, value, sektor_ana)
        if not is_valid:
            excluded.append({"kod": kod, "reason": f"F3_{reason}"})
            continue

        # F4: İstatistiksel outlier (Winsorization için sınır tespiti)
        # Not: F4 tüm included listesi toplandıktan sonra uygulanır
        included.append({"kod": kod, "value": value})

    # F4: Winsorization (p5-p95)
    if len(included) >= 5:
        values = [p["value"] for p in included]
        p5 = np.percentile(values, 5)
        p95 = np.percentile(values, 95)
        
        final_included = []
        for peer in included:
            if peer["value"] < p5:
                excluded.append({"kod": peer["kod"], "reason": f"F4_BELOW_P5({p5:.4f})"})
            elif peer["value"] > p95:
                excluded.append({"kod": peer["kod"], "reason": f"F4_ABOVE_P95({p95:.4f})"})
            else:
                final_included.append(peer)
        included = final_included

    # F5: Minimum peer kontrolü
    n = len(included)
    reliability = (
        "HIGH"         if n >= 10 else
        "MEDIUM"       if n >= 5  else
        "LOW"          if n >= 3  else
        "INSUFFICIENT"
    )

    return FilterResult(
        included=included,
        excluded=excluded,
        n_peers=n,
        reliability=reliability,
        can_compute=(n >= 3)
    )
```

---

## 6. RASYO HESAPLAMA — SEKTOR BAZLI KONFİGÜRASYON

```python
# Her sektör için hangi rasyolar hesaplanır ve formülleri
# Mali tablo item_code'ları İş Yatırım API'sinden gelir

SEKTOR_RASYO_CONFIG = {
    "_default": [
        # (rasyo_kodu, formül_lambda, dönem_tipi)
        # dönem_tipi: 'instant' = bilanço, 'ttm' = gelir tablosu
        ("cari_oran",           lambda t: t["donen_varliklar"] / t["kisa_vadeli_yukumlulukler"], "instant"),
        ("asit_test_orani",     lambda t: (t["donen_varliklar"] - t["stoklar"]) / t["kisa_vadeli_yukumlulukler"], "instant"),
        ("borclanma_orani",     lambda t: t["toplam_yukumlulukler"] / t["toplam_varliklar"], "instant"),
        ("net_borclanma_orani", lambda t: (t["finansal_borclar"] - t["nakit_ve_esdeğerleri"]) / t["ozkaynaklar"], "instant"),
        ("brut_kar_marji",      lambda t: t["brut_kar"] / t["net_satislar"], "ttm"),
        ("favok_marji",         lambda t: t["favok"] / t["net_satislar"], "ttm"),
        ("net_kar_marji",       lambda t: t["net_kar"] / t["net_satislar"], "ttm"),
        ("roe",                 lambda t: t["net_kar_ttm"] / t["ozkaynaklar_ort"], "ttm"),
        ("roa",                 lambda t: t["net_kar_ttm"] / t["toplam_varliklar_ort"], "ttm"),
        ("fk_orani",            lambda t: t["piyasa_degeri"] / t["net_kar_ttm"], "ttm"),
        ("fd_favok",            lambda t: (t["piyasa_degeri"] + t["net_borc"]) / t["favok_ttm"], "ttm"),
        ("pd_dd",               lambda t: t["piyasa_degeri"] / t["ozkaynaklar"], "instant"),
    ],
    "Bankacılık & Finans": [
        ("nfm",                 lambda t: t["net_faiz_geliri"] / t["faiz_getirili_varliklar_ort"], "ttm"),
        ("kredi_mevduat_orani", lambda t: t["krediler"] / t["mevduat"], "instant"),
        ("sermaye_yeterlilik",  lambda t: t["sermaye_yeterlilik_rasyosu"], "instant"),  # KAP'tan direkt
        ("npl_orani",           lambda t: t["takipteki_krediler"] / t["toplam_krediler"], "instant"),
        ("roe",                 lambda t: t["net_kar_ttm"] / t["ozkaynaklar_ort"], "ttm"),
        ("roa",                 lambda t: t["net_kar_ttm"] / t["toplam_varliklar_ort"], "ttm"),
        ("fk_orani",            lambda t: t["piyasa_degeri"] / t["net_kar_ttm"], "ttm"),
        ("pd_dd",               lambda t: t["piyasa_degeri"] / t["ozkaynaklar"], "instant"),
    ],
    "Sigortacılık": [
        ("hasarprim_orani",     lambda t: t["odenen_hasarlar"] / t["kazanilan_primler"], "ttm"),
        ("masraf_orani",        lambda t: t["isletme_giderleri"] / t["kazanilan_primler"], "ttm"),
        ("bilesik_oran",        lambda t: (t["odenen_hasarlar"] + t["isletme_giderleri"]) / t["kazanilan_primler"], "ttm"),
        ("roe",                 lambda t: t["net_kar_ttm"] / t["ozkaynaklar_ort"], "ttm"),
        ("fk_orani",            lambda t: t["piyasa_degeri"] / t["net_kar_ttm"], "ttm"),
    ],
    # ... diğer sektörler benzer yapıda
}
```

---

## 7. MEDYAN HESAPLAMA WORKER

```python
async def compute_sector_median(sektor_ana: str, rasyo_kodu: str, period_key: str):
    """
    Sektör medyanını hesapla ve sector_medians tablosuna yaz.
    Event-driven: company_ratios tablosuna yeni kayıt girince tetiklenir.
    """
    # 1. Bu sektör için tüm şirketleri ve rasyolarını çek
    peers_raw = await db.fetch_all("""
        SELECT cr.kod, cr.rasyo_degeri, c.sektor_ana,
               COUNT(*) OVER (PARTITION BY cr.kod) as available_periods
        FROM company_ratios cr
        JOIN companies c ON cr.kod = c.kod
        WHERE c.sektor_ana = $1
          AND cr.rasyo_kodu = $2
          AND cr.period_key = $3
          AND c.is_active = TRUE
    """, sektor_ana, rasyo_kodu, period_key)
    
    # 2. Filtre pipeline'ını çalıştır (F1-F5)
    result = run_filter_pipeline(peers_raw, rasyo_kodu, sektor_ana)
    
    if not result.can_compute:
        # n < 3: medyan hesaplanamaz, sadece log'la
        await log_insufficient_peers(sektor_ana, rasyo_kodu, period_key, result)
        return
    
    values = [p["value"] for p in result.included]
    market_caps = [get_market_cap(p["kod"]) for p in result.included]
    
    # 3. İki medyan hesapla
    median_ew = float(np.median(values))
    median_wt = float(weighted_quantile(values, market_caps, q=0.5))
    p25 = float(np.percentile(values, 25))
    p75 = float(np.percentile(values, 75))
    
    # 4. sector_medians tablosuna upsert
    median_id = await db.execute("""
        INSERT INTO sector_medians 
            (sektor_ana, rasyo_kodu, period_key, median_ew, median_wt, 
             p25, p75, n_peers, n_excluded, reliability, is_stale)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10, FALSE)
        ON CONFLICT (sektor_ana, rasyo_kodu, period_key) 
        DO UPDATE SET 
            median_ew=$4, median_wt=$5, p25=$6, p75=$7,
            n_peers=$8, n_excluded=$9, reliability=$10,
            computed_at=NOW(), is_stale=FALSE
        RETURNING id
    """, sektor_ana, rasyo_kodu, period_key,
         median_ew, median_wt, p25, p75,
         result.n_peers, len(result.excluded), result.reliability)
    
    # 5. Audit trail: hangi şirket dahil/hariç
    await db.executemany("""
        INSERT INTO sector_median_peers (median_id, kod, rasyo_degeri, is_included, exclusion_reason)
        VALUES ($1,$2,$3,$4,$5)
        ON CONFLICT (median_id, kod) DO UPDATE SET
            rasyo_degeri=$3, is_included=$4, exclusion_reason=$5
    """, [
        (median_id, p["kod"], p["value"], True, None) for p in result.included
    ] + [
        (median_id, e["kod"], e.get("value"), False, e["reason"]) for e in result.excluded
    ])
```

---

## 8. UYGULAMA SIRASI

```
Hafta 1:
  [x] companies tablosunu doldur (sektor_ham → sektor_ana mapping dahil)
  [x] İş Yatırım fetch fonksiyonu + rate limiter
  [x] financial_statements_raw upsert
  [x] fetch_log + diff sistemi

Hafta 2:
  [x] Item code → rasyo mapping (İş Yatırım'ın item_code'larını incele, eşleştir)
  [x] company_ratios hesaplama worker
  [x] TTM hesaplama mantığı
  [x] F3 ECONOMIC_BOUNDS config (yukarıdaki tablodan)

Hafta 3:
  [x] Tam filtre pipeline F1-F5
  [x] Sektör medyan worker
  [x] sector_median_peers audit trail
  [x] Event-driven invalidation (Redis Pub/Sub veya Supabase realtime)

Hafta 4:
  [x] Scheduler (APScheduler veya Cloud Scheduler)
  [x] Admin UI: manuel tetikleme, fetch_log görüntüleme
  [x] Alerting: checksum değişimi → Slack/e-posta bildirimi
```

---

## 9. KRİTİK NOTLAR

1. **Item code mapping önceliklidir.** İş Yatırım API'si item_code olarak numerik veya kısa string kodlar döndürür. Bunları `brut_kar`, `net_satislar` gibi semantik isimlerle eşleştiren bir mapping tablosu olmadan rasyo hesaplanamaz. İlk çekimde GARAN ve BIMAS için tam response'u logla, item_code listesini çıkar, mapping'i elle onayla.

2. **TTM için 4 çeyrek şart.** Şirketin son 4 çeyreğinde hiç eksik yoksa TTM hesaplanır. Eksik varsa `NULL` — medyandan F2 ile çıkar.

3. **Negatif F/K medyandan çıkar (F3).** Zarar eden şirketin F/K'sı negatif — ekonomik olarak anlamsız. `fk_orani` için `min=0.0` sınırı bunu otomatik hariç tutar.

4. **GYO'da cari oran hesaplanmaz.** `SEKTOR_RASYO_CONFIG["GYO"]` listesinde `cari_oran` bulunmaz. F3'te `RASYO_SEKTOR_UYUMSUZ` döner.

5. **Haftalık tam taramada checksum diff'i kullan** — değişmeyen şirketler için rasyo ve medyan yeniden hesaplanmaz.

---

## 10. İŞ YATIRIM API — GERÇEK ITEM CODE MAPPING (UFRS_K / BANKALAR)

### 10a. Item Code Hiyerarşi Mantığı

```
PREFIX (ilk karakter):
  1x  →  AKTİF     (Bilanço - Varlıklar)
  2x  →  PASİF     (Bilanço - Kaynaklar & Özkaynaklar)
  3x  →  GELİR TABLOSU

SUFFIX UZUNLUĞU (derinlik):
  1 karakter  (1Z, 2O, 3A)  →  Özet / Ana toplam kalemi
  2 karakter  (1AF, 3CA)    →  Alt kalem L1
  3 karakter  (1AFD, 3CAA)  →  Alt kalem L2
  4 karakter  (1AFA, 3CAB)  →  Alt kalem L3 (detay)

KURAL: Rasyo hesabında daima en kısa (en üst) code'u kullan.
       1Z = toplam aktif, alt kalemleri toplamak yerine direkt al.
```

### 10b. UFRS_K Bankacılık — Kritik Item Codes

```python
UFRS_K_ITEM_MAP = {

    # ── BİLANÇO: AKTİF ──────────────────────────────────────────────
    "toplam_aktif":              "1Z",
    "nakit_ve_mb":               "1A",    # Nakit + Merkez Bankası
    "bankalar":                  "1AC",   # Yabancı muhabir bankalar
    "toplam_krediler":           "1AF",   # Gross krediler (brüt)
    "takipteki_krediler":        "1AFD",  # ⚠️ GARAN'da 0 → ayrı tablo
    "kiralama_alacaklari":       "1AL",
    "maddi_duran_varliklar":     "1AN",
    "maddi_olmayan_varliklar":   "1AO",
    "vergi_varligi":             "1AR",

    # ── BİLANÇO: PASİF ──────────────────────────────────────────────
    "toplam_pasif":              "2Z",    # Kontrol: 2Z == 1Z olmalı
    "mevduat":                   "2A",
    "alinan_krediler":           "2C",
    "para_piyasasi_borclari":    "2D",
    "ihrac_edilen_menkul":       "2E",    # Tahvil/bono ihraçları
    "karsilikar":                "2L",
    "vergi_borcu":               "2M",
    "sermaye_benzeri_krediler":  "2NBA",  # Subordinated debt
    "ozkaynaklar":               "2O",   # Toplam özkaynak
    "net_kar_donem":             "2OV",  # Dönem net karı (bilanço tarafı)
    "azinlik_paylari":           "2OVA",

    # ── GELİR TABLOSU ────────────────────────────────────────────────
    "faiz_gelirleri":            "3A",
    "faiz_giderleri":            "3B",
    "net_faiz_geliri":           "3C",   # NII = 3A - 3B (API zaten hesaplıyor)
    "net_komisyon_geliri":       "3CA",  # Net fee & commission
    "alinan_komisyon":           "3CAA", # Gross alınan
    "verilen_komisyon":          "3CAD", # Gross ödenen
    "temttu_gelirleri":          "3CB",
    "ticari_kar_zarar":          "3CC",  # Net trading (negatif olabilir)
    "diger_faaliyet_gelirleri":  "3CD",
    "toplam_faaliyet_geliri":    "3CE",  # Total banking income
    "kredi_karsililari":         "3CF",  # Provision for loan losses
    "diger_faaliyet_giderleri":  "3CG",  # OPEX (personel + genel gider)
    "net_faaliyet_kari":         "3CH",  # PPOP proxy (pre-provision op. profit)
    "vergi_oncesi_kar":          "3CL",  # Sürdürülen faaliyetler
    "vergi_karsılıgı":           "3CM",
    "net_kar_surdurulen":        "3CN",  # Sürdürülen faaliyetler net kar
    "net_kar_toplam":            "3Z",   # Konsolide net kar
    "net_kar_ana_ortaklik":      "3ZA",  # ← RASYO HESABINDA BU KULLANILIR
    "net_kar_azinlik":           "3ZB",
}
```

### 10c. Value Alanlarının Dönem Anlamı

```
API'ye gönderilen:  year1=2026, period1=3  → value1
                    year2=2025, period2=12  → value2
                    year3=2025, period3=9   → value3
                    year4=2025, period4=6   → value4

period değerleri:   3=Q1, 6=Q2, 9=Q3, 12=Q4 (tam yıl kümülatif)

BANKA GELİR TABLOSU DAVRANIŞI:
  Bankalar kümülatif raporlar (yıl başından itibaren toplamlar).
  value1 (Q1 2026) = Ocak-Mart 2026 toplamı
  value2 (Q4 2025) = Ocak-Aralık 2025 toplamı  ← TAM YIL
  value3 (Q3 2025) = Ocak-Eylül 2025 toplamı
  value4 (Q2 2025) = Ocak-Haziran 2025 toplamı

  TTM (Trailing 12 Month) = value2 (yıllık) kullan — banka için yeterli.
  Yıllıklaştırma: value1 × 4 ← sadece yaklaşık, mevsimsellik görmez.

XI_29 (Sanayi vb.) GELİR TABLOSU DAVRANIŞI:
  Çeyreklik raporlar (sadece o çeyreğin geliri).
  TTM = value1 + value2 + value3 + value4 (4 çeyrek toplamı).
  period=12 olan dönem YILLIK değil, sadece Q4 çeyreğidir.
```

### 10d. Bankacılık Rasyoları — Hesap Formülleri

```python
# value1 = son dönem (bilanço için anlık, gelir tablosu için kümülatif)
# value2 = önceki yıl sonu (yıllık gelir tablosu)

def compute_bank_ratios(items: dict, period: str) -> dict:
    """
    items: {item_code: float}  ← tüm dönemlerin value'ları
    period: '2026Q1', '2025Q4' vb.
    """
    is_annual = period.endswith("Q4")

    # Bilanço kalemleri (anlık - her zaman value1)
    toplam_aktif  = items["1Z"]["v1"]
    ozkaynaklar   = items["2O"]["v1"]
    mevduat       = items["2A"]["v1"]
    krediler      = items["1AF"]["v1"]

    # Ortalama hesabı için (ROE, ROA):
    ozkaynaklar_prev = items["2O"]["v2"]  # önceki dönem
    aktif_prev       = items["1Z"]["v2"]
    oz_ort = (ozkaynaklar + ozkaynaklar_prev) / 2
    aktif_ort = (toplam_aktif + aktif_prev) / 2

    # Gelir tablosu: yıllık veya TTM
    if is_annual:
        net_kar  = items["3ZA"]["v1"]   # Yıllık net kar (doğrudan)
        nii      = items["3C"]["v1"]
        opex     = items["3CG"]["v1"]
        toplam_g = items["3CE"]["v1"]
        provision= items["3CF"]["v1"]
        komisyon = items["3CA"]["v1"]
    else:
        # Q1/Q2/Q3 için: son yıllığı (v2) kullan, daha güvenilir
        net_kar  = items["3ZA"]["v2"]
        nii      = items["3C"]["v2"]
        opex     = items["3CG"]["v2"]
        toplam_g = items["3CE"]["v2"]
        provision= items["3CF"]["v2"]
        komisyon = items["3CA"]["v2"]
        # Alternatif: Q annualize (v1 × 4) — daha güncel ama gürültülü

    # Finansal borç (mevduat dışı)
    fin_borc = (
        items["2C"]["v1"] +   # Alınan krediler
        items["2D"]["v1"] +   # Para piyasası
        items["2E"]["v1"] +   # İhraç edilen menkul
        items["2NBA"]["v1"]   # Sermaye benzeri
    )

    return {
        "kredi_mevduat_orani":   safe_div(krediler, mevduat),
        "roe":                   safe_div(net_kar, oz_ort),
        "roa":                   safe_div(net_kar, aktif_ort),
        "pd_dd":                 None,  # piyasa değeri ayrıca gelir
        "cost_income_ratio":     safe_div(opex, toplam_g),
        "provision_gelir_orani": safe_div(provision, toplam_g),
        "nii_payed":             safe_div(nii, toplam_g),
        "komisyon_payed":        safe_div(komisyon, toplam_g),
        # NIM için faiz getirili varlık toplamı ayrıca hesaplanmalı
        # NPL için ayrı endpoint/tablo araştırılmalı
    }
```

### 10e. GARAN 2026Q1 Doğrulama — Referans Değerler

Mapping'in doğru çalıştığını test etmek için bu referans değerleri kullan:

```
Toplam Aktif (1Z):       4,783,750,292,000 TRY  (~4.78 T)
Mevduat (2A):            3,166,804,452,000 TRY  (~3.17 T)
Krediler (1AF):          2,768,109,767,000 TRY  (~2.77 T)
Özkaynaklar (2O):          453,087,703,000 TRY
Net Kar Q1 2026 (3ZA):      33,154,454,000 TRY
NII Q1 2026 (3C):           71,431,416,000 TRY
Net Kar 2025 yıllık (3ZA): 109,816,312,000 TRY
NII 2025 yıllık (3C):      204,745,374,000 TRY

Hesaplanan Rasyolar (kontrol):
  Kredi/Mevduat:   87.4%   (normal banka aralığı: 80-100%)
  ROE (2025):      26.4%
  ROA (2025):       2.55%
  Cost/Income:     26.1%   (2026Q1 kümülatif)
  NIM (tahmin):    ~7%     (faiz getirili varlık yaklaşımıyla)
```

### 10f. Kritik Uyarılar — Üretimde Dikkat Edilecekler

```
⚠️  1AFD (Takipteki Krediler): GARAN'da 0 dönüyor.
    NPL verisi büyük ihtimalle ayrı bir dipnot tablosunda.
    Çözüm: İş Yatırım'ın başka endpoint'lerini araştır
           veya NPL oranını sisteme manuel gir.

⚠️  1AS (Satış Amaçlı Duran Varlıklar): 2026Q1'de 221T TRY
    Diğer dönemlerde ~5T TRY → Durdurulan faaliyet etkisi.
    Bu kalem outlier filtreden geçer ama bilanço toplamını şişirir.
    Dönemler arası karşılaştırmada bu farkı işaretle.

⚠️  Gelir tablosu KÜMÜLATİF: Q1 değerlerini yıllık gibi okuma.
    ROE, ROA için mutlaka period=12 (yıllık) değerlerini kullan.

⚠️  2OVA (Azınlık Payları) özkaynağa dahil: Rasyo hesabında
    "ana ortaklık özkaynak" = 2O - 2OVA kullanmak daha doğru.
    PD/DD ve ROE için bu ayrımı değerlendir.
```

---

## 11. SONRAKI ADIM: XI_29 ITEM CODE MAPPING

BIMAS veya başka bir XI_29 şirketi (sanayi/perakende) için aynı
endpoint'i çek, response'u kaydet. XI_29'da item code yapısı farklı:
  - Bilanço standart UFRS (dönen/duran varlık, kısa/uzun vadeli borç)
  - Gelir tablosu çeyreklik (kümülatif değil) → TTM = 4 çeyrek toplamı
  - item code'lar büyük ihtimalle farklı prefix/şema kullanır

Test şirketi önerileri:
  - BIMAS (Perakende, büyük/sağlıklı veri)
  - EREGL (Demir-Çelik, XI_29 sanayi)
  - TCELL (İletişim, XI_29 farklı sektör)
