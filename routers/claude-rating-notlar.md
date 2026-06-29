# HissePro — Company Rating Sistemi
## OpenCode IDE Uygulama Talimatı (`/comp` servisi)

---

## 0. BAĞLAM — NEREDE DURUYORUZ

Bu dökümanı okumadan önce `mali_tablo_sistemi_talimat.md` dosyasını oku.
Mevcut sistem durumu:

```
✅ financial_statements_raw  → İş Yatırım'dan ham veri çekildi
✅ company_ratios            → Sektöre özgü rasyolar hesaplandı
✅ sector_medians            → 14 sektör için F1-F5 filtreli medyanlar hesaplandı
✅ sector_median_peers       → Audit trail mevcut

🔨 ŞİMDİ YAPILACAK:
   company_scores            → Her şirket için 0-100 puan sistemi
```

**Bu doküman:** `company_ratios` + `sector_medians` tablolarını input olarak alıp
`company_scores` tablosunu dolduran rating motorunu kuracak.

---

## 1. MİMARİ KARAR — İKİ AYRI SKOR

Tek skor yeterli değil. Her şirket için **iki bağımsız skor** üretilecek:

```
┌─────────────────────────────────────────────────────────────┐
│  SCORE_SEKTOR (0-100)                                       │
│  "Bu şirket kendi sektöründe nerede?"                      │
│  Peer grubu: aynı sektor_ana içindeki şirketler            │
│  Kullanım: Sektör içi karşılaştırma, sektör rotasyonu      │
├─────────────────────────────────────────────────────────────┤
│  SCORE_GENEL (0-100)                                        │
│  "Bu şirket tüm BIST'te nerede?"                           │
│  Peer grubu: Tüm aktif şirketler (cross-sector)            │
│  Kullanım: Genel tarama, farklı sektör karşılaştırması     │
└─────────────────────────────────────────────────────────────┘
```

**Önemli:** Sektöre özgü rasyolar (örn. banka NFM, sigorta hasar-prim oranı)
sadece `score_sektor` hesabına girer. `score_genel` sadece evrensel rasyoları kullanır
(ROE, ROA, F/K, PD/DD gibi — tüm sektörlerde hesaplanan ortak metrikler).

---

## 2. VERİTABANI ŞEMASI — YENİ TABLOLAR

`/comp` servisindeki mevcut `database.py` veya `models.py` dosyasına ekle:

```sql
-- ── Ana skor tablosu ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS company_scores (
    id                  BIGSERIAL PRIMARY KEY,
    kod                 TEXT NOT NULL REFERENCES companies(kod),
    period_key          TEXT NOT NULL,              -- '2026Q1', '2025Q4'

    -- Kompozit skorlar
    score_sektor        NUMERIC(5,2),               -- 0-100, sektör içi
    score_genel         NUMERIC(5,2),               -- 0-100, tüm BIST

    -- Pillar skorları (sektör normalize — score_sektor bileşenleri)
    score_karlilik      NUMERIC(5,2),               -- Kârlılık & Büyüme pillar
    score_degerleme     NUMERIC(5,2),               -- Değerleme pillar
    score_finansal      NUMERIC(5,2),               -- Finansal Sağlık pillar
    score_kalite        NUMERIC(5,2),               -- Kalite & İstikrar pillar

    -- Güvenilirlik
    reliability_sektor  TEXT CHECK (reliability_sektor IN ('HIGH','MEDIUM','LOW','INSUFFICIENT')),
    reliability_genel   TEXT CHECK (reliability_genel IN ('HIGH','MEDIUM','LOW','INSUFFICIENT')),
    n_peers_sektor      INTEGER,                    -- Kaç peer ile karşılaştırıldı
    n_peers_genel       INTEGER,

    -- Metadata
    computed_at         TIMESTAMPTZ DEFAULT NOW(),
    is_stale            BOOLEAN DEFAULT FALSE,

    UNIQUE(kod, period_key)
);

-- ── Ratio bazlı detay (açıklanabilirlik için) ──────────────────
CREATE TABLE IF NOT EXISTS company_score_details (
    id                  BIGSERIAL PRIMARY KEY,
    score_id            BIGINT NOT NULL REFERENCES company_scores(id) ON DELETE CASCADE,
    kod                 TEXT NOT NULL,
    period_key          TEXT NOT NULL,
    rasyo_kodu          TEXT NOT NULL,              -- 'net_kar_marji', 'roe' vb.
    rasyo_degeri        NUMERIC,                    -- Ham rasyo değeri
    peer_median         NUMERIC,                    -- Karşılaştırılan medyan
    peer_p25            NUMERIC,
    peer_p75            NUMERIC,
    ratio_score         NUMERIC(5,2),               -- Bu rasyonun 0-100 skoru
    pillar              TEXT NOT NULL,              -- 'karlilik','degerleme','finansal','kalite'
    scope               TEXT NOT NULL CHECK (scope IN ('sektor','genel')),
    higher_is_better    BOOLEAN NOT NULL,

    UNIQUE(score_id, rasyo_kodu, scope)
);

-- ── İndeksler ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_company_scores_kod ON company_scores(kod);
CREATE INDEX IF NOT EXISTS idx_company_scores_period ON company_scores(period_key);
CREATE INDEX IF NOT EXISTS idx_company_scores_sektor ON company_scores(score_sektor DESC);
CREATE INDEX IF NOT EXISTS idx_company_scores_genel ON company_scores(score_genel DESC);
CREATE INDEX IF NOT EXISTS idx_score_details_score_id ON company_score_details(score_id);
```

---

## 3. TEMEL ALGORİTMA — RATIO SKORU HESAPLAMA

### 3a. Sigmoid-Tabanlı Percentile Skoru

Her rasyo için peer grubuna göre 0-100 skoru üret.
Bu fonksiyon tüm hesaplamaların temelidir — doğru implement et.

