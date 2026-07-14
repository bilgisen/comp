"""
Company Scores API Router
Endpoints for company rating scores
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, desc

from core.database import get_db
from models.score import CompanyScore, CompanyScoreDetail
from pydantic import BaseModel


router = APIRouter(prefix="/scores", tags=["scores"])


# ─────────────────────────────────────────────────────────────────────────────
# PYDANTIC MODELS
# ─────────────────────────────────────────────────────────────────────────────

class ScoreDetailResponse(BaseModel):
    ratio_code: str
    ratio_value: Optional[float]
    peer_median: Optional[float]
    peer_p25: Optional[float]
    peer_p75: Optional[float]
    ratio_score: Optional[float]
    ratio_score_raw: Optional[float]
    pillar: str
    scope: str
    higher_is_better: bool
    reliability: Optional[str]

    class Config:
        from_attributes = True


class CompanyScoreResponse(BaseModel):
    ticker: str
    period_key: str
    score_sektor: Optional[float]
    score_genel: Optional[float]
    score_karlilik: Optional[float]
    score_finansal: Optional[float]
    score_verimlilik: Optional[float]
    score_degerleme: Optional[float]
    reliability_sektor: Optional[str]
    reliability_genel: Optional[str]
    n_peers_sektor: Optional[int]
    n_peers_genel: Optional[int]
    pillar_coverage: Optional[float]
    data_quality_score: Optional[float]
    computed_at: datetime
    details: Optional[List[ScoreDetailResponse]] = None

    class Config:
        from_attributes = True


class ScoreSummaryResponse(BaseModel):
    ticker: str
    name: Optional[str]
    sector_main: Optional[str]
    period_key: str
    score_sektor: Optional[float]
    score_genel: Optional[float]
    reliability_sektor: Optional[str]

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    rank: int
    ticker: str
    name: Optional[str]
    sector_main: Optional[str]
    score: float
    reliability: Optional[str]

    class Config:
        from_attributes = True


class SectorLeaderboardResponse(BaseModel):
    sector: str
    companies: List[LeaderboardResponse]


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/{ticker}", response_model=CompanyScoreResponse)
async def get_company_score(
    ticker: str,
    period_key: Optional[str] = Query(None, description="Period key (e.g., 2026Q1)"),
    include_details: bool = Query(False, description="Include ratio-level details"),
    db: Session = Depends(get_db),
):
    """
    Get score for a specific company.
    
    If period_key is not provided, returns the latest available period.
    """
    query = db.query(CompanyScore).filter(CompanyScore.ticker == ticker.upper())
    
    if period_key:
        query = query.filter(CompanyScore.period_key == period_key)
    else:
        query = query.order_by(desc(CompanyScore.period_key))
    
    score = query.first()
    
    if not score:
        raise HTTPException(
            status_code=404,
            detail=f"No score found for {ticker}"
        )
    
    response = CompanyScoreResponse(
        ticker=score.ticker,
        period_key=score.period_key,
        score_sektor=float(score.score_sektor) if score.score_sektor else None,
        score_genel=float(score.score_genel) if score.score_genel else None,
        score_karlilik=float(score.score_karlilik) if score.score_karlilik else None,
        score_finansal=float(score.score_finansal) if score.score_finansal else None,
        score_verimlilik=float(score.score_verimlilik) if score.score_verimlilik else None,
        score_degerleme=float(score.score_degerleme) if score.score_degerleme else None,
        reliability_sektor=score.reliability_sektor,
        reliability_genel=score.reliability_genel,
        n_peers_sektor=score.n_peers_sektor,
        n_peers_genel=score.n_peers_genel,
        pillar_coverage=float(score.pillar_coverage) if score.pillar_coverage else None,
        data_quality_score=float(score.data_quality_score) if score.data_quality_score else None,
        computed_at=score.computed_at,
    )
    
    if include_details:
        details = db.query(CompanyScoreDetail).filter(
            CompanyScoreDetail.score_id == score.id
        ).all()
        
        response.details = [
            ScoreDetailResponse(
                ratio_code=d.ratio_code,
                ratio_value=float(d.ratio_value) if d.ratio_value else None,
                peer_median=float(d.peer_median) if d.peer_median else None,
                peer_p25=float(d.peer_p25) if d.peer_p25 else None,
                peer_p75=float(d.peer_p75) if d.peer_p75 else None,
                ratio_score=float(d.ratio_score) if d.ratio_score else None,
                ratio_score_raw=float(d.ratio_score_raw) if d.ratio_score_raw else None,
                pillar=d.pillar,
                scope=d.scope,
                higher_is_better=d.higher_is_better,
                reliability=d.reliability,
            )
            for d in details
        ]
    
    return response


@router.get("/", response_model=List[ScoreSummaryResponse])
async def list_scores(
    period_key: Optional[str] = Query(None, description="Period key"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    min_score: Optional[float] = Query(None, description="Minimum sector score"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    List company scores with optional filters.
    """
    query = text("""
        SELECT 
            cs.ticker,
            c.name,
            c.sector_main,
            cs.period_key,
            cs.score_sektor,
            cs.score_genel,
            cs.reliability_sektor
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.is_stale = FALSE
    """)
    
    params = {}
    conditions = []
    
    if period_key:
        conditions.append("cs.period_key = :period_key")
        params["period_key"] = period_key
    
    if sector:
        conditions.append("c.sector_main = :sector")
        params["sector"] = sector
    
    if min_score:
        conditions.append("cs.score_sektor >= :min_score")
        params["min_score"] = min_score
    
    if conditions:
        query = text(str(query) + " AND " + " AND ".join(conditions))
    
    query = text(str(query) + f" ORDER BY cs.score_sektor DESC NULLS LAST LIMIT {limit} OFFSET {offset}")
    
    rows = db.execute(query, params).fetchall()
    
    return [
        ScoreSummaryResponse(
            ticker=row.ticker,
            name=row.name,
            sector_main=row.sector_main,
            period_key=row.period_key,
            score_sektor=float(row.score_sektor) if row.score_sektor else None,
            score_genel=float(row.score_genel) if row.score_genel else None,
            reliability_sektor=row.reliability_sektor,
        )
        for row in rows
    ]


