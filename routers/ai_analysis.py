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
            "standard": UserTier.MEMBER,
            "free": UserTier.MEMBER,
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
            cs.score_karlilik, cs.score_finansal, cs.score_verimlilik,
            cs.reliability_sektor, cs.n_peers_sektor,
            c.sector_main
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.ticker = :ticker AND cs.period_key = :period_key
    """), {"ticker": ticker, "period_key": period_key}).fetchone()
    
    if not result:
        return None
    
    # Calculate rank and percentile
    rank_result = db.execute(text("""
        SELECT COUNT(*) + 1 as rank
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE c.sector_main = :sector
          AND cs.period_key = :period_key
          AND cs.score_sektor > :score
    """), {
        "sector": result.sector_main,
        "period_key": period_key,
        "score": result.score_sektor or 0
    }).fetchone()
    
    rank = rank_result.rank if rank_result else 1
    percentile = int(100 - (rank / max(result.n_peers_sektor or 1, 1)) * 100)
    
    return ScoreCard(
        score_sektor=float(result.score_sektor) if result.score_sektor else None,
        score_genel=float(result.score_genel) if result.score_genel else None,
        score_karlilik=float(result.score_karlilik) if result.score_karlilik else None,
        score_finansal=float(result.score_finansal) if result.score_finansal else None,
        score_verimlilik=float(result.score_verimlilik) if result.score_verimlilik else None,
        reliability=result.reliability_sektor,
        percentile_sector=percentile,
        rank_sector=rank,
        total_peers=result.n_peers_sektor
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
    """Generate SWOT analysis card"""
    
    # Get company scores and ratios
    scores = db.execute(text("""
        SELECT 
            cs.score_sektor, cs.score_karlilik, cs.score_finansal, cs.score_verimlilik,
            cr.ratio_code, cr.ratio_value
        FROM company_scores cs
        LEFT JOIN company_ratios cr ON cr.ticker = cs.ticker AND cr.period_key = cs.period_key
        WHERE cs.ticker = :ticker AND cs.period_key = :period_key
    """), {"ticker": ticker, "period_key": period_key}).fetchall()
    
    strengths = []
    weaknesses = []
    opportunities = []
    threats = []
    
    # Analyze based on scores
    for row in scores:
        if row.score_karlilik and float(row.score_karlilik) > 70:
            strengths.append(SWOTItem(
                item="Yüksek kârlılık performansı",
                impact="high",
                source="score_karlilik"
            ))
        elif row.score_karlilik and float(row.score_karlilik) < 40:
            weaknesses.append(SWOTItem(
                item="Kârlılık baskısı",
                impact="high",
                source="score_karlilik"
            ))
        
        if row.score_finansal and float(row.score_finansal) > 70:
            strengths.append(SWOTItem(
                item="Güçlü finansal yapı",
                impact="high",
                source="score_finansal"
            ))
        elif row.score_finansal and float(row.score_finansal) < 40:
            threats.append(SWOTItem(
                item="Finansal risk faktörleri",
                impact="medium",
                source="score_finansal"
            ))
    
    # Add generic opportunities and threats
    opportunities.extend([
        SWOTItem(item="Sektör büyüme potansiyeli", impact="medium", source="sector_trend"),
        SWOTItem(item="Pazar payı genişleme imkanı", impact="medium", source="market_position")
    ])
    
    threats.extend([
        SWOTItem(item="Sektörel rekabet baskısı", impact="medium", source="sector_analysis"),
        SWOTItem(item="Makroekonomik belirsizlik", impact="low", source="macro_environment")
    ])
    
    return SWOTCard(
        strengths=strengths[:5],
        weaknesses=weaknesses[:5],
        opportunities=opportunities[:5],
        threats=threats[:5],
        overall_assessment=None  # Will be generated by AI
    )


def generate_sector_position_card(db, ticker: str, period_key: str) -> Optional[SectorPositionCard]:
    """Generate sector position card"""
    
    result = db.execute(text("""
        SELECT 
            c.sector_main,
            cs.score_sektor,
            cs.n_peers_sektor,
            RANK() OVER (
                PARTITION BY c.sector_main 
                ORDER BY cs.score_sektor DESC NULLS LAST
            ) as sector_rank
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.ticker = :ticker AND cs.period_key = :period_key
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
    
    return SectorPositionCard(
        sector_name=result.sector_main,
        total_companies=result.n_peers_sektor or 1,
        rank=int(result.sector_rank) if result.sector_rank else 1,
        percentile=float(result.score_sektor) if result.score_sektor else 50.0,
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
    """Generate member-level summary (1 paragraph)"""
    
    # Build context for analysis - handle null scores gracefully
    score_val = score_card.score_sektor if score_card and score_card.score_sektor else None
    score_desc = "güçlü" if score_val and score_val > 60 else "orta" if score_val and score_val > 40 else "zayıf" if score_val else "belirsiz"
    
    top_ratios = sorted(ratio_cards, key=lambda x: x.percentile or 0, reverse=True)[:3] if ratio_cards else []
    ratio_strengths = [r.ratio_name for r in top_ratios if r.percentile and r.percentile > 60]
    
    if score_val:
        summary_text = f"{company_name} ({ticker}), {sector} sektöründe {score_desc} bir performans sergiliyor. Temel analiz puanı {score_val:.1f}/100 ile sektör içinde %{score_card.percentile_sector or 50} persentilde yer alıyor."
    else:
        summary_text = f"{company_name} ({ticker}), {sector} sektöründe faaliyet gösteriyor. Temel analiz verileri hesaplanıyor."
    
    if ratio_strengths:
        summary_text += f" Öne çıkan metrikler: {', '.join(ratio_strengths[:2])}."
    
    key_strengths = ratio_strengths[:2] if ratio_strengths else ["Sektör içi konum"]
    key_concerns = [r.ratio_name for r in ratio_cards if r.percentile and r.percentile < 40][:2] if ratio_cards else []
    
    return AnalysisSummary(
        summary=summary_text,
        key_strengths=key_strengths,
        key_concerns=key_concerns if key_concerns else ["Yetersiz veri"],
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
    """Generate subscriber-level detailed report"""
    
    # Handle null scores gracefully
    score_val = score_card.score_sektor if score_card and score_card.score_sektor else None
    karlilik_val = score_card.score_karlilik if score_card and score_card.score_karlilik else None
    finansal_val = score_card.score_finansal if score_card and score_card.score_finansal else None
    
    # Executive summary
    if score_val:
        exec_summary = f"{company_name} ({ticker}), {sector} sektöründe {sector_position.rank if sector_position else '-'}. sırada yer alıyor. Temel analiz puanı: {score_val:.1f}/100."
        if karlilik_val and finansal_val:
            exec_summary += f" Kârlılık skoru: {karlilik_val:.1f}, Finansal sağlık: {finansal_val:.1f}."
    else:
        exec_summary = f"{company_name} ({ticker}), {sector} sektöründe faaliyet gösteriyor. Detaylı analiz verileri hesaplanıyor."
    
    # Financial position
    if finansal_val:
        financial_pos = f"Şirketin finansal durumu {'güçlü' if finansal_val > 60 else 'orta' if finansal_val > 40 else 'dikkat gerektirir'}."
    else:
        financial_pos = "Finansal durum analizi için yeterli veri bulunamadı."
    
    if sector_position:
        financial_pos += f" Sektör içi pozisyon: %{sector_position.percentile:.0f} percentil."
    
    # Profitability analysis
    profitability_rats = [r for r in ratio_cards if r.ratio_code in ['roe', 'roa', 'gross_margin', 'net_margin']] if ratio_cards else []
    profitability_analysis = "Kârlılık metrikleri: " + ", ".join([
        f"{r.ratio_name}: {r.company_value:.2f}" for r in profitability_rats[:3]
    ]) if profitability_rats else "Kârlılık verisi yetersiz."
    
    # Balance sheet analysis
    balance_rats = [r for r in ratio_cards if r.ratio_code in ['current_ratio', 'debt_ratio', 'net_debt_to_equity']] if ratio_cards else []
    balance_analysis = "Bilanço metrikleri: " + ", ".join([
        f"{r.ratio_name}: {r.company_value:.2f}" for r in balance_rats[:3]
    ]) if balance_rats else "Bilanço verisi yetersiz."
    
    # Sector comparison
    if sector_position:
        sector_comp = f"Sektör karşılaştırmasında {len(sector_position.above_median_ratios)} oranda sektör ortalamasının üzerinde, {len(sector_position.below_median_ratios)} oranda ise altında performans gösteriyor."
    else:
        sector_comp = "Sektör karşılaştırma verisi yetersiz."
    
    # Catalysts and risks
    catalysts = ["Sektörel büyüme potansiyeli", "Operasyonel verimlilik artışı"]
    risks = ["Piyasa volatilitesi", "Sektörel rekabet"]
    
    if swot_card and swot_card.strengths:
        catalysts.extend([s.item for s in swot_card.strengths[:2]])
    if swot_card and swot_card.threats:
        risks.extend([t.item for t in swot_card.threats[:2]])
    
    # Conclusion
    if score_val:
        conclusion = f"{company_name}, temel analiz kriterlerine göre {'olumlu' if score_val > 60 else 'nötr' if score_val > 40 else 'dikkatli'} bir görünüm sunuyor. Yatırımcıların kendi risk profillerine göre pozisyon alması önerilir."
    else:
        conclusion = f"{company_name} için detaylı analiz tamamlanınca güncellenecektir."
    
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
        disclaimer="Bu analiz yatırım tavsiyesi değildir. Yatırım kararlarınız için profesyonel danışmanlık alınız."
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
    
    # 4. SWOT Card (subscriber only)
    swot_card = None
    if tier == UserTier.SUBSCRIBER:
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