```python
# scoring/ratio_scorer.py

import numpy as np
import math
from typing import Optional


def compute_ratio_score(
    value: float,
    peer_values: list[float],
    higher_is_better: bool = True,
    sigmoid_steepness: float = 0.8,
) -> Optional[float]:
    """
    Bir rasyonun peer grubundaki sigmoid-normalized skorunu hesapla (0-100).

    Mantık:
      1. Medyandan sapma hesapla (IQR ile normalize → outlier'a dayanıklı)
      2. Sigmoid fonksiyonu uygula → S-eğrisi, asimptotik 0/100
      3. Yön düzelt (borç oranı gibi "düşük = iyi" rasyolar için)

    Özellikler:
      - Medyanda olan şirket → her zaman 50 puan
      - Çok iyi şirket → 85-95 arası (100'e ulaşamaz — asimptotik)
      - Çok kötü şirket → 5-15 arası (0'a inemez — asimptotik)
      - 3'ten az peer → None döndür (güvenilmez)

    Args:
        value: Hedef şirketin rasyo değeri
        peer_values: Peer grubunun rasyo değerleri (target dahil veya hariç olabilir)
        higher_is_better: True = yüksek değer iyidir (ROE gibi)
                          False = düşük değer iyidir (borç oranı gibi)
        sigmoid_steepness: S-eğrisinin dikliliği (0.8 = dengeli)

    Returns:
        0.0-100.0 arası float, veya None (yetersiz peer)
    """
    if not peer_values or len(peer_values) < 3:
        return None

    if not math.isfinite(value):
        return None

    peer_arr = np.array([v for v in peer_values if math.isfinite(v)], dtype=float)

    if len(peer_arr) < 3:
        return None

    median = np.median(peer_arr)
    q25 = np.percentile(peer_arr, 25)
    q75 = np.percentile(peer_arr, 75)
    iqr = q75 - q25

    # IQR = 0 durumu: tüm peer'lar aynı değerde
    if iqr < 1e-10:
        return 50.0

    # Robust Z-score: IQR/1.3490 normal dağılıma göre std yaklaşımı
    # 0.7413 = 1 / (2 * 0.6745): IQR'ı std'ye çevirme faktörü
    robust_std = iqr / (2 * 0.6745)
    z = (value - median) / robust_std

    # Yön düzeltmesi
    if not higher_is_better:
        z = -z

    # Sigmoid dönüşümü: f(z) = 100 / (1 + e^(-k*z))
    score = 100.0 / (1.0 + math.exp(-sigmoid_steepness * z))

    return round(float(np.clip(score, 0.0, 100.0)), 2)
```

### 3b. Reliability Cezası

Sektör medyanı az şirketle hesaplandıysa (LOW/MEDIUM), skoru medyana doğru kısıt.
Bu kritik — 3 şirketlik bir sektörde "mükemmel" skor yanıltıcıdır.

```python
# scoring/ratio_scorer.py (devamı)

RELIABILITY_DAMPENING = {
    "HIGH":         1.00,   # Ceza yok (n >= 10)
    "MEDIUM":       0.80,   # %20 medyana yaklaştır (n: 5-9)
    "LOW":          0.55,   # %45 medyana yaklaştır (n: 3-4)
    "INSUFFICIENT": None,   # Bu rasyo için skor üretme
}


def apply_reliability_dampening(
    raw_score: float,
    reliability: str,
) -> Optional[float]:
    """
    Peer güvenilirliği düşükse skoru medyan (50) yönüne çek.

    Örnek: raw_score=80, reliability=LOW
      deviation = 80 - 50 = 30
      dampened  = 50 + (30 * 0.55) = 50 + 16.5 = 66.5
    """
    factor = RELIABILITY_DAMPENING.get(reliability)

    if factor is None:
        return None  # INSUFFICIENT → bu rasyo için skor yok

    deviation = raw_score - 50.0
    dampened = 50.0 + (deviation * factor)
    return round(float(np.clip(dampened, 0.0, 100.0)), 2)
```

---

## 4. PILLAR YAPISI VE AĞIRLIKLAR

### 4a. XI_29 (Sanayi, GYO, Enerji, Perakende, vb.) — Genel Sektörler

```python
# scoring/pillar_config.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class RatioWeight:
    rasyo_kodu: str
    weight: float           # Pillar içi ağırlık (toplamı 1.0 olmalı)
    higher_is_better: bool
    required: bool = False  # True = bu rasyo yoksa pillar hesaplanamaz


@dataclass
class PillarConfig:
    name: str
    weight: float           # Toplam skor içindeki pillar ağırlığı
    ratios: list[RatioWeight]
    min_ratios: int = 2     # En az kaç rasyo olursa pillar hesaplanır


# XI_29 sektörleri için pillar yapısı
XI29_PILLARS: list[PillarConfig] = [

    PillarConfig(
        name="karlilik",
        weight=0.30,        # Toplam skorun %30'u
        min_ratios=2,
        ratios=[
            RatioWeight("net_kar_marji",   weight=0.35, higher_is_better=True),
            RatioWeight("favok_marji",     weight=0.25, higher_is_better=True),
            RatioWeight("roe",             weight=0.25, higher_is_better=True),
            RatioWeight("roa",             weight=0.15, higher_is_better=True),
        ]
    ),

    PillarConfig(
        name="degerleme",
        weight=0.25,        # Toplam skorun %25'i
        min_ratios=2,
        ratios=[
            # Değerleme: düşük F/K, FD/FAVÖK, PD/DD daha iyidir
            RatioWeight("fk_orani",    weight=0.40, higher_is_better=False),
            RatioWeight("fd_favok",    weight=0.30, higher_is_better=False),
            RatioWeight("pd_dd",       weight=0.30, higher_is_better=False),
        ]
    ),

    PillarConfig(
        name="finansal",
        weight=0.25,        # Toplam skorun %25'i
        min_ratios=2,
        ratios=[
            RatioWeight("cari_oran",           weight=0.30, higher_is_better=True),
            # Net borçlanma: düşük (veya negatif = net nakit) daha iyi
            RatioWeight("net_borclanma_orani", weight=0.30, higher_is_better=False),
            RatioWeight("borclanma_orani",     weight=0.25, higher_is_better=False),
            RatioWeight("asit_test_orani",     weight=0.15, higher_is_better=True),
        ]
    ),

    PillarConfig(
        name="kalite",
        weight=0.20,        # Toplam skorun %20'si
        min_ratios=1,
        ratios=[
            RatioWeight("brut_kar_marji",  weight=0.50, higher_is_better=True),
            # favok_marji_istikrar = son 4 çeyrekte standart sapma (düşük = istikrarlı)
            RatioWeight("favok_marji_std", weight=0.30, higher_is_better=False),
            # gelir_buyume_std = gelir büyümesi volatilitesi
            RatioWeight("gelir_buyume_std",weight=0.20, higher_is_better=False),
        ]
    ),
]
```

### 4b. Bankacılık & Finans (UFRS_K) — CAMELS-Lite

```python
# scoring/pillar_config.py (devamı)

BANKA_PILLARS: list[PillarConfig] = [

    PillarConfig(
        name="karlilik",
        weight=0.30,
        min_ratios=2,
        ratios=[
            RatioWeight("roe",  weight=0.40, higher_is_better=True),
            RatioWeight("roa",  weight=0.35, higher_is_better=True),
            RatioWeight("nfm",  weight=0.25, higher_is_better=True),  # Net Faiz Marjı
        ]
    ),

    PillarConfig(
        name="verimlilik",  # Management Efficiency
        weight=0.25,
        min_ratios=1,
        ratios=[
            # Cost/Income: düşük = verimli
            RatioWeight("cost_income_ratio",     weight=0.55, higher_is_better=False),
            RatioWeight("komisyon_gelir_orani",  weight=0.45, higher_is_better=True),
        ]
    ),

    PillarConfig(
        name="varlik_kalitesi",  # Asset Quality
        weight=0.25,
        min_ratios=1,
        ratios=[
            RatioWeight("npl_orani",              weight=0.60, higher_is_better=False),
            RatioWeight("provision_gelir_orani",  weight=0.40, higher_is_better=False),
        ]
    ),

    PillarConfig(
        name="sermaye_likidite",  # Capital & Liquidity
        weight=0.20,
        min_ratios=1,
        ratios=[
            RatioWeight("sermaye_yeterlilik",   weight=0.50, higher_is_better=True),
            # Kredi/Mevduat: çok yüksekse likidite riski
            RatioWeight("kredi_mevduat_orani",  weight=0.50, higher_is_better=False),
        ]
    ),
]
```