@router.get("/leaderboard/sektor", response_model=List[SectorLeaderboardResponse])
async def get_sector_leaderboard(
    period_key: Optional[str] = Query(None, description="Period key"),
    top_n: int = Query(10, ge=1, le=50, description="Top N per sector"),
    db: Session = Depends(get_db),
):
    """
    Get top companies by sector score within each sector.
    """
    # Get latest period if not specified
    if not period_key:
        period_key = db.execute(text("""
            SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE
        """)).scalar()
    
    if not period_key:
        raise HTTPException(status_code=404, detail="No scores available")
    
    query = text("""
        SELECT 
            c.sector_main,
            cs.ticker,
            c.name,
            cs.score_sektor,
            cs.reliability_sektor,
            RANK() OVER (PARTITION BY c.sector_main ORDER BY cs.score_sektor DESC NULLS LAST) as rank
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.period_key = :period_key
          AND cs.is_stale = FALSE
          AND cs.score_sektor IS NOT NULL
    """)
    
    rows = db.execute(query, {"period_key": period_key}).fetchall()
    
    # Group by sector
    sector_data = {}
    for row in rows:
        sector = row.sector_main or "Unknown"
        if sector not in sector_data:
            sector_data[sector] = []
        
        if row.rank <= top_n:
            sector_data[sector].append(LeaderboardResponse(
                rank=int(row.rank),
                ticker=row.ticker,
                name=row.name,
                sector_main=sector,
                score=float(row.score_sektor),
                reliability=row.reliability_sektor,
            ))
    
    return [
        SectorLeaderboardResponse(
            sector=sector,
            companies=companies[:top_n]
        )
        for sector, companies in sorted(sector_data.items())
    ]


