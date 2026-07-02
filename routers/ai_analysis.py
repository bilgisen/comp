"""
AI Analysis Router
Generates CEO-level analysis reports with tiered access control

Tiered Access:
- Anonymous: Basic score cards only
- Member: 1-paragraph summary + enhanced cards
- Subscriber: Full SWOT + detailed report + ultimate cards
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from enum import Enum

from core.database import get_db

router = APIRouter(prefix="/ai", tags=["ai-analysis"])


# ─────────────────────────────────────────────────────────────────────────────
# ENUMS AND MODELS
# ─────────────────────────────────────────────────────────────────────────────

class UserTier(str, Enum):
    ANONYMOUS = "anonymous"
    MEMBER = "member"
    SUBSCRIBER = "subscriber"


class AnalysisCardType(str, Enum):
    SCORE_CARD = "score_card"
    RATIO_COMPARISON = "ratio_comparison"
    TREND_CHART = "trend_chart"
    PEER_COMPARISON = "peer_comparison"
    SWOT = "swot"
    SECTOR_POSITION = "sector_position"
    FINANCIAL_HEALTH = "financial_health"


# ─────────────────────────────────────────────────────────────────────────────
# PYDANTIC RESPONSE MODELS
# ─────────────────────────────────────────────────────────────────────────────

class ScoreCard(BaseModel):
    """Temel Analiz Puan Kartı"""
    score_sektor: Optional[float]
    score_genel: Optional[float]
    score_karlilik: Optional[float]
    score_finansal: Optional[float]
    score_verimlilik: Optional[float]
    score_degerleme: Optional[float]
    reliability: Optional[str]
    percentile_sector: Optional[int]
    rank_sector: Optional[int]
    total_peers: Optional[int]


class RatioComparisonCard(BaseModel):
    """Rasyo Kıyaslama Kartı"""
    ratio_name: str
    ratio_code: str
    company_value: Optional[float]
    sector_median: Optional[float]
    sector_p25: Optional[float]
    sector_p75: Optional[float]
    percentile: Optional[int]
    interpretation: Optional[str]


class TrendData(BaseModel):
    """Trend Verisi"""
    period: str
    value: Optional[float]
    score: Optional[float]


class TrendChartCard(BaseModel):
    """Trend Grafik Kartı"""
    ratio_code: str
    ratio_name: str
    trend: List[TrendData]
    trend_direction: Optional[str]
    volatility: Optional[float]


class SWOTItem(BaseModel):
    item: str
    impact: str  # high, medium, low
    source: str  # which ratio/metric


class SWOTCard(BaseModel):
    """SWOT Analiz Kartı"""
    strengths: List[SWOTItem]
    weaknesses: List[SWOTItem]
    opportunities: List[SWOTItem]
    threats: List[SWOTItem]
    overall_assessment: Optional[str]


class PeerComparisonCard(BaseModel):
    """Sektör Kıyaslama Kartı"""
    ticker: str
    name: str
    score: Optional[float]
    key_ratios: Dict[str, Optional[float]]
    position: int


class SectorPositionCard(BaseModel):
    """Sektör İçi Pozisyon"""
    sector_name: str
    total_companies: int
    rank: int
    percentile: float
    above_median_ratios: List[str]
    below_median_ratios: List[str]


class FinancialHealthCard(BaseModel):
    """Finansal Sağlık Kartı"""
    overall_health: str  # excellent, good, fair, poor
    liquidity_score: Optional[float]
    leverage_score: Optional[float]
    profitability_score: Optional[float]
    efficiency_score: Optional[float]
    alerts: List[str]
    recommendations: List[str]


class AnalysisSummary(BaseModel):
    """Analiz Özeti (Member tier)"""
    summary: str
    key_strengths: List[str]
    key_concerns: List[str]
    investment_thesis: Optional[str]


class DetailedReport(BaseModel):
    """Detaylı Rapor (Subscriber tier)"""
    executive_summary: str
    financial_position: str
    profitability_analysis: str
    balance_sheet_analysis: str
    sector_comparison: str
    swot_analysis: SWOTCard
    catalysts: List[str]
    risks: List[str]
    conclusion: str
    disclaimer: str


class TieredAnalysisResponse(BaseModel):
    """Tiered response based on user level"""
    tier: UserTier
    ticker: str
    company_name: str
    sector: str
    
    # Cards based on tier
    cards: List[Dict[str, Any]]
    
    # Analysis based on tier
    summary: Optional[AnalysisSummary] = None
    detailed_report: Optional[DetailedReport] = None
    
    # Metadata
    period_key: str
    computed_at: datetime
    data_quality: str


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_user_tier(authorization: Optional[str]) -> UserTier:
    """Determine user tier from authorization header
    
    Supports multiple formats:
    - Bearer subscriber_token (legacy)
    - Bearer member_token (legacy)  
    - Bearer <jwt_token> with X-User-Tier header
    - Direct tier header: X-User-Tier: pro/ultimate/standard/free
    """
    if not authorization:
        return UserTier.ANONYMOUS
    
    # Check for explicit tier header (from Hono orchestrator)
    # This is set by the frontend via Hono proxy
    
    # Legacy token format check
    if "subscriber_" in authorization or "ultimate" in authorization or "pro" in authorization:
        return UserTier.SUBSCRIBER
    elif "member_" in authorization or "standard" in authorization or "free" in authorization:
        return UserTier.MEMBER
    
    return UserTier.ANONYMOUS


def get_user_tier_from_headers(authorization: Optional[str], user_tier_header: Optional[str] = None) -> UserTier:
    """Get user tier from headers - supports both auth token and explicit tier header"""
    
    # Priority 1: Explicit tier header from orchestrator
    if user_tier_header:
        tier_map = {
            "ultimate": UserTier.SUBSCRIBER,
            "pro": UserTier.SUBSCRIBER,
            "subscriber": UserTier.SUBSCRIBER,
            "standard": UserTier.MEMBER,
            "free": UserTier.MEMBER,
            "member": UserTier.MEMBER,
        }
        return tier_map.get(user_tier_header.lower(), UserTier.ANONYMOUS)
    
    # Priority 2: Auth token parsing
    return get_user_tier(authorization)


def calculate_percentile(value: float, peer_values: List[float]) -> int:
    """Calculate percentile of value within peer group"""
    if not peer_values or len(peer_values) < 2:
        return 50
    
    below = sum(1 for v in peer_values if v < value)
    return int((below / len(peer_values)) * 100)


def interpret_ratio(ratio_code: str, company_value: float, sector_median: float) -> str:
    """Generate interpretation for ratio comparison"""
    diff_pct = ((company_value - sector_median) / abs(sector_median)) * 100 if sector_median else 0
    
    interpretations = {
        "roe": f"Özkaynak kârlılığı sektör ortalamasına göre %{abs(diff_pct):.1f} {'üstünde' if diff_pct > 0 else 'altında'}.",
        "roa": f"Aktif kârlılığı sektör ortalamasından {'daha yüksek' if diff_pct > 0 else 'daha düşük'}.",
        "current_ratio": f"Likidite pozisyonu {'güçlü' if company_value > sector_median else 'zayıf'}.",
        "debt_ratio": f"Borçlanma seviyesi sektör ortalamasına göre {'düşük' if company_value < sector_median else 'yüksek'}.",
        "gross_margin": f"Brüt kâr marjı {'sektör lideri düzeyinde' if diff_pct > 20 else 'sektör ortalaması civarında'}.",
        "net_margin": f"Net kâr marjı {'rekabetçi' if company_value > sector_median else 'geliştirilmeye açık'}.",
    }
    
    return interpretations.get(ratio_code, f"Sektör medianına göre %{diff_pct:.1f} fark.")


# ─────────────────────────────────────────────────────────────────────────────
# CARD GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

def generate_score_card(db, ticker: str, period_key: str) -> Optional[ScoreCard]:
    """Generate score card for a company"""
    result = db.execute(text("""
        SELECT 
            cs.score_sektor, cs.score_genel,
            cs.score_karlilik, cs.score_finansal, cs.score_verimlilik, cs.score_degerleme,
            cs.reliability_sektor, cs.n_peers_sektor,
            c.sector_main
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.ticker = :ticker AND cs.period_key = :period_key
    """), {"ticker": ticker, "period_key": period_key}).fetchone()
    
    if not result:
        return None
    
    # Calculate rank using RANK() window function (consistent with leaderboard)
    rank_result = db.execute(text("""
        SELECT sector_rank, total_companies
        FROM (
            SELECT
                cs.ticker,
                RANK() OVER (
                    PARTITION BY c.sector_main
                    ORDER BY cs.score_sektor DESC NULLS LAST
                ) as sector_rank,
                COUNT(*) OVER (PARTITION BY c.sector_main) as total_companies
            FROM company_scores cs
            JOIN companies c ON cs.ticker = c.ticker
            WHERE c.sector_main = :sector
              AND cs.period_key = :period_key
        ) ranked
        WHERE ticker = :ticker
    """), {
        "sector": result.sector_main,
        "period_key": period_key,
        "ticker": ticker,
    }).fetchone()
    
    rank = rank_result.sector_rank if rank_result else 1
    total = rank_result.total_companies if rank_result else 1
    percentile = int(100 - (rank / max(total, 1)) * 100)
    
    return ScoreCard(
        score_sektor=float(result.score_sektor) if result.score_sektor else None,
        score_genel=float(result.score_genel) if result.score_genel else None,
        score_karlilik=float(result.score_karlilik) if result.score_karlilik else None,
        score_finansal=float(result.score_finansal) if result.score_finansal else None,
        score_verimlilik=float(result.score_verimlilik) if result.score_verimlilik else None,
        score_degerleme=float(result.score_degerleme) if result.score_degerleme else None,
        reliability=result.reliability_sektor,
        percentile_sector=percentile,
        rank_sector=rank,
        total_peers=total
    )


def generate_ratio_comparison_cards(
    db, 
    ticker: str, 
    period_key: str,
    tier: UserTier
) -> List[RatioComparisonCard]:
    """Generate ratio comparison cards"""
    
    # Define key ratios based on tier - only using ratios that exist in company_ratios table
    if tier == UserTier.ANONYMOUS:
        key_ratios = ["roe", "current_ratio", "debt_ratio"]
    elif tier == UserTier.MEMBER:
        key_ratios = ["roe", "roa", "current_ratio", "debt_ratio", "gross_margin", "net_margin"]
    else:  # SUBSCRIBER
        key_ratios = ["roe", "roa", "current_ratio", "acid_test_ratio", "debt_ratio", 
                      "net_debt_to_equity", "gross_margin", "operating_margin", "net_margin", 
                      "ebitda_margin", "asset_turnover"]
    
    cards = []
    
    for ratio_code in key_ratios:
        result = db.execute(text("""
            SELECT 
                cr.ratio_value,
                sb.median_ew, sb.p25, sb.p75,
                cr.ratio_code
            FROM company_ratios cr
            LEFT JOIN sector_benchmarks sb 
                ON sb.ratio_code = cr.ratio_code 
                AND sb.sector_main = (SELECT sector_main FROM companies WHERE ticker = :ticker)
                AND sb.period_key = cr.period_key
            WHERE cr.ticker = :ticker 
              AND cr.ratio_code = :ratio_code
              AND cr.period_key = :period_key
        """), {"ticker": ticker, "ratio_code": ratio_code, "period_key": period_key}).fetchone()
        
        if result and result.ratio_value:
            ratio_names = {
                "roe": "Özkaynak Kârlılığı (ROE)",
                "roa": "Aktif Kârlılığı (ROA)",
                "current_ratio": "Cari Oran",
                "acid_test_ratio": "Asit Test Oranı",
                "debt_ratio": "Borçlanma Oranı",
                "net_debt_to_equity": "Net Borç / Özkaynak",
                "gross_margin": "Brüt Kâr Marjı",
                "operating_margin": "Faaliyet Kâr Marjı",
                "net_margin": "Net Kâr Marjı",
                "ebitda_margin": "FAVÖK Marjı",
                "asset_turnover": "Aktif Devir Hızı"
            }
            
            company_val = float(result.ratio_value)
            median_val = float(result.median_ew) if result.median_ew else None
            
            cards.append(RatioComparisonCard(
                ratio_name=ratio_names.get(ratio_code, ratio_code),
                ratio_code=ratio_code,
                company_value=company_val,
                sector_median=median_val,
                sector_p25=float(result.p25) if result.p25 else None,
                sector_p75=float(result.p75) if result.p75 else None,
                percentile=calculate_percentile(company_val, []) if median_val else 50,
                interpretation=interpret_ratio(ratio_code, company_val, median_val) if median_val else None
            ))
    
    return cards


def generate_swot_card(db, ticker: str, period_key: str) -> SWOTCard:
    """Generate SWOT analysis card based on actual ratio data and sector comparisons."""
    
    # Get company ratios with sector comparisons
    ratios = db.execute(text("""
        SELECT 
            cr.ratio_code, cr.ratio_value,
            sb.median_ew as sector_median,
            sb.p25, sb.p75,
            CASE 
                WHEN cr.ratio_value IS NULL THEN NULL
                WHEN sb.median_ew IS NULL THEN NULL
                WHEN cr.ratio_value > sb.p75 THEN 'above_high'
                WHEN cr.ratio_value > sb.median_ew THEN 'above_median'
                WHEN cr.ratio_value > sb.p25 THEN 'below_median'
                ELSE 'below_low'
            END as position
        FROM company_ratios cr
        LEFT JOIN companies c ON cr.ticker = c.ticker
        LEFT JOIN sector_benchmarks sb 
            ON sb.ratio_code = cr.ratio_code 
            AND sb.sector_main = c.sector_main
            AND sb.period_key = cr.period_key
        WHERE cr.ticker = :ticker AND cr.period_key = :period_key
          AND cr.ratio_value IS NOT NULL
    """), {"ticker": ticker, "period_key": period_key}).fetchall()
    
    # Get company scores
    scores = db.execute(text("""
        SELECT score_sektor, score_karlilik, score_finansal, score_verimlilik, score_degerleme
        FROM company_scores
        WHERE ticker = :ticker AND period_key = :period_key
    """), {"ticker": ticker, "period_key": period_key}).fetchone()
    
    strengths = []
    weaknesses = []
    opportunities = []
    threats = []
    
    # Ratio-specific analysis maps
    RATIO_LABELS = {
        "roe": "Özkaynak kârlılığı (ROE)",
        "roa": "Aktif kârlılığı (ROA)",
        "gross_margin": "Brüt kâr marjı",
        "net_margin": "Net kâr marjı",
        "operating_margin": "Operasyonel marj",
        "ebitda_margin": "FAVÖK marjı",
        "current_ratio": "Cari oran",
        "acid_test_ratio": "Asit test oranı",
        "debt_ratio": "Borçlanma oranı",
        "debt_to_equity": "Borç/Özsermaye",
        "net_debt_to_equity": "Net borç/Özsermaye",
        "asset_turnover": "Aktif devir hızı",
        "cost_income_ratio": "Maliyet/Gelir oranı",
        "loan_to_deposit": "Kredi/Mevduat oranı",
        "npl_ratio": "Takipteki kredi oranı",
        "capital_adequacy": "Sermaye yeterlilik oranı",
        "net_interest_margin": "Net faiz marjı",
    }
    
    # Map ratios to SWOT categories
    STRENGTH_RATIOS = {
        "roe", "roa", "gross_margin", "net_margin", "operating_margin", "ebitda_margin",
        "current_ratio", "acid_test_ratio", "asset_turnover", "net_interest_margin", "capital_adequacy"
    }
    WEAKNESS_RATIOS = {"debt_ratio", "debt_to_equity", "net_debt_to_equity", "npl_ratio"}
    
    for row in ratios:
        label = RATIO_LABELS.get(row.ratio_code, row.ratio_code)
        pos = row.position
        val = float(row.ratio_value) if row.ratio_value else None
        med = float(row.sector_median) if row.sector_median else None
        
        if pos is None or val is None:
            continue
        
        # Strengths: significantly above sector median (top quartile)
        if pos == "above_high" and row.ratio_code in STRENGTH_RATIOS:
            diff_pct = ((val - med) / abs(med) * 100) if med and med != 0 else 0
            if diff_pct > 20:
                impacts = "high"
                item = f"{label} sektör ortalamasının显著 üzerinde (%{diff_pct:.0f} выше)"
            else:
                impacts = "medium"
                item = f"{label} sektör üst çeyreğinde"
            strengths.append(SWOTItem(item=item, impact=impacts, source=row.ratio_code))
        
        # Weaknesses: significantly below sector median (bottom quartile)
        elif pos == "below_low" and row.ratio_code in WEAKNESS_RATIOS:
            diff_pct = ((med - val) / abs(med) * 100) if med and med != 0 else 0
            if diff_pct > 20:
                impacts = "high"
                item = f"{label} sektör ortalamasının belirgin şekilde altında"
            else:
                impacts = "medium"
                item = f"{label} sektör alt çeyreğinde"
            weaknesses.append(SWOTItem(item=item, impact=impacts, source=row.ratio_code))
        
        elif pos == "below_low" and row.ratio_code in STRENGTH_RATIOS:
            # A normally-good ratio is below median = weakness
            weaknesses.append(SWOTItem(
                item=f"{label} sektör ortalamasının altında",
                impact="medium",
                source=row.ratio_code
            ))
        
        elif pos == "above_high" and row.ratio_code in WEAKNESS_RATIOS:
            # A normally-bad ratio is above median = concern
            weaknesses.append(SWOTItem(
                item=f"{label} sektör ortalamasının üzerinde (risk)",
                impact="medium",
                source=row.ratio_code
            ))
    
    # Score-based analysis
    if scores:
        if scores.score_karlilik and float(scores.score_karlilik) > 70:
            strengths.append(SWOTItem(
                item="Güçlü kârlılık performansı (sektör üst çeyreği)",
                impact="high", source="score_karlilik"
            ))
        elif scores.score_karlilik and float(scores.score_karlilik) < 40:
            weaknesses.append(SWOTItem(
                item="Kârlılık performansı sektör ortalamasının altında",
                impact="high", source="score_karlilik"
            ))
    
    # Sector-specific opportunities and threats based on ratio patterns
    ratio_codes = {r.ratio_code for r in ratios}
    above_count = sum(1 for r in ratios if r.position in ("above_high", "above_median"))
    below_count = sum(1 for r in ratios if r.position in ("below_low", "below_median"))
    total = len(ratios) if ratios else 1
    
    if above_count > total * 0.6:
        opportunities.append(SWOTItem(
            item="Çoğunlukla sektörün üzerinde performans — büyüme potansiyeli güçlü",
            impact="high", source="sector_pattern"
        ))
    elif below_count > total * 0.6:
        threats.append(SWOTItem(
            item="Çoğunlukla sektörün altında performans — iyileşme gereksinimi var",
            impact="high", source="sector_pattern"
        ))
    
    # Liquidity/leverage specific
    if "current_ratio" in ratio_codes:
        cr_row = next((r for r in ratios if r.ratio_code == "current_ratio"), None)
        if cr_row and cr_row.position == "above_high":
            opportunities.append(SWOTItem(
                item="Güçlü likidite pozisyonu — büyüme yatırımları için kaynak mevcut",
                impact="medium", source="current_ratio"
            ))
        elif cr_row and cr_row.position == "below_low":
            threats.append(SWOTItem(
                item="Düşük likidite — kısa vadeli borç ödeme kapasitesi risk altında",
                impact="high", source="current_ratio"
            ))
    
    if "debt_ratio" in ratio_codes:
        dr_row = next((r for r in ratios if r.ratio_code == "debt_ratio"), None)
        if dr_row and dr_row.position == "below_low":
            opportunities.append(SWOTItem(
                item="Düşük borçlanma — finansal esneklik yüksek",
                impact="medium", source="debt_ratio"
            ))
        elif dr_row and dr_row.position == "above_high":
            threats.append(SWOTItem(
                item="Yüksek borçlanma — faiz artışı riski",
                impact="high", source="debt_ratio"
            ))
    
    if "npl_ratio" in ratio_codes:
        npl_row = next((r for r in ratios if r.ratio_code == "npl_ratio"), None)
        if npl_row and float(npl_row.ratio_value or 0) > 0.05:
            threats.append(SWOTItem(
                item=f"Takipteki kredi oranı yüksek (%{float(npl_row.ratio_value)*100:.1f})",
                impact="high", source="npl_ratio"
            ))
        elif npl_row and float(npl_row.ratio_value or 0) < 0.02:
            strengths.append(SWOTItem(
                item="Kredi kalitesi güçlü — düşük takipteki kredi oranı",
                impact="medium", source="npl_ratio"
            ))
    
    # Ensure at least some items
    if not strengths:
        strengths.append(SWOTItem(item="Sektördeki konumunu koruyor", impact="low", source="general"))
    if not weaknesses:
        weaknesses.append(SWOTItem(item="Belirgin zayıf yön tespit edilemedi", impact="low", source="general"))
    if not opportunities:
        opportunities.append(SWOTItem(item="Sektör dinamiklerine göre konumunu değerlendirilmeli", impact="low", source="general"))
    if not threats:
        threats.append(SWOTItem(item="Piyasa koşullarına dikkat edilmeli", impact="low", source="general"))
    
    return SWOTCard(
        strengths=strengths[:5],
        weaknesses=weaknesses[:5],
        opportunities=opportunities[:5],
        threats=threats[:5],
        overall_assessment=None
    )


def generate_sector_position_card(db, ticker: str, period_key: str) -> Optional[SectorPositionCard]:
    """Generate sector position card"""
    
    result = db.execute(text("""
        SELECT sector_name, score_sektor, sector_rank, total_companies
        FROM (
            SELECT
                c.sector_main as sector_name,
                cs.score_sektor,
                RANK() OVER (
                    PARTITION BY c.sector_main
                    ORDER BY cs.score_sektor DESC NULLS LAST
                ) as sector_rank,
                COUNT(*) OVER (PARTITION BY c.sector_main) as total_companies,
                cs.ticker
            FROM company_scores cs
            JOIN companies c ON cs.ticker = c.ticker
            WHERE cs.period_key = :period_key
              AND cs.score_sektor IS NOT NULL
        ) ranked
        WHERE ticker = :ticker
    """), {"ticker": ticker, "period_key": period_key}).fetchone()
    
    if not result:
        return None
    
    # Get ratio performance
    ratio_perf = db.execute(text("""
        SELECT 
            cr.ratio_code,
            CASE WHEN cr.ratio_value > sb.median_ew THEN 'above' ELSE 'below' END as position
        FROM company_ratios cr
        JOIN sector_benchmarks sb 
            ON sb.ratio_code = cr.ratio_code 
            AND sb.sector_main = :sector
            AND sb.period_key = cr.period_key
        WHERE cr.ticker = :ticker AND cr.period_key = :period_key
    """), {"ticker": ticker, "sector": result.sector_main, "period_key": period_key}).fetchall()
    
    above_median = [r.ratio_code for r in ratio_perf if r.position == 'above']
    below_median = [r.ratio_code for r in ratio_perf if r.position == 'below']
    
    rank = int(result.sector_rank) if result.sector_rank else 1
    total = int(result.total_companies) if result.total_companies else 1
    percentile = int(100 - (rank / max(total, 1)) * 100)

    return SectorPositionCard(
        sector_name=result.sector_name,
        total_companies=total,
        rank=rank,
        percentile=percentile,
        above_median_ratios=above_median,
        below_median_ratios=below_median
    )


# ─────────────────────────────────────────────────────────────────────────────
# AI ANALYSIS GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

async def generate_member_summary(
    ticker: str,
    company_name: str,
    sector: str,
    score_card: ScoreCard,
    ratio_cards: List[RatioComparisonCard]
) -> AnalysisSummary:
    """Generate member-level summary based on actual ratio data."""
    
    score_val = score_card.score_sektor if score_card and score_card.score_sektor else None
    karlilik_val = score_card.score_karlilik if score_card and score_card.score_karlilik else None
    percentile = score_card.percentile_sector if score_card else None
    
    # Build summary from actual data
    if score_val:
        if score_val > 70:
            perf = "güçlü"
        elif score_val > 50:
            perf = "ortalamanın üzerinde"
        elif score_val > 30:
            perf = "ortalama"
        else:
            perf = "zayıf"
        
        summary_text = f"{company_name} ({ticker}), {sector} sektöründe {perf} bir performans sergiliyor. "
        summary_text += f"Temel analiz puanı {score_val:.1f}/100."
        
        if percentile:
            summary_text += f" Sektör içinde %{percentile:.0f} percentilde yer alıyor."
    else:
        summary_text = f"{company_name} ({ticker}), {sector} sektöründe faaliyet gösteriyor. Temel analiz verileri hesaplanıyor."
    
    # Key strengths from actual ratio data
    key_strengths = []
    top_ratios = sorted(
        [r for r in ratio_cards if r.percentile is not None],
        key=lambda x: x.percentile or 0,
        reverse=True
    )[:5]
    
    for r in top_ratios[:3]:
        if r.percentile and r.percentile > 60:
            key_strengths.append(r.ratio_name)
    
    if not key_strengths:
        key_strengths = ["Sektör içi genel konum"]
    
    # Key concerns from actual ratio data
    key_concerns = []
    weak_ratios = sorted(
        [r for r in ratio_cards if r.percentile is not None],
        key=lambda x: x.percentile or 0
    )[:5]
    
    for r in weak_ratios[:3]:
        if r.percentile and r.percentile < 40:
            key_concerns.append(r.ratio_name)
    
    if not key_concerns:
        key_concerns = ["Belirgin risk alanı tespit edilmedi"]
    
    return AnalysisSummary(
        summary=summary_text,
        key_strengths=key_strengths,
        key_concerns=key_concerns,
        investment_thesis=None
    )


async def generate_subscriber_report(
    ticker: str,
    company_name: str,
    sector: str,
    score_card: ScoreCard,
    ratio_cards: List[RatioComparisonCard],
    swot_card: SWOTCard,
    sector_position: SectorPositionCard
) -> DetailedReport:
    """Generate subscriber-level detailed report based on actual ratio data."""
    
    score_val = score_card.score_sektor if score_card and score_card.score_sektor else None
    karlilik_val = score_card.score_karlilik if score_card and score_card.score_karlilik else None
    
    # ── Executive Summary ──────────────────────────────────────────────
    if score_val and sector_position:
        rank_text = f"sektöründe {sector_position.rank}. sırada"
        perc_text = f"%{sector_position.percentile:.0f} percentilde"
        exec_summary = f"{company_name} ({ticker}), {sector} sektöründe {rank_text}, {perc_text} yer alıyor. "
        exec_summary += f"Temel analiz puanı: {score_val:.1f}/100."
        
        if karlilik_val:
            exec_summary += f" Kârlılık skoru: {karlilik_val:.1f}/100."
        
        # Add ratio highlights
        top_ratios = [r for r in ratio_cards if r.percentile and r.percentile > 70][:2]
        if top_ratios:
            names = [r.ratio_name for r in top_ratios]
            exec_summary += f" Öne çıkan metrikler: {', '.join(names)}."
        
        weak_ratios = [r for r in ratio_cards if r.percentile and r.percentile < 30][:2]
        if weak_ratios:
            names = [r.ratio_name for r in weak_ratios]
            exec_summary += f" Zayıf alanlar: {', '.join(names)}."
    else:
        exec_summary = f"{company_name} ({ticker}), {sector} sektöründe faaliyet gösteriyor. Temel analiz puanı henüz hesaplanmamış."
    
    # ── Financial Position ─────────────────────────────────────────────
    health_ratios = [r for r in ratio_cards if r.ratio_code in [
        'current_ratio', 'acid_test_ratio', 'debt_ratio', 'debt_to_equity', 'net_debt_to_equity'
    ]]
    
    if health_ratios:
        above = [r for r in health_ratios if r.percentile and r.percentile > 60]
        below = [r for r in health_ratios if r.percentile and r.percentile < 40]
        
        if len(above) > len(below):
            financial_pos = f"Şirketin finansal durumu güçlü. "
        elif len(below) > len(above):
            financial_pos = f"Şirketin finansal durumunda dikkat gerektiren alanlar mevcut. "
        else:
            financial_pos = f"Şirketin finansal durumu sektör ortalamasında. "
        
        for r in health_ratios[:3]:
            val_text = f"{r.company_value:.2f}" if r.company_value else "N/A"
            if r.sector_median:
                diff = "üzerinde" if (r.company_value or 0) > r.sector_median else "altında"
                financial_pos += f"{r.ratio_name}: {val_text} (sektör ortalamasının {diff}). "
            else:
                financial_pos += f"{r.ratio_name}: {val_text}. "
    else:
        financial_pos = "Finansal sağlık verisi yetersiz."
    
    # ── Profitability Analysis ─────────────────────────────────────────
    prof_ratios = [r for r in ratio_cards if r.ratio_code in [
        'roe', 'roa', 'gross_margin', 'net_margin', 'operating_margin', 'ebitda_margin'
    ]]
    
    if prof_ratios:
        profitability_analysis = "Kârlılık metrikleri: "
        for r in prof_ratios[:4]:
            val_text = f"%{r.company_value*100:.1f}" if r.company_value and r.ratio_code in [
                'roe', 'roa', 'gross_margin', 'net_margin', 'operating_margin', 'ebitda_margin'
            ] else f"{r.company_value:.2f}" if r.company_value else "N/A"
            
            if r.percentile:
                if r.percentile > 70:
                    status = "sektör üst çeyreğinde"
                elif r.percentile > 40:
                    status = "sektör ortalamasında"
                else:
                    status = "sektör altında"
                profitability_analysis += f"{r.ratio_name}: {val_text} ({status}), "
            else:
                profitability_analysis += f"{r.ratio_name}: {val_text}, "
        profitability_analysis = profitability_analysis.rstrip(", ") + "."
    else:
        profitability_analysis = "Kârlılık verisi yetersiz."
    
    # ── Balance Sheet Analysis ─────────────────────────────────────────
    balance_rats = [r for r in ratio_cards if r.ratio_code in [
        'current_ratio', 'debt_ratio', 'debt_to_equity', 'net_debt_to_equity', 'asset_turnover'
    ]]
    
    if balance_rats:
        balance_analysis = "Bilanço metrikleri: "
        for r in balance_rats[:4]:
            val_text = f"{r.company_value:.2f}" if r.company_value else "N/A"
            if r.percentile:
                if r.percentile > 60:
                    status = "sektör üzerinde"
                elif r.percentile < 40:
                    status = "sektör altında"
                else:
                    status = "sektör ortalamasında"
                balance_analysis += f"{r.ratio_name}: {val_text} ({status}), "
            else:
                balance_analysis += f"{r.ratio_name}: {val_text}, "
        balance_analysis = balance_analysis.rstrip(", ") + "."
    else:
        balance_analysis = "Bilanço verisi yetersiz."
    
    # ── Sector Comparison ──────────────────────────────────────────────
    if sector_position:
        above_median = len(sector_position.above_median_ratios)
        below_median = len(sector_position.below_median_ratios)
        total = above_median + below_median
        
        if total > 0:
            above_pct = (above_median / total) * 100
            if above_pct > 70:
                perf_desc = "sektör ortalamasının üzerinde güçlü bir performans"
            elif above_pct > 50:
                perf_desc = "çoğunlukla sektör ortalamasının üzerinde"
            elif above_pct > 30:
                perf_desc = "sektör ortalamasına yakın bir performans"
            else:
                perf_desc = "çoğunlukla sektör ortalamasının altında"
            
            sector_comp = f"Sektör karşılaştırmasında {above_median}/{total} oranda {perf_desc} gösteriyor."
            if sector_position.percentile:
                sector_comp += f" Genel percentil: %{sector_position.percentile:.0f}."
        else:
            sector_comp = "Sektör karşılaştırma verisi yetersiz."
    else:
        sector_comp = "Sektör karşılaştırma verisi bulunamadı."
    
    # ── Catalysts and Risks (from SWOT) ────────────────────────────────
    catalysts = []
    risks = []
    
    if swot_card:
        if swot_card.strengths:
            catalysts.extend([s.item for s in swot_card.strengths[:3]])
        if swot_card.opportunities:
            catalysts.extend([o.item for o in swot_card.opportunities[:2]])
        if swot_card.weaknesses:
            risks.extend([w.item for w in swot_card.weaknesses[:3]])
        if swot_card.threats:
            risks.extend([t.item for t in swot_card.threats[:2]])
    
    if not catalysts:
        catalysts = ["Sektördeki güçlü konumunu sürdürme potansiyeli"]
    if not risks:
        risks = ["Piyasa koşullarındaki değişkenlikler"]
    
    # ── Conclusion (data-driven) ───────────────────────────────────────
    if score_val:
        if score_val > 70:
            conclusion = f"{company_name}, temel analiz kriterlerine göre güçlü bir performans sergiliyor (puan: {score_val:.1f}/100). "
            conclusion += "Sektöründe üst sıralarda yer alması, sağlıklı finansal yapı ve kârlılık göstergelerine işaret ediyor."
        elif score_val > 50:
            conclusion = f"{company_name}, temel analiz kriterlerine göre ortalamanın üzerinde bir performans sergiliyor (puan: {score_val:.1f}/100). "
            conclusion += "Bazı metriklerde sektör ortalamasının üzerinde olmasına rağmen, iyileştirilebilecek alanlar mevcut."
        elif score_val > 30:
            conclusion = f"{company_name}, temel analiz kriterlerine göre ortalama bir performans sergiliyor (puan: {score_val:.1f}/100). "
            conclusion += "Sektöründe orta sıralarda yer alıyor. Kârlılık ve finansal yapı alanlarında iyileşme potansiyeli bulunuyor."
        else:
            conclusion = f"{company_name}, temel analiz kriterlerine göre zayıf bir performans sergiliyor (puan: {score_val:.1f}/100). "
            conclusion += "Sektöründe alt sıralarda yer alması, ciddi yapısal sorunlara işaret ediyor. Yatırım kararı alınırken dikkatli olunmalı."
        
        # Add SWOT-based insight
        if swot_card and swot_card.strengths:
            conclusion += f" Güçlü yönler: {swot_card.strengths[0].item}."
        if swot_card and swot_card.threats:
            conclusion += f" Riskler: {swot_card.threats[0].item}."
    else:
        conclusion = f"{company_name} için temel analiz puanı henüz hesaplanmamış. Yeterli finansal veri bekleniyor."
    
    return DetailedReport(
        executive_summary=exec_summary,
        financial_position=financial_pos,
        profitability_analysis=profitability_analysis,
        balance_sheet_analysis=balance_analysis,
        sector_comparison=sector_comp,
        swot_analysis=swot_card,
        catalysts=catalysts[:5],
        risks=risks[:5],
        conclusion=conclusion,
        disclaimer="Bu analiz otomatik veri analizine dayanmaktadır ve yatırım tavsiyesi değildir. Yatırım kararlarınız için profesyonel danışmanlık alınız."
    )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENDPOINT
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/analysis/{ticker}", response_model=TieredAnalysisResponse)
async def get_tiered_analysis(
    ticker: str,
    period_key: Optional[str] = Query(None, description="Period key (default: latest)"),
    authorization: Optional[str] = Header(None),
    x_user_tier: Optional[str] = Header(None, alias="X-User-Tier"),
    db: Session = Depends(get_db),
):
    """
    Get tiered fundamental analysis for a company.
    
    Tiers:
    - Anonymous: Score card + basic ratio cards
    - Member: Enhanced cards + 1-paragraph summary
    - Subscriber: Ultimate cards + detailed report + SWOT
    
    Headers:
    - Authorization: Bearer token (legacy support)
    - X-User-Tier: Explicit tier from orchestrator (pro, ultimate, standard, free)
    """
    
    # Determine user tier from headers
    tier = get_user_tier_from_headers(authorization, x_user_tier)
    
    # Get company info
    company = db.execute(text("""
        SELECT ticker, name, sector_main 
        FROM companies 
        WHERE ticker = :ticker AND is_active = TRUE
    """), {"ticker": ticker.upper()}).fetchone()
    
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
    
    # Get latest period if not specified
    if not period_key:
        period_key = db.execute(text("""
            SELECT MAX(period_key) FROM company_scores WHERE ticker = :ticker
        """), {"ticker": ticker.upper()}).scalar()
    
    if not period_key:
        raise HTTPException(status_code=404, detail=f"No analysis available for {ticker}")
    
    # Generate cards based on tier
    cards = []
    
    # 1. Score Card (all tiers)
    score_card = generate_score_card(db, ticker.upper(), period_key)
    if score_card:
        cards.append({"type": "score_card", "data": score_card.model_dump()})
    
    # 2. Ratio Comparison Cards (tier-dependent depth)
    ratio_cards = generate_ratio_comparison_cards(db, ticker.upper(), period_key, tier)
    for rc in ratio_cards:
        cards.append({"type": "ratio_comparison", "data": rc.model_dump()})
    
    # 3. Sector Position Card (member+)
    if tier in [UserTier.MEMBER, UserTier.SUBSCRIBER]:
        sector_pos = generate_sector_position_card(db, ticker.upper(), period_key)
        if sector_pos:
            cards.append({"type": "sector_position", "data": sector_pos.model_dump()})
    
    # 4. SWOT Card (member+)
    swot_card = None
    if tier in [UserTier.MEMBER, UserTier.SUBSCRIBER]:
        swot_card = generate_swot_card(db, ticker.upper(), period_key)
        cards.append({"type": "swot", "data": swot_card.model_dump()})
    
    # Generate analysis based on tier
    summary = None
    detailed_report = None
    
    if tier == UserTier.MEMBER and score_card and ratio_cards:
        summary = await generate_member_summary(
            ticker.upper(), company.name, company.sector_main,
            score_card, ratio_cards
        )
        # Member also gets detailed report if SWOT is available
        if swot_card:
            sector_pos = generate_sector_position_card(db, ticker.upper(), period_key)
            detailed_report = await generate_subscriber_report(
                ticker.upper(), company.name, company.sector_main,
                score_card, ratio_cards, swot_card,
                sector_pos or SectorPositionCard(
                    sector_name=company.sector_main,
                    total_companies=1,
                    rank=1,
                    percentile=50.0,
                    above_median_ratios=[],
                    below_median_ratios=[]
                )
            )
    
    elif tier == UserTier.SUBSCRIBER and score_card and ratio_cards and swot_card:
        sector_pos = generate_sector_position_card(db, ticker.upper(), period_key)
        detailed_report = await generate_subscriber_report(
            ticker.upper(), company.name, company.sector_main,
            score_card, ratio_cards, swot_card,
            sector_pos or SectorPositionCard(
                sector_name=company.sector_main,
                total_companies=1,
                rank=1,
                percentile=50.0,
                above_median_ratios=[],
                below_median_ratios=[]
            )
        )
    
    return TieredAnalysisResponse(
        tier=tier,
        ticker=ticker.upper(),
        company_name=company.name,
        sector=company.sector_main,
        cards=cards,
        summary=summary,
        detailed_report=detailed_report,
        period_key=period_key,
        computed_at=datetime.utcnow(),
        data_quality="verified"
    )


@router.get("/swot/{ticker}", response_model=SWOTCard)
async def get_swot_analysis(
    ticker: str,
    period_key: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None),
    x_user_tier: Optional[str] = Header(None, alias="X-User-Tier"),
    db: Session = Depends(get_db),
):
    """
    Get SWOT analysis for a company (subscriber only).
    
    Requires Pro or Ultimate subscription.
    """
    tier = get_user_tier_from_headers(authorization, x_user_tier)
    
    if tier != UserTier.SUBSCRIBER:
        raise HTTPException(
            status_code=403,
            detail="SWOT analizi Pro ve Ultimate aboneleri için özeldir."
        )
    
    if not period_key:
        period_key = db.execute(text("""
            SELECT MAX(period_key) FROM company_scores WHERE ticker = :ticker
        """), {"ticker": ticker.upper()}).scalar()
    
    return generate_swot_card(db, ticker.upper(), period_key)


# ─────────────────────────────────────────────────────────────────────────────
# CEO-LEVEL FUNDAMENTAL REPORT (No tier restrictions)
# ─────────────────────────────────────────────────────────────────────────────

class FundamentalReportResponse(BaseModel):
    """CEO-Level Fundamental Analysis Report Response"""
    ticker: str
    company_name: str
    sector: str
    period_key: str
    executive_summary: str
    financial_health: Dict[str, Any]
    profitability: Dict[str, Any]
    sector_comparison: Dict[str, Any]
    swot: Dict[str, Any]
    scenarios: Dict[str, Any]
    watchlist: List[Dict[str, str]]
    computed_at: datetime
    disclaimer: str


@router.get("/fundamental-report/{ticker}", response_model=FundamentalReportResponse)
async def get_fundamental_report(
    ticker: str,
    period_key: Optional[str] = Query(None, description="Period key (default: latest)"),
    db: Session = Depends(get_db),
):
    """
    CEO-level fundamental analysis report for all members.
    
    No tier restrictions — all authenticated users get full access.
    Includes: Executive Summary, Financial Health, Profitability,
    Sector Comparison, SWOT, Scenarios, Watchlist.
    """
    from services.fundamental_report import FundamentalReportService
    
    service = FundamentalReportService(db)
    report = service.generate(ticker.upper(), period_key)
    
    if not report:
        raise HTTPException(status_code=404, detail=f"Fundamental report for {ticker} not found or insufficient data.")
    
    return FundamentalReportResponse(
        ticker=report.ticker,
        company_name=report.company_name,
        sector=report.sector,
        period_key=report.period_key,
        executive_summary=report.executive_summary,
        financial_health=report.financial_health,
        profitability=report.profitability,
        sector_comparison=report.sector_comparison,
        swot=report.swot,
        scenarios=report.scenarios,
        watchlist=report.watchlist,
        computed_at=report.computed_at,
        disclaimer=report.disclaimer,
    )