### 4c. Sigortacılık (UFRS_S)

```python
SIGORTA_PILLARS: list[PillarConfig] = [

    PillarConfig(
        name="karlilik",
        weight=0.35,
        min_ratios=2,
        ratios=[
            RatioWeight("roe",             weight=0.45, higher_is_better=True),
            RatioWeight("net_kar_marji",   weight=0.35, higher_is_better=True),
            RatioWeight("roa",             weight=0.20, higher_is_better=True),
        ]
    ),

    PillarConfig(
        name="teknik_performans",
        weight=0.40,
        min_ratios=2,
        ratios=[
            # Bileşik oran = hasar + masraf. Düşük = teknik kâr var
            RatioWeight("bilesik_oran",     weight=0.45, higher_is_better=False),
            RatioWeight("hasarprim_orani",  weight=0.35, higher_is_better=False),
            RatioWeight("masraf_orani",     weight=0.20, higher_is_better=False),
        ]
    ),

    PillarConfig(
        name="degerleme",
        weight=0.25,
        min_ratios=1,
        ratios=[
            RatioWeight("fk_orani",  weight=0.55, higher_is_better=False),
            RatioWeight("pd_dd",     weight=0.45, higher_is_better=False),
        ]
    ),
]
```

### 4d. Pillar Config Router

```python
# scoring/pillar_config.py (devamı)

PILLAR_CONFIG_MAP: dict[str, list[PillarConfig]] = {
    "Bankacılık & Finans":          BANKA_PILLARS,
    "Sigortacılık":                 SIGORTA_PILLARS,
    # Diğer tüm sektörler XI29 varsayılanını kullanır:
    "_default":                     XI29_PILLARS,
}

# score_genel için evrensel rasyolar (sektör bağımsız)
# Sadece tüm sektörlerde hesaplanan rasyolar buraya girer
GENEL_PILLARS: list[PillarConfig] = [

    PillarConfig(
        name="karlilik",
        weight=0.35,
        min_ratios=2,
        ratios=[
            RatioWeight("roe",           weight=0.50, higher_is_better=True),
            RatioWeight("roa",           weight=0.30, higher_is_better=True),
            RatioWeight("net_kar_marji", weight=0.20, higher_is_better=True),
        ]
    ),

    PillarConfig(
        name="degerleme",
        weight=0.35,
        min_ratios=1,
        ratios=[
            RatioWeight("fk_orani",  weight=0.45, higher_is_better=False),
            RatioWeight("pd_dd",     weight=0.35, higher_is_better=False),
            RatioWeight("fd_favok",  weight=0.20, higher_is_better=False),
        ]
    ),

    PillarConfig(
        name="finansal",
        weight=0.30,
        min_ratios=1,
        ratios=[
            # Bankalar için borçlanma oranı farklı anlam taşır
            # Bu nedenle genel pillar'da ağırlığı düşük
            RatioWeight("net_borclanma_orani", weight=0.60, higher_is_better=False),
            RatioWeight("borclanma_orani",     weight=0.40, higher_is_better=False),
        ]
    ),
]


def get_pillar_config(sektor_ana: str) -> list[PillarConfig]:
    return PILLAR_CONFIG_MAP.get(sektor_ana, PILLAR_CONFIG_MAP["_default"])
```

---

## 5. ANA SCORING ENGINE