@router.get("/leaderboard/genel", response_model=List[LeaderboardResponse])
async def get_global_leaderboard(
    period_key: Optional[str] = Query(None, description="Period key"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """
    Get top companies by general (market-wide) score.
    """
    # Get latest period if not specified
    if not period_key:
        period_key = db.execute(text("""
            SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE
        """)).scalar()
    
    if not period_key:
        raise HTTPException(status_code=404, detail="No scores available")
    
    query = text("""
        SELECT 
            cs.ticker,
            c.name,
            c.sector_main,
            cs.score_genel,
            cs.reliability_genel,
            RANK() OVER (ORDER BY cs.score_genel DESC NULLS LAST) as rank
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.period_key = :period_key
          AND cs.is_stale = FALSE
          AND cs.score_genel IS NOT NULL
        ORDER BY cs.score_genel DESC NULLS LAST
        LIMIT :limit
    """)
    
    rows = db.execute(query, {"period_key": period_key, "limit": limit}).fetchall()
    
    return [
        LeaderboardResponse(
            rank=int(row.rank),
            ticker=row.ticker,
            name=row.name,
            sector_main=row.sector_main,
            score=float(row.score_genel),
            reliability=row.reliability_genel,
        )
        for row in rows
    ]


@router.get("/compare/{tickers}")
async def compare_scores(
    tickers: str,
    period_key: Optional[str] = Query(None, description="Period key"),
    db: Session = Depends(get_db),
):
    """
    Compare scores of multiple companies.
    
    tickers: Comma-separated list of ticker symbols (e.g., "THYAO,GARAN,AKBNK")
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    
    if len(ticker_list) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 tickers allowed")
    
    # Get latest period if not specified
    if not period_key:
        period_key = db.execute(text("""
            SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE
        """)).scalar()
    
    if not period_key:
        raise HTTPException(status_code=404, detail="No scores available")
    
    query = text("""
        SELECT 
            cs.ticker,
            c.name,
            c.sector_main,
            cs.score_sektor,
            cs.score_genel,
            cs.score_karlilik,
            cs.score_finansal,
            cs.score_verimlilik,
            cs.score_degerleme,
            cs.reliability_sektor,
            cs.reliability_genel
        FROM company_scores cs
        JOIN companies c ON cs.ticker = c.ticker
        WHERE cs.ticker = ANY(:tickers)
          AND cs.period_key = :period_key
          AND cs.is_stale = FALSE
    """)
    
    rows = db.execute(query, {"tickers": ticker_list, "period_key": period_key}).fetchall()
    
    return {
        "period_key": period_key,
        "companies": [
            {
                "ticker": row.ticker,
                "name": row.name,
                "sector_main": row.sector_main,
                "score_sektor": float(row.score_sektor) if row.score_sektor else None,
                "score_genel": float(row.score_genel) if row.score_genel else None,
                "pillars": {
                    "karlilik": float(row.score_karlilik) if row.score_karlilik else None,
                    "finansal": float(row.score_finansal) if row.score_finansal else None,
                    "verimlilik": float(row.score_verimlilik) if row.score_verimlilik else None,
                    "degerleme": float(row.score_degerleme) if row.score_degerleme else None,
                },
                "reliability": {
                    "sektor": row.reliability_sektor,
                    "genel": row.reliability_genel,
                }
            }
            for row in rows
        ]
    }


@router.post("/compute/{period_key}")
async def trigger_scoring(
    period_key: str,
    db: Session = Depends(get_db),
):
    """
    Manually trigger scoring for a period (background task).
    
    Note: In production, this should be a background task.
    """
    from services.scoring.worker import ScoringWorker
    
    worker = ScoringWorker(db)
    results = worker.run_scoring_for_period(period_key)
    
    return {
        "status": "completed",
        "period_key": period_key,
        "results": results
    }
