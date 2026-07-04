"""
Sector analysis API endpoints
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from core.database import get_db, get_async_db
from models.company import Company
from models.benchmark import SectorBenchmark

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def list_sectors(db: AsyncSession = Depends(get_async_db)):
    """List all available sectors with company counts (only companies with scores)"""
    try:
        from sqlalchemy import text
        
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
                "total_sectors": len(sectors)
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
                    "active_companies": sector.company_count  # Same as total since we only count scored companies
                }
                for sector in sectors
            ],
            "total_sectors": len(sectors),
            "period": latest_period
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing sectors: {e}", exc_info=True)
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