```python
# scoring/engine.py

import math
import numpy as np
from dataclasses import dataclass
from typing import Optional
from .ratio_scorer import compute_ratio_score, apply_reliability_dampening
from .pillar_config import (
    PillarConfig, RatioWeight,
    get_pillar_config, GENEL_PILLARS,
    RELIABILITY_DAMPENING
)


@dataclass
class RatioScoreDetail:
    rasyo_kodu: str
    rasyo_degeri: Optional[float]
    peer_median: Optional[float]
    peer_p25: Optional[float]
    peer_p75: Optional[float]
    ratio_score: Optional[float]        # Dampening uygulanmış final skor
    ratio_score_raw: Optional[float]    # Ham skor (debug için)
    pillar: str
    scope: str                          # 'sektor' | 'genel'
    higher_is_better: bool
    reliability: Optional[str]


@dataclass
class PillarScoreResult:
    pillar_name: str
    pillar_score: Optional[float]       # Ağırlıklı ortalama, 0-100
    pillar_weight: float
    n_ratios_available: int
    n_ratios_total: int
    ratio_details: list[RatioScoreDetail]


@dataclass
class CompanyScoreResult:
    kod: str
    period_key: str
    score_sektor: Optional[float]
    score_genel: Optional[float]
    pillar_scores: list[PillarScoreResult]  # score_sektor bileşenleri
    reliability_sektor: str
    reliability_genel: str
    n_peers_sektor: int
    n_peers_genel: int
    score_details: list[RatioScoreDetail]   # Tüm detaylar (DB'ye yazılacak)


def compute_pillar_score(
    pillar: PillarConfig,
    company_ratios: dict[str, float],           # {rasyo_kodu: değer}
    peer_ratio_values: dict[str, list[float]],  # {rasyo_kodu: [peer değerleri]}
    median_data: dict[str, dict],               # {rasyo_kodu: {median_ew, p25, p75, reliability}}
    scope: str,
) -> PillarScoreResult:
    """
    Tek bir pillar için ağırlıklı ortalama skor hesapla.

    Ağırlık normalizasyonu: Mevcut rasyoların ağırlıkları
    normalize edilir → eksik rasyo durumunda kalan rasyolar
    orantılı ağırlık alır.
    """
    ratio_details = []
    weighted_scores = []
    total_available_weight = 0.0

    for ratio_cfg in pillar.ratios:
        rk = ratio_cfg.rasyo_kodu
        value = company_ratios.get(rk)

        # Peer verisini al
        peers = peer_ratio_values.get(rk, [])
        med_info = median_data.get(rk, {})
        reliability = med_info.get("reliability", "INSUFFICIENT")

        detail = RatioScoreDetail(
            rasyo_kodu=rk,
            rasyo_degeri=value,
            peer_median=med_info.get("median_ew"),
            peer_p25=med_info.get("p25"),
            peer_p75=med_info.get("p75"),
            ratio_score=None,
            ratio_score_raw=None,
            pillar=pillar.name,
            scope=scope,
            higher_is_better=ratio_cfg.higher_is_better,
            reliability=reliability,
        )

        if value is None or not math.isfinite(value) or len(peers) < 3:
            ratio_details.append(detail)
            continue

        # Ham skor
        raw_score = compute_ratio_score(
            value=value,
            peer_values=peers,
            higher_is_better=ratio_cfg.higher_is_better,
        )

        if raw_score is None:
            ratio_details.append(detail)
            continue

        # Reliability dampening uygula
        final_score = apply_reliability_dampening(raw_score, reliability)

        detail.ratio_score_raw = raw_score
        detail.ratio_score = final_score
        ratio_details.append(detail)

        if final_score is not None:
            weighted_scores.append((final_score, ratio_cfg.weight))
            total_available_weight += ratio_cfg.weight

    # Minimum rasyo kontrolü
    n_available = sum(1 for d in ratio_details if d.ratio_score is not None)

    if n_available < pillar.min_ratios:
        return PillarScoreResult(
            pillar_name=pillar.name,
            pillar_score=None,
            pillar_weight=pillar.weight,
            n_ratios_available=n_available,
            n_ratios_total=len(pillar.ratios),
            ratio_details=ratio_details,
        )

    # Normalize ağırlıklar ile ağırlıklı ortalama
    if total_available_weight == 0:
        pillar_score = None
    else:
        pillar_score = sum(
            score * (w / total_available_weight)
            for score, w in weighted_scores
        )
        pillar_score = round(pillar_score, 2)

    return PillarScoreResult(
        pillar_name=pillar.name,
        pillar_score=pillar_score,
        pillar_weight=pillar.weight,
        n_ratios_available=n_available,
        n_ratios_total=len(pillar.ratios),
        ratio_details=ratio_details,
    )


def compute_composite_score(
    pillar_results: list[PillarScoreResult],
) -> tuple[Optional[float], str]:
    """
    Pillar sonuçlarından composite skor ve reliability üret.

    Returns: (composite_score, reliability_label)
    """
    weighted_scores = []
    total_available_weight = 0.0
    n_pillars_ok = 0

    for pr in pillar_results:
        if pr.pillar_score is not None:
            weighted_scores.append((pr.pillar_score, pr.pillar_weight))
            total_available_weight += pr.pillar_weight
            n_pillars_ok += 1

    total_pillars = len(pillar_results)

    # Pillar coverage → reliability
    coverage = n_pillars_ok / total_pillars if total_pillars > 0 else 0
    if coverage >= 0.875:       # 7/8 veya 4/4 pillar mevcut
        reliability = "HIGH"
    elif coverage >= 0.625:     # 5/8 veya 3/4 pillar mevcut
        reliability = "MEDIUM"
    elif coverage >= 0.375:     # 3/8 veya 2/4 pillar mevcut
        reliability = "LOW"
    else:
        reliability = "INSUFFICIENT"

    if total_available_weight < 0.50 or n_pillars_ok == 0:
        return None, "INSUFFICIENT"

    composite = sum(
        score * (w / total_available_weight)
        for score, w in weighted_scores
    )

    return round(composite, 2), reliability


def compute_company_score(
    kod: str,
    period_key: str,
    sektor_ana: str,
    # Şirketin tüm rasyoları
    company_ratios: dict[str, float],
    # Sektör peer'larının rasyo değerleri (key = rasyo_kodu)
    sektor_peer_values: dict[str, list[float]],
    sektor_median_data: dict[str, dict],
    n_peers_sektor: int,
    # Tüm BIST peer'larının rasyo değerleri (genel için)
    genel_peer_values: dict[str, list[float]],
    genel_median_data: dict[str, dict],
    n_peers_genel: int,
) -> CompanyScoreResult:
    """
    Bir şirket için hem sektör hem genel skoru hesapla.
    """
    sektor_pillar_cfgs = get_pillar_config(sektor_ana)

    # ── SEKTÖR SKORU ──────────────────────────────────────────────
    sektor_pillar_results = []
    for pillar_cfg in sektor_pillar_cfgs:
        result = compute_pillar_score(
            pillar=pillar_cfg,
            company_ratios=company_ratios,
            peer_ratio_values=sektor_peer_values,
            median_data=sektor_median_data,
            scope="sektor",
        )
        sektor_pillar_results.append(result)

    score_sektor, reliability_sektor = compute_composite_score(sektor_pillar_results)

    # ── GENEL SKOR ────────────────────────────────────────────────
    genel_pillar_results = []
    for pillar_cfg in GENEL_PILLARS:
        result = compute_pillar_score(
            pillar=pillar_cfg,
            company_ratios=company_ratios,
            peer_ratio_values=genel_peer_values,
            median_data=genel_median_data,
            scope="genel",
        )
        genel_pillar_results.append(result)

    score_genel, reliability_genel = compute_composite_score(genel_pillar_results)

    # Tüm detayları birleştir
    all_details = []
    for pr in sektor_pillar_results + genel_pillar_results:
        all_details.extend(pr.ratio_details)

    # Pillar skorlarını sözlüğe dönüştür (DB yazımı için)
    pillar_score_map = {
        pr.pillar_name: pr.pillar_score
        for pr in sektor_pillar_results
    }

    return CompanyScoreResult(
        kod=kod,
        period_key=period_key,
        score_sektor=score_sektor,
        score_genel=score_genel,
        pillar_scores=sektor_pillar_results,
        reliability_sektor=reliability_sektor,
        reliability_genel=reliability_genel,
        n_peers_sektor=n_peers_sektor,
        n_peers_genel=n_peers_genel,
        score_details=all_details,
    )
```

---

## 6. VERİ HAZIRLAMA — DB'DEN PEER DEĞERLERİ ÇEKME

