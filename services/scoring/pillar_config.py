"""
Pillar Configuration Module
Defines pillar structures and ratio weights for different sectors

Pillars are category groups for financial ratios:
- Karlilik (Profitability): ROE, ROA, margins
- Finansal (Financial Health): Liquidity, leverage
- Verimlilik (Efficiency): Asset turnover
- Degerleme (Valuation): P/E, P/B (when data available)

Sector-specific configurations:
- XI_29 (Industrial): Default 4-pillar structure
- Bankacılık (Banking): CAMELS-lite structure
- Sigortacılık (Insurance): Technical performance focus
- GYO (REIT): NAV and rental yield focus
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class RatioWeight:
    """Weight configuration for a single ratio within a pillar"""
    ratio_code: str          # Database ratio code (e.g., 'gross_margin', 'roe')
    weight: float            # Weight within pillar (should sum to 1.0)
    higher_is_better: bool   # True = higher is good, False = lower is good
    required: bool = False   # If True, pillar cannot be calculated without this ratio
    
    def __post_init__(self):
        # Map Turkish ratio names to database codes if needed
        ratio_mapping = {
            "net_kar_marji": "net_margin",
            "favok_marji": "ebitda_margin",
            "fk_orani": "pe_ratio",
            "pd_dd": "pb_ratio",
            "fd_favok": "ev_ebitda",
            "cari_oran": "current_ratio",
            "asit_test_orani": "acid_test_ratio",
            "borclanma_orani": "debt_ratio",
            "net_borclanma_orani": "net_debt_to_equity",
            "nfm": "net_interest_margin",
            "kredi_mevduat_orani": "loan_to_deposit",
            "npl_orani": "npl_ratio",
            "sermaye_yeterlilik": "capital_adequacy",
            "bilesik_oran": "combined_ratio",
            "hasarprim_orani": "loss_ratio",
            "masraf_orani": "expense_ratio",
        }
        self.ratio_code = ratio_mapping.get(self.ratio_code, self.ratio_code)


@dataclass
class PillarConfig:
    """Configuration for a scoring pillar"""
    name: str                          # Pillar name (karlilik, finansal, etc.)
    weight: float                      # Weight in composite score (should sum to 1.0)
    ratios: List[RatioWeight]          # Ratios in this pillar
    min_ratios: int = 2                # Minimum ratios needed for pillar score
    description: str = ""              # Human-readable description


# ─────────────────────────────────────────────────────────────────────────────
# XI_29 SECTORS (Industrial, GYO, Energy, Retail, etc.)
# ─────────────────────────────────────────────────────────────────────────────

XI29_PILLARS: List[PillarConfig] = [
    
    PillarConfig(
        name="karlilik",
        weight=0.40,
        min_ratios=2,
        description="Kârlılık performansı",
        ratios=[
            RatioWeight("gross_margin",      weight=0.25, higher_is_better=True),
            RatioWeight("operating_margin",  weight=0.25, higher_is_better=True),
            RatioWeight("net_margin",        weight=0.20, higher_is_better=True),
            RatioWeight("ebitda_margin",     weight=0.15, higher_is_better=True),
            RatioWeight("roe",               weight=0.15, higher_is_better=True),
        ]
    ),
    
    PillarConfig(
        name="finansal",
        weight=0.35,
        min_ratios=2,
        description="Finansal sağlık ve likidite",
        ratios=[
            RatioWeight("current_ratio",       weight=0.30, higher_is_better=True),
            RatioWeight("acid_test_ratio",     weight=0.20, higher_is_better=True),
            RatioWeight("debt_ratio",          weight=0.25, higher_is_better=False),
            RatioWeight("net_debt_to_equity",  weight=0.25, higher_is_better=False),
        ]
    ),
    
    PillarConfig(
        name="verimlilik",
        weight=0.25,
        min_ratios=1,
        description="Aktif verimliliği",
        ratios=[
            RatioWeight("asset_turnover", weight=1.0, higher_is_better=True),
        ]
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# BANKING SECTORS (UFRS_K) - CAMELS-Lite
# ─────────────────────────────────────────────────────────────────────────────

BANKA_PILLARS: List[PillarConfig] = [
    
    PillarConfig(
        name="karlilik",
        weight=0.35,
        min_ratios=2,
        description="Kârlılık performansı",
        ratios=[
            RatioWeight("roe",                   weight=0.40, higher_is_better=True),
            RatioWeight("roa",                   weight=0.35, higher_is_better=True),
            RatioWeight("net_interest_margin",   weight=0.25, higher_is_better=True),
        ]
    ),
    
    PillarConfig(
        name="verimlilik",
        weight=0.25,
        min_ratios=1,
        description="Operasyonel verimlilik",
        ratios=[
            RatioWeight("cost_income_ratio", weight=1.0, higher_is_better=False),
        ]
    ),
    
    PillarConfig(
        name="varlik_kalitesi",
        weight=0.25,
        min_ratios=1,
        description="Kredi kalitesi",
        ratios=[
            RatioWeight("npl_ratio", weight=1.0, higher_is_better=False),
        ]
    ),
    
    PillarConfig(
        name="sermaye_likidite",
        weight=0.15,
        min_ratios=1,
        description="Sermaye yapısı",
        ratios=[
            RatioWeight("capital_adequacy", weight=0.60, higher_is_better=True),
            RatioWeight("loan_to_deposit",  weight=0.40, higher_is_better=False),
        ]
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# INSURANCE SECTORS (UFRS_S)
# ─────────────────────────────────────────────────────────────────────────────

SIGORTA_PILLARS: List[PillarConfig] = [
    
    PillarConfig(
        name="karlilik",
        weight=0.35,
        min_ratios=2,
        description="Kârlılık performansı",
        ratios=[
            RatioWeight("roe",         weight=0.45, higher_is_better=True),
            RatioWeight("net_margin",  weight=0.35, higher_is_better=True),
            RatioWeight("roa",         weight=0.20, higher_is_better=True),
        ]
    ),
    
    PillarConfig(
        name="teknik_performans",
        weight=0.40,
        min_ratios=2,
        description="Teknik kârlılık",
        ratios=[
            RatioWeight("combined_ratio", weight=0.45, higher_is_better=False),
            RatioWeight("loss_ratio",     weight=0.35, higher_is_better=False),
            RatioWeight("expense_ratio",  weight=0.20, higher_is_better=False),
        ]
    ),
    
    PillarConfig(
        name="degerleme",
        weight=0.25,
        min_ratios=1,
        description="Değerleme",
        ratios=[
            RatioWeight("pb_ratio", weight=1.0, higher_is_better=False),
        ]
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# GYO SECTORS (Real Estate Investment Trusts)
# ─────────────────────────────────────────────────────────────────────────────

GYO_PILLARS: List[PillarConfig] = [
    
    PillarConfig(
        name="karlilik",
        weight=0.40,
        min_ratios=2,
        description="Kârlılık performansı",
        ratios=[
            RatioWeight("gross_margin",     weight=0.30, higher_is_better=True),
            RatioWeight("operating_margin", weight=0.30, higher_is_better=True),
            RatioWeight("net_margin",       weight=0.25, higher_is_better=True),
            RatioWeight("roe",              weight=0.15, higher_is_better=True),
        ]
    ),
    
    PillarConfig(
        name="finansal",
        weight=0.35,
        min_ratios=1,
        description="Finansal yapı",
        ratios=[
            RatioWeight("debt_ratio",          weight=0.50, higher_is_better=False),
            RatioWeight("net_debt_to_equity",  weight=0.50, higher_is_better=False),
        ]
    ),
    
    PillarConfig(
        name="degerleme",
        weight=0.25,
        min_ratios=1,
        description="Değerleme",
        ratios=[
            RatioWeight("pb_ratio", weight=1.0, higher_is_better=False),
        ]
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# GENEL PILLARS (Cross-sector comparison for score_genel)
# ─────────────────────────────────────────────────────────────────────────────

GENEL_PILLARS: List[PillarConfig] = [
    
    PillarConfig(
        name="karlilik",
        weight=0.45,
        min_ratios=2,
        description="Kârlılık performansı",
        ratios=[
            RatioWeight("roe",         weight=0.50, higher_is_better=True),
            RatioWeight("roa",         weight=0.30, higher_is_better=True),
            RatioWeight("net_margin",  weight=0.20, higher_is_better=True),
        ]
    ),
    
    PillarConfig(
        name="finansal",
        weight=0.35,
        min_ratios=1,
        description="Finansal sağlık",
        ratios=[
            RatioWeight("debt_ratio",          weight=0.60, higher_is_better=False),
            RatioWeight("net_debt_to_equity",  weight=0.40, higher_is_better=False),
        ]
    ),
    
    PillarConfig(
        name="verimlilik",
        weight=0.20,
        min_ratios=1,
        description="Aktif verimliliği",
        ratios=[
            RatioWeight("asset_turnover", weight=1.0, higher_is_better=True),
        ]
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# SECTOR ROUTER
# ─────────────────────────────────────────────────────────────────────────────

PILLAR_CONFIG_MAP: Dict[str, List[PillarConfig]] = {
    "Bankacılık":           BANKA_PILLARS,
    "Bankacılık & Finans":  BANKA_PILLARS,
    "Sigortacılık":         SIGORTA_PILLARS,
    "GYO":                  GYO_PILLARS,
    "_default":             XI29_PILLARS,
}


def get_pillar_config(sector_main: str) -> List[PillarConfig]:
    """
    Get pillar configuration for a sector.
    
    Args:
        sector_main: Main sector name from companies table
    
    Returns:
        List of PillarConfig for the sector
    """
    return PILLAR_CONFIG_MAP.get(sector_main, PILLAR_CONFIG_MAP["_default"])


def get_all_ratio_codes(sector_main: str) -> List[str]:
    """
    Get all ratio codes needed for a sector's scoring.
    
    Args:
        sector_main: Main sector name
    
    Returns:
        List of unique ratio codes
    """
    pillar_configs = get_pillar_config(sector_main)
    ratio_codes = set()
    
    for pillar in pillar_configs:
        for ratio in pillar.ratios:
            ratio_codes.add(ratio.ratio_code)
    
    return list(ratio_codes)


def get_genel_ratio_codes() -> List[str]:
    """
    Get all ratio codes needed for score_genel calculation.
    
    Returns:
        List of unique ratio codes for general scoring
    """
    ratio_codes = set()
    
    for pillar in GENEL_PILLARS:
        for ratio in pillar.ratios:
            ratio_codes.add(ratio.ratio_code)
    
    return list(ratio_codes)


# Reliability dampening factors (imported by ratio_scorer)
RELIABILITY_DAMPENING = {
    "HIGH":         1.00,
    "MEDIUM":       0.80,
    "LOW":          0.55,
    "INSUFFICIENT": None,
}
