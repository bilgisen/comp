"""
Sector/Industry analysis API endpoints

IMPORTANT: This module supports both legacy sector_main (14 sectors) 
and new industry classification (21-28 industries) for backward compatibility.

New endpoints use /industries/ prefix, legacy endpoints use /sectors/
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, text

from core.database import get_db, get_async_db
from models.company import Company
from models.benchmark import SectorBenchmark

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== NEW INDUSTRY ENDPOINTS ====================

@router.get("/industries")
async def list_industries(db: AsyncSession = Depends(get_async_db)):
    """
    List all industries with company counts and reliability ratings
    
    Returns 21-28 industries for better peer comparisons
    """
    try:
        # Get latest period
        latest_period_result = await db.execute(
            text("SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE")
        )
        latest_period = latest_period_result.scalar()
        
        if not latest_period:
            latest_period = "2026Q1"  # Default fallback
        
        # Count companies per industry (with or without scores)
        query_text = text("""
            SELECT 
                c.industry,
                COUNT(DISTINCT c.ticker) as company_count,
                COUNT(DISTINCT cs.ticker) as scored_count
            FROM companies c
            LEFT JOIN company_scores cs ON c.ticker = cs.ticker 
                AND cs.period_key = :period 
                AND cs.is_stale = FALSE
            WHERE c.is_active = TRUE 
              AND c.industry IS NOT NULL
            GROUP BY c.industry
            ORDER BY company_count DESC
        """)
        
        result = await db.execute(query_text, {"period": latest_period})
        industries = result.all()
        
        # Classify reliability
        industry_list = []
        for ind in industries:
            count = ind.company_count
            reliability = (
                "HIGH" if count >= 10 else
                "MEDIUM" if count >= 5 else
                "LOW"
            )
            
            industry_list.append({
                "name": ind.industry,
                "slug": ind.industry.lower().replace(" ", "-").replace("&", "and").replace("ı", "i").replace("ş", "s").replace("ğ", "g").replace("ü", "u").replace("ö", "o").replace("ç", "c").replace("İ", "i"),
                "total_companies": count,
                "active_companies": ind.scored_count or 0,  # Companies with scores
                "reliability": reliability,
                "min_peers_for_benchmark": 3
            })
        
        return {
            "industries": industry_list,
            "total_industries": len(industry_list),
            "high_quality_count": sum(1 for i in industry_list if i["reliability"] == "HIGH"),
            "period": latest_period,
            "system": "industry"  # Indicates this is the new system
        }
        
    except Exception as e:
        logger.error(f"Error listing industries: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/industries/{industry}")
async def get_industry_detail(
    industry: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Get detailed information about an industry"""
    try:
        # Decode URL-encoded industry name
        industry_name = industry.replace("-", " ").replace("and", "&").title()
        
        # Get company count and list
        query_text = text("""
            SELECT 
                c.ticker,
                c.name,
                c.market_cap,
                c.city,
                cs.total_score,
                cs.percentile
            FROM companies c
            LEFT JOIN company_scores cs ON c.ticker = cs.ticker 
                AND cs.period_key = (SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE)
            WHERE c.industry = :industry 
              AND c.is_active = TRUE
            ORDER BY cs.total_score DESC NULLS LAST
        """)
        
        result = await db.execute(query_text, {"industry": industry_name})
        companies = result.all()
        
        if not companies:
            raise HTTPException(status_code=404, detail=f"Industry '{industry}' not found")
        
        return {
            "industry": industry_name,
            "slug": industry,
            "total_companies": len(companies),
            "companies": [
                {
                    "ticker": c.ticker,
                    "name": c.name,
                    "market_cap": c.market_cap,
                    "city": c.city,
                    "score": float(c.total_score) if c.total_score else None,
                    "percentile": float(c.percentile) if c.percentile else None
                }
                for c in companies
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting industry detail for {industry}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/industries/{industry}/benchmarks")
async def get_industry_benchmarks(
    industry: str,
    period: Optional[str] = Query(None, description="Period key (e.g., 2026Q1)"),
    ratios: Optional[List[str]] = Query(None, description="Specific ratio codes"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get benchmark data for an industry"""
    try:
        from services.sector_benchmarks import SectorBenchmarkService
        
        # Decode URL-encoded industry name
        industry_name = industry.replace("-", " ").replace("and", "&").title()
        
        benchmark_service = SectorBenchmarkService(db)
        benchmarks = await benchmark_service.get_sector_benchmarks(
            sector_main=industry_name,  # Note: DB column is still sector_main
            period_key=period,
            ratio_codes=ratios
        )
        
        return {
            "industry": industry_name,
            "slug": industry,
            "period": period or benchmarks.get("period_key"),
            "benchmarks": benchmarks,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting benchmarks for industry {industry}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== LEGACY SECTOR ENDPOINTS (BACKWARD COMPATIBILITY) ====================

@router.get("/")
async def list_sectors(db: AsyncSession = Depends(get_async_db)):
    """
    LEGACY: List all available sectors (14 broad categories)
    
    For new implementations, use /industries endpoint instead
    """
    try:
        # Get latest period
        latest_period_result = await db.execute(
            text("SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE")
        )
        latest_period = latest_period_result.scalar()
        
        if not latest_period:
            # Fallback to all companies if no scores exist
            query = select(
                Company.sector_main,
                func.count(Company.id).label("company_count"),
                func.count(Company.id).filter(Company.is_active == True).label("active_companies")
            ).group_by(Company.sector_main)
            
            result = await db.execute(query)
            sectors = result.all()
            
            return {
                "sectors": [
                    {
                        "name": sector.sector_main,
                        "total_companies": sector.company_count,
                        "active_companies": sector.active_companies
                    }
                    for sector in sectors
                ],
                "total_sectors": len(sectors),
                "system": "legacy"
            }
        
        # Count companies WITH scores per sector
        query_text = text("""
            SELECT 
                c.sector_main,
                COUNT(DISTINCT cs.ticker) as company_count
            FROM company_scores cs
            JOIN companies c ON cs.ticker = c.ticker
            WHERE cs.period_key = :period AND cs.is_stale = FALSE
            GROUP BY c.sector_main
            ORDER BY c.sector_main
        """)
        
        result = await db.execute(query_text, {"period": latest_period})
        sectors = result.all()
        
        return {
            "sectors": [
                {
                    "name": sector.sector_main,
                    "total_companies": sector.company_count,
                    "active_companies": sector.company_count
                }
                for sector in sectors
            ],
            "total_sectors": len(sectors),
            "period": latest_period,
            "system": "legacy",
            "note": "Use /industries endpoint for better peer comparisons"
        }
        
    except Exception as e:
        logger.error(f"Error listing sectors: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{sector}/benchmarks")
async def get_sector_benchmarks(
    sector: str,
    period: Optional[str] = Query(None, description="Period key"),
    ratios: Optional[List[str]] = Query(None, description="Specific ratios"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get sector benchmark data"""
    try:
        from services.sector_benchmarks import SectorBenchmarkService
        
        benchmark_service = SectorBenchmarkService(db)
        benchmarks = await benchmark_service.get_sector_benchmarks(
            sector_main=sector,
            period_key=period,
            ratio_codes=ratios
        )
        
        return {
            "sector": sector,
            "period": period,
            "benchmarks": benchmarks,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting benchmarks for {sector}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{sector}/companies")
async def get_sector_companies(
    sector: str,
    active_only: bool = Query(True, description="Only active companies"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get companies in a sector"""
    try:
        query = select(Company).where(Company.sector_main == sector)
        
        if active_only:
            query = query.where(Company.is_active == True)
        
        result = await db.execute(query.order_by(Company.name))
        companies = result.scalars().all()
        
        return {
            "sector": sector,
            "companies": [
                {
                    "ticker": company.ticker,
                    "name": company.name,
                    "city": company.city,
                    "financial_group": company.financial_group,
                    "is_active": company.is_active
                }
                for company in companies
            ],
            "count": len(companies)
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting companies for {sector}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{sector}/benchmarks")
async def get_sector_benchmarks(
    sector: str,
    period: Optional[str] = Query(None, description="Period key"),
    ratios: Optional[List[str]] = Query(None, description="Specific ratios"),
    db: AsyncSession = Depends(get_async_db)
):
    """LEGACY: Get sector benchmark data (use /industries/{industry}/benchmarks instead)"""
    try:
        from services.sector_benchmarks import SectorBenchmarkService
        
        benchmark_service = SectorBenchmarkService(db)
        benchmarks = await benchmark_service.get_sector_benchmarks(
            sector_main=sector,
            period_key=period,
            ratio_codes=ratios
        )
        
        return {
            "sector": sector,
            "period": period,
            "benchmarks": benchmarks,
            "generated_at": datetime.utcnow().isoformat(),
            "system": "legacy"
        }
        
    except Exception as e:
        logger.error(f"Error getting benchmarks for {sector}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{sector}/companies")
async def get_sector_companies(
    sector: str,
    active_only: bool = Query(True, description="Only active companies"),
    db: AsyncSession = Depends(get_async_db)
):
    """LEGACY: Get companies in a sector (use /industries/{industry} instead)"""
    try:
        query = select(Company).where(Company.sector_main == sector)
        
        if active_only:
            query = query.where(Company.is_active == True)
        
        result = await db.execute(query.order_by(Company.name))
        companies = result.scalars().all()
        
        return {
            "sector": sector,
            "companies": [
                {
                    "ticker": company.ticker,
                    "name": company.name,
                    "city": company.city,
                    "financial_group": company.financial_group,
                    "industry": company.industry,  # Show new industry field
                    "is_active": company.is_active
                }
                for company in companies
            ],
            "count": len(companies),
            "system": "legacy"
        }
        
    except Exception as e:
        logger.error(f"Error getting companies for {sector}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