```python
# scoring/data_loader.py

from typing import Optional
import asyncpg  # veya projenin mevcut DB kütüphanesi


async def load_peer_ratio_values(
    db,
    sektor_ana: str,
    rasyo_kodlari: list[str],
    period_key: str,
    scope: str = "sektor",   # 'sektor' | 'genel'
) -> tuple[dict[str, list[float]], dict[str, dict], int]:
    """
    Peer grubunun rasyo değerlerini ve medyan bilgisini yükle.

    Returns:
        peer_values:  {rasyo_kodu: [float, ...]}
        median_data:  {rasyo_kodu: {median_ew, p25, p75, reliability, n_peers}}
        n_peers:      Grupta kaç şirket var
    """
    if scope == "sektor":
        # Sektör içi peer'lar
        where_clause = "c.sektor_ana = $1"
        params_base = [sektor_ana]
    else:
        # Tüm BIST (genel)
        where_clause = "1=1"
        params_base = []

    # Tüm peer rasyolarını çek
    param_offset = len(params_base)
    rasyo_placeholder = ", ".join(
        f"${i+param_offset+1}" for i in range(len(rasyo_kodlari))
    )

    query = f"""
        SELECT cr.kod, cr.rasyo_kodu, cr.rasyo_degeri
        FROM company_ratios cr
        JOIN companies c ON cr.kod = c.kod
        WHERE {where_clause}
          AND cr.rasyo_kodu IN ({rasyo_placeholder})
          AND cr.period_key = ${param_offset + len(rasyo_kodlari) + 1}
          AND c.is_active = TRUE
          AND cr.rasyo_degeri IS NOT NULL
    """
    rows = await db.fetch(query, *params_base, *rasyo_kodlari, period_key)

    # Rasyo bazında grupla
    peer_values: dict[str, list[float]] = {rk: [] for rk in rasyo_kodlari}
    peer_kods: set[str] = set()
    for row in rows:
        peer_values[row["rasyo_kodu"]].append(float(row["rasyo_degeri"]))
        peer_kods.add(row["kod"])

    n_peers = len(peer_kods)

    # Medyan verisini çek (sector_medians tablosundan)
    if scope == "sektor":
        med_rows = await db.fetch("""
            SELECT rasyo_kodu, median_ew, p25, p75, reliability, n_peers
            FROM sector_medians
            WHERE sektor_ana = $1
              AND rasyo_kodu = ANY($2::text[])
              AND period_key = $3
              AND is_stale = FALSE
        """, sektor_ana, rasyo_kodlari, period_key)
    else:
        # Genel için global medyan tablosu — yoksa peer_values'dan hesapla
        # global_medians tablosu Bölüm 8'de tanımlanacak
        med_rows = await db.fetch("""
            SELECT rasyo_kodu, median_ew, p25, p75, reliability, n_peers
            FROM global_medians
            WHERE rasyo_kodu = ANY($1::text[])
              AND period_key = $2
              AND is_stale = FALSE
        """, rasyo_kodlari, period_key)

    median_data: dict[str, dict] = {}
    for row in med_rows:
        median_data[row["rasyo_kodu"]] = {
            "median_ew":   float(row["median_ew"]) if row["median_ew"] else None,
            "p25":         float(row["p25"]) if row["p25"] else None,
            "p75":         float(row["p75"]) if row["p75"] else None,
            "reliability": row["reliability"],
            "n_peers":     row["n_peers"],
        }

    return peer_values, median_data, n_peers
```

---

## 7. WORKER — BATCH SCORING

APScheduler veya FastAPI background task olarak çalıştır.
Mevcut scheduler yapısına entegre et (APScheduler zaten kuruluysa ona ekle).

```python
# scoring/worker.py

import asyncio
import logging
from datetime import date
from .engine import compute_company_score, CompanyScoreResult
from .data_loader import load_peer_ratio_values
from .pillar_config import get_pillar_config, GENEL_PILLARS

logger = logging.getLogger(__name__)


async def run_scoring_for_period(db, period_key: str) -> dict:
    """
    Belirtilen dönem için tüm aktif şirketlerin skorunu hesapla.
    Bu fonksiyon scheduler tarafından çağrılır.

    Tetiklenme zamanı:
      - company_ratios tablosuna yeni veri yazıldığında (event-driven)
      - Pazar 05:00 (haftalık tam geçiş, scheduler Layer 2)
      - Admin UI manuel tetikleme
    """
    logger.info(f"Scoring başlıyor: period_key={period_key}")

    # Tüm aktif şirketleri sektörüyle çek
    companies = await db.fetch("""
        SELECT kod, sektor_ana, financial_group
        FROM companies
        WHERE is_active = TRUE
        ORDER BY sektor_ana, kod
    """)

    # Tüm BIST rasyolarını tek sorguda çek (N+1 önlemi)
    genel_rasyo_kodlari = ["roe", "roa", "net_kar_marji", "fk_orani", "pd_dd",
                           "fd_favok", "net_borclanma_orani", "borclanma_orani"]

    all_company_ratios = await db.fetch("""
        SELECT kod, rasyo_kodu, rasyo_degeri
        FROM company_ratios
        WHERE period_key = $1
    """, period_key)

    # Şirket bazında rasyo sözlüğü oluştur
    company_ratio_map: dict[str, dict[str, float]] = {}
    for row in all_company_ratios:
        if row["kod"] not in company_ratio_map:
            company_ratio_map[row["kod"]] = {}
        if row["rasyo_degeri"] is not None:
            company_ratio_map[row["kod"]][row["rasyo_kodu"]] = float(row["rasyo_degeri"])

    # Genel (BIST geneli) peer değerlerini yükle — bir kez
    genel_peer_values, genel_median_data, n_peers_genel = await load_peer_ratio_values(
        db=db,
        sektor_ana=None,
        rasyo_kodlari=genel_rasyo_kodlari,
        period_key=period_key,
        scope="genel",
    )

    results = []
    errors = []

    # Sektör bazında grupla → her sektör için peer verisi bir kez çekilir
    sektörler = {}
    for c in companies:
        sektörler.setdefault(c["sektor_ana"], []).append(c)

    for sektor_ana, sektor_companies in sektörler.items():
        # Bu sektörün pillar config'inden gereken rasyo kodlarını topla
        pillar_cfgs = get_pillar_config(sektor_ana)
        sektor_rasyo_kodlari = list({
            r.rasyo_kodu
            for p in pillar_cfgs
            for r in p.ratios
        })

        # Sektör peer değerlerini yükle
        sektor_peer_values, sektor_median_data, n_peers_sektor = \
            await load_peer_ratio_values(
                db=db,
                sektor_ana=sektor_ana,
                rasyo_kodlari=sektor_rasyo_kodlari,
                period_key=period_key,
                scope="sektor",
            )

        for company in sektor_companies:
            kod = company["kod"]
            company_ratios = company_ratio_map.get(kod, {})

            try:
                result = compute_company_score(
                    kod=kod,
                    period_key=period_key,
                    sektor_ana=sektor_ana,
                    company_ratios=company_ratios,
                    sektor_peer_values=sektor_peer_values,
                    sektor_median_data=sektor_median_data,
                    n_peers_sektor=n_peers_sektor,
                    genel_peer_values=genel_peer_values,
                    genel_median_data=genel_median_data,
                    n_peers_genel=n_peers_genel,
                )
                results.append(result)

            except Exception as e:
                logger.error(f"Scoring hatası: kod={kod}, error={e}")
                errors.append({"kod": kod, "error": str(e)})

    # DB'ye toplu yaz
    await _upsert_scores_batch(db, results, period_key)

    logger.info(
        f"Scoring tamamlandı: {len(results)} şirket, "
        f"{len(errors)} hata, period={period_key}"
    )
    return {"success": len(results), "errors": len(errors), "details": errors}


async def _upsert_scores_batch(db, results: list[CompanyScoreResult], period_key: str):
    """
    Tüm sonuçları tek transaction içinde DB'ye yaz.
    """
    async with db.transaction():
        for r in results:
            # Pillar skorlarını çıkar
            pillar_map = {pr.pillar_name: pr.pillar_score for pr in r.pillar_scores}

            # company_scores upsert
            score_id = await db.fetchval("""
                INSERT INTO company_scores (
                    kod, period_key,
                    score_sektor, score_genel,
                    score_karlilik, score_degerleme,
                    score_finansal, score_kalite,
                    reliability_sektor, reliability_genel,
                    n_peers_sektor, n_peers_genel,
                    is_stale, computed_at
                ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,FALSE,NOW())
                ON CONFLICT (kod, period_key) DO UPDATE SET
                    score_sektor       = EXCLUDED.score_sektor,
                    score_genel        = EXCLUDED.score_genel,
                    score_karlilik     = EXCLUDED.score_karlilik,
                    score_degerleme    = EXCLUDED.score_degerleme,
                    score_finansal     = EXCLUDED.score_finansal,
                    score_kalite       = EXCLUDED.score_kalite,
                    reliability_sektor = EXCLUDED.reliability_sektor,
                    reliability_genel  = EXCLUDED.reliability_genel,
                    n_peers_sektor     = EXCLUDED.n_peers_sektor,
                    n_peers_genel      = EXCLUDED.n_peers_genel,
                    is_stale           = FALSE,
                    computed_at        = NOW()
                RETURNING id
            """,
                r.kod, r.period_key,
                r.score_sektor, r.score_genel,
                pillar_map.get("karlilik"),
                pillar_map.get("degerleme"),
                pillar_map.get("finansal"),
                pillar_map.get("kalite"),
                r.reliability_sektor, r.reliability_genel,
                r.n_peers_sektor, r.n_peers_genel,
            )

            # company_score_details upsert (mevcut detayları sil, yeniden yaz)
            await db.execute(
                "DELETE FROM company_score_details WHERE score_id = $1", score_id
            )

            if r.score_details:
                await db.executemany("""
                    INSERT INTO company_score_details (
                        score_id, kod, period_key, rasyo_kodu,
                        rasyo_degeri, peer_median, peer_p25, peer_p75,
                        ratio_score, pillar, scope, higher_is_better
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
                """, [
                    (
                        score_id, r.kod, r.period_key, d.rasyo_kodu,
                        d.rasyo_degeri, d.peer_median, d.peer_p25, d.peer_p75,
                        d.ratio_score, d.pillar, d.scope, d.higher_is_better
                    )
                    for d in r.score_details
                    if d.ratio_score is not None
                ])
```

---

## 8. GLOBAL MEDIAN TABLOSU (score_genel için)

`score_genel` hesabı tüm BIST'teki şirketlerle karşılaştırma yapar.
Bu karşılaştırma için sektör ayrımı olmayan global medyanlar gerekli.

```sql
-- global_medians: Tüm BIST için sektör bağımsız medyanlar
CREATE TABLE IF NOT EXISTS global_medians (
    id              BIGSERIAL PRIMARY KEY,
    rasyo_kodu      TEXT NOT NULL,
    period_key      TEXT NOT NULL,
    median_ew       NUMERIC,
    p25             NUMERIC,
    p75             NUMERIC,
    n_peers         INTEGER NOT NULL,
    reliability     TEXT CHECK (reliability IN ('HIGH','MEDIUM','LOW','INSUFFICIENT')),
    computed_at     TIMESTAMPTZ DEFAULT NOW(),
    is_stale        BOOLEAN DEFAULT FALSE,
    UNIQUE(rasyo_kodu, period_key)
);
```

```python
# scoring/global_median_worker.py

async def compute_global_medians(db, period_key: str):
    """
    Tüm BIST'teki şirketler için global medyanları hesapla.
    sector_medians tablosuna yazmak yerine global_medians'a yazar.
    
    Çağrılma zamanı: run_scoring_for_period çağrılmadan önce.
    """
    import numpy as np

    GLOBAL_RASYO_KODLARI = [
        "roe", "roa", "net_kar_marji", "favok_marji",
        "fk_orani", "pd_dd", "fd_favok",
        "net_borclanma_orani", "borclanma_orani",
    ]

    for rasyo_kodu in GLOBAL_RASYO_KODLARI:
        rows = await db.fetch("""
            SELECT cr.rasyo_degeri
            FROM company_ratios cr
            JOIN companies c ON cr.kod = c.kod
            WHERE cr.rasyo_kodu = $1
              AND cr.period_key = $2
              AND c.is_active = TRUE
              AND cr.rasyo_degeri IS NOT NULL
        """, rasyo_kodu, period_key)

        values = [float(r["rasyo_degeri"]) for r in rows]
        n = len(values)

        if n < 3:
            reliability = "INSUFFICIENT"
            median_ew = p25 = p75 = None
        else:
            arr = np.array(values)
            median_ew = float(np.median(arr))
            p25 = float(np.percentile(arr, 25))
            p75 = float(np.percentile(arr, 75))
            reliability = (
                "HIGH"   if n >= 30 else
                "MEDIUM" if n >= 15 else
                "LOW"    if n >= 5  else
                "INSUFFICIENT"
            )

        await db.execute("""
            INSERT INTO global_medians
                (rasyo_kodu, period_key, median_ew, p25, p75, n_peers, reliability, is_stale)
            VALUES ($1,$2,$3,$4,$5,$6,$7,FALSE)
            ON CONFLICT (rasyo_kodu, period_key) DO UPDATE SET
                median_ew=$3, p25=$4, p75=$5, n_peers=$6,
                reliability=$7, computed_at=NOW(), is_stale=FALSE
        """, rasyo_kodu, period_key, median_ew, p25, p75, n, reliability)
```

---

## 9. FASTAPI ENDPOINT'LERİ

Mevcut `/comp` servisine ekle. Router yapısını koru.

```python
# routers/scores.py

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from typing import Optional
from ..scoring.worker import run_scoring_for_period
from ..scoring.global_median_worker import compute_global_medians

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/{kod}")
async def get_company_score(
    kod: str,
    period_key: Optional[str] = Query(None, description="Örn: 2026Q1. Boş = en güncel"),
    db=Depends(get_db),
):
    """
    Bir şirketin rating skorunu döndür.
    
    Response içerir:
    - score_sektor, score_genel (0-100)
    - score_karlilik, score_degerleme, score_finansal, score_kalite
    - Harf notu (A+, A, B+, ...)
    - n_peers, reliability
    """
    if period_key is None:
        # En güncel dönemi bul
        period_key = await db.fetchval("""
            SELECT period_key FROM company_scores
            WHERE kod = $1 AND is_stale = FALSE
            ORDER BY computed_at DESC LIMIT 1
        """, kod)
        if period_key is None:
            raise HTTPException(404, f"{kod} için henüz skor hesaplanmamış")

    row = await db.fetchrow("""
        SELECT * FROM company_scores
        WHERE kod = $1 AND period_key = $2
    """, kod, period_key)

    if not row:
        raise HTTPException(404, "Skor bulunamadı")

    return {
        "kod": kod,
        "period_key": period_key,
        "score_sektor": row["score_sektor"],
        "score_genel": row["score_genel"],
        "grade_sektor": _score_to_grade(row["score_sektor"]),
        "grade_genel": _score_to_grade(row["score_genel"]),
        "pillars": {
            "karlilik":  row["score_karlilik"],
            "degerleme": row["score_degerleme"],
            "finansal":  row["score_finansal"],
            "kalite":    row["score_kalite"],
        },
        "meta": {
            "reliability_sektor": row["reliability_sektor"],
            "reliability_genel":  row["reliability_genel"],
            "n_peers_sektor":     row["n_peers_sektor"],
            "n_peers_genel":      row["n_peers_genel"],
            "computed_at":        row["computed_at"],
        }
    }


@router.get("/{kod}/details")
async def get_score_details(
    kod: str,
    period_key: Optional[str] = Query(None),
    scope: str = Query("sektor", regex="^(sektor|genel)$"),
    db=Depends(get_db),
):
    """
    Ratio bazlı detay skorları döndür.
    AI servisine context sağlamak için kullanılır.
    """
    if period_key is None:
        period_key = await db.fetchval("""
            SELECT period_key FROM company_scores
            WHERE kod = $1 ORDER BY computed_at DESC LIMIT 1
        """, kod)

    score_id = await db.fetchval("""
        SELECT id FROM company_scores WHERE kod = $1 AND period_key = $2
    """, kod, period_key)

    if not score_id:
        raise HTTPException(404, "Skor bulunamadı")

    details = await db.fetch("""
        SELECT rasyo_kodu, rasyo_degeri, peer_median, peer_p25, peer_p75,
               ratio_score, pillar, higher_is_better
        FROM company_score_details
        WHERE score_id = $1 AND scope = $2
        ORDER BY pillar, ratio_score DESC NULLS LAST
    """, score_id, scope)

    return {
        "kod": kod,
        "period_key": period_key,
        "scope": scope,
        "details": [dict(d) for d in details]
    }


@router.get("/sector/{sektor_ana}/ranking")
async def get_sector_ranking(
    sektor_ana: str,
    period_key: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db=Depends(get_db),
):
    """
    Sektördeki şirketleri score_sektor'a göre sırala.
    """
    if period_key is None:
        period_key = await db.fetchval("""
            SELECT period_key FROM company_scores cs
            JOIN companies c ON cs.kod = c.kod
            WHERE c.sektor_ana = $1
            ORDER BY cs.computed_at DESC LIMIT 1
        """, sektor_ana)

    rows = await db.fetch("""
        SELECT cs.kod, c.hisse_adi,
               cs.score_sektor, cs.score_genel,
               cs.reliability_sektor, cs.n_peers_sektor
        FROM company_scores cs
        JOIN companies c ON cs.kod = c.kod
        WHERE c.sektor_ana = $1
          AND cs.period_key = $2
          AND cs.is_stale = FALSE
        ORDER BY cs.score_sektor DESC NULLS LAST
        LIMIT $3
    """, sektor_ana, period_key, limit)

    return {
        "sektor_ana": sektor_ana,
        "period_key": period_key,
        "ranking": [
            {
                "rank": i + 1,
                "kod": r["kod"],
                "hisse_adi": r["hisse_adi"],
                "score_sektor": r["score_sektor"],
                "score_genel": r["score_genel"],
                "grade": _score_to_grade(r["score_sektor"]),
                "reliability": r["reliability_sektor"],
            }
            for i, r in enumerate(rows)
        ]
    }


@router.post("/compute/{period_key}")
async def trigger_scoring(
    period_key: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    # Admin auth buraya ekle (mevcut auth sisteminle)
):
    """
    Manuel skor hesaplama tetikleme (Admin UI için).
    Background task olarak çalışır, anında 202 döner.
    """
    async def _run():
        await compute_global_medians(db, period_key)
        await run_scoring_for_period(db, period_key)

    background_tasks.add_task(_run)
    return {"status": "accepted", "period_key": period_key, "message": "Scoring başlatıldı"}


def _score_to_grade(score: Optional[float]) -> Optional[str]:
    """0-100 skoru harf notuna çevir."""
    if score is None:
        return None
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B+"
    if score >= 60: return "B"
    if score >= 50: return "C+"
    if score >= 40: return "C"
    return "D"
```

---

## 10. DOSYA YAPISI

`/comp` servisine şu yapıda ekle:

```
/comp
├── scoring/
│   ├── __init__.py
│   ├── ratio_scorer.py          ← Bölüm 3: compute_ratio_score, apply_reliability_dampening
│   ├── pillar_config.py         ← Bölüm 4: XI29_PILLARS, BANKA_PILLARS, get_pillar_config
│   ├── engine.py                ← Bölüm 5: compute_company_score
│   ├── data_loader.py           ← Bölüm 6: load_peer_ratio_values
│   ├── worker.py                ← Bölüm 7: run_scoring_for_period
│   └── global_median_worker.py  ← Bölüm 8: compute_global_medians
├── routers/
│   └── scores.py                ← Bölüm 9: FastAPI endpoints
└── migrations/
    └── 004_company_scores.sql   ← Bölüm 2: CREATE TABLE ifadeleri
```

---

## 11. SCHEDULER ENTEGRASYONU

Mevcut APScheduler yapısına ekle. `main.py` veya `scheduler.py` dosyasında:

```python
# Mevcut scheduler setup'ına ekle

from scoring.worker import run_scoring_for_period
from scoring.global_median_worker import compute_global_medians
from utils.period_utils import get_current_period_key  # mevcut yardımcı fonksiyon

# Pazar 05:00 — company_ratios güncellendikten 1 saat sonra
scheduler.add_job(
    func=_run_scoring_pipeline,
    trigger="cron",
    day_of_week="sun",
    hour=5,
    minute=0,
    id="weekly_scoring",
    replace_existing=True,
)

# Event-driven tetikleme: company_ratios tablosuna yeni veri yazılınca
# Redis pub/sub veya mevcut async queue sisteminden çağır:
async def on_ratios_updated(period_key: str):
    """
    company_ratios worker tamamlanınca bu fonksiyon çağrılır.
    Zaten mevcut invalidation pipeline'ına ekle.
    """
    await compute_global_medians(db, period_key)
    await run_scoring_for_period(db, period_key)

async def _run_scoring_pipeline():
    period_key = get_current_period_key()
    db = await get_db_connection()
    await compute_global_medians(db, period_key)
    await run_scoring_for_period(db, period_key)
```

---

## 12. KALİTE & İSTİKRAR PILLAR — EK HESAPLAMALAR

`favok_marji_std` ve `gelir_buyume_std` standart company_ratios tablosunda yok.
Bunları ayrı hesapla ve company_ratios'a `rasyo_kodu` olarak ekle:

```python
# Bu hesaplamayı company_ratios worker'ına ekle (mevcut ratio hesaplama kodunda)

async def compute_stability_metrics(db, kod: str, period_key: str):
    """
    Son 4 çeyrekte FAVÖK marjı ve gelir büyümesi standart sapmasını hesapla.
    Bunlar "kalite" pillar'ı için gerekli.
    """
    import numpy as np

    # Son 4 dönemi çek
    rows = await db.fetch("""
        SELECT period_key, rasyo_degeri
        FROM company_ratios
        WHERE kod = $1
          AND rasyo_kodu = 'favok_marji'
        ORDER BY period_key DESC
        LIMIT 4
    """, kod)

    if len(rows) >= 3:
        values = [float(r["rasyo_degeri"]) for r in rows if r["rasyo_degeri"]]
        std = float(np.std(values)) if len(values) >= 2 else None

        if std is not None:
            await db.execute("""
                INSERT INTO company_ratios (kod, period_key, rasyo_kodu, rasyo_degeri)
                VALUES ($1, $2, 'favok_marji_std', $3)
                ON CONFLICT (kod, period_key, rasyo_kodu) DO UPDATE
                SET rasyo_degeri = EXCLUDED.rasyo_degeri, computed_at = NOW()
            """, kod, period_key, std)

    # Gelir büyümesi volatilitesi
    gelir_rows = await db.fetch("""
        SELECT period_key, rasyo_degeri
        FROM company_ratios
        WHERE kod = $1
          AND rasyo_kodu = 'net_satislar_buyume'
        ORDER BY period_key DESC
        LIMIT 4
    """, kod)

    if len(gelir_rows) >= 3:
        values = [float(r["rasyo_degeri"]) for r in gelir_rows if r["rasyo_degeri"]]
        std = float(np.std(values)) if len(values) >= 2 else None

        if std is not None:
            await db.execute("""
                INSERT INTO company_ratios (kod, period_key, rasyo_kodu, rasyo_degeri)
                VALUES ($1, $2, 'gelir_buyume_std', $3)
                ON CONFLICT (kod, period_key, rasyo_kodu) DO UPDATE
                SET rasyo_degeri = EXCLUDED.rasyo_degeri, computed_at = NOW()
            """, kod, period_key, std)
```

---

## 13. KRİTİK UYARILAR — UYGULAMA ÖNCESİ OKU

```
⚠️  1. GYO'DA CARİ ORAN YOK
    GYO sektöründe cari_oran ve asit_test_orani hesaplanmaz.
    Mevcut F3 filtresi RASYO_SEKTOR_UYUMSUZ döndürdüğünde bu rasyolar
    company_ratios tablosuna NULL olarak girer. Skorlama motoru
    None değeri gördüğünde bu rasyoyu otomatik atlar — sorun yok.

⚠️  2. BANKA GELIR TABLOSU KÜMÜLATIF
    Bankalar için TTM hesabında period=12 (yıllık) değeri kullanılır.
    Q1/Q2/Q3 dönemleri için v2 (önceki yıl sonu) alınır.
    Bu kuralı ihlal etme — yanlış TTM bankacılık pillar'ını bozar.

⚠️  3. NEGATİF F/K MEDYANDAN ZATEN ÇIKMIŞ
    F3 filtresi fk_orani için min=0.0 sınırı koyuyor.
    Zarar eden şirketler (negatif F/K) sector_medians'a dahil değil.
    Negatif F/K'lı şirkete skor hesaplanırken peer_values listesinde
    negatif değer olmaz — kontrol etme gerek yok, sistem doğal koru.

⚠️  4. SCORE_GENEL CROSS-SECTOR KARŞILAŞTIRMA
    GYO'nun F/K'sı ile Teknoloji şirketinin F/K'sı farklı aralıklarda.
    Bu nedenle score_genel economic_bounds dışı değerleri içerebilir.
    F3 filtresi sector_medians için uygulanıyor ama global_medians
    için AYNI F3 mantığını uygula (global_median_worker'da).

⚠️  5. PEER COUNT EŞİKLERİ
    Global medyan için n >= 30 = HIGH tercih edildi (sektörden farklı).
    BIST'te 500+ aktif şirket var — genel rasyolarda HIGH bekle.
    Sektör medyanında ise sector_medians.reliability alanını kullan.

⚠️  6. VALKEY/REDIS CACHING
    company_scores tablosu günde 1 kez güncellenir.
    API endpoint'lerini Valkey'e cache'le (TTL: 4 saat).
    Cache key: f"company_score:{kod}:{period_key}"
    company_ratios güncellenince bu cache'i invalidate et.

⚠️  7. TEKNİK ANALİZ SKORU İLE BİRLEŞTİRME — HENÜZ DEĞİL
    Bu sistem sadece temel analiz skorunu üretir.
    Teknik analiz skoru ayrı bir tablo/sistem olacak.
    Birleştirme (composite score) her iki sistem olgunlaşınca yapılacak.
    Şimdi bu iki skoru birleştirmeye çalışma.
```

---

## 14. DOĞRULAMA — GARAN REF DEĞERLERI

Sistem kurulduktan sonra GARAN 2025Q4 (yıllık) dönem ile test et:

```
Beklenen girdi rasyoları (company_ratios tablosundan):
  roe:               0.264  (26.4%)
  roa:               0.0255 (2.55%)
  kredi_mevduat_orani: 0.874 (87.4%)
  cost_income_ratio: 0.261  (26.1%)

Beklenen davranış:
  ROE = 26.4% → Bankacılık sektöründe yüksek → score_sektor yüksek olmalı
  Cost/Income = 26.1% → Çok verimli (sektör ortalaması ~40%) → yüksek skor

Kontrol et:
  1. compute_ratio_score(0.264, peer_values, higher_is_better=True) > 70 olmalı
  2. Banka pillar "karlilik" skoru 65+ olmalı
  3. Banka pillar "verimlilik" skoru 75+ olmalı (26.1% cost/income sektörde üst çeyrek)
  4. score_sektor'un en az 65+ olması beklenir
```

---

## 15. UYGULAMA SIRASI

```
Adım 1: migrations/004_company_scores.sql çalıştır
         → company_scores ve company_score_details tabloları oluşur

Adım 2: scoring/ klasörünü oluştur
         → ratio_scorer.py, pillar_config.py, engine.py

Adım 3: data_loader.py yaz
         → Mevcut DB bağlantı yapısını kullan (projedeki asyncpg/databases setup)

Adım 4: global_median_worker.py yaz ve çalıştır (2025Q4 için)
         → global_medians tablosunu doldur

Adım 5: worker.py yaz ve 2025Q4 için manuel tetikle
         → company_scores tablosunu doldur

Adım 6: routers/scores.py ekle, main.py'e router'ı kaydet

Adım 7: GARAN 2025Q4 ile Bölüm 14 doğrulamasını yap

Adım 8: Scheduler'a entegre et (haftalık + event-driven)
```