"""
Sector analysis API endpoints
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from models.company import Company
from models.benchmark import SectorBenchmark

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def list_sectors(db: Session = Depends(get_db)):
    """List all available sectors with company counts"""
    try:
        from sqlalchemy import func
        
        sectors = db.query(
            Company.sector_main,
            func.count(Company.id).label("company_count"),
            func.count(Company.id).filter(Company.is_active == True).label("active_companies")
        ).group_by(Company.sector_main).all()
        
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
        
    except Exception as e:
        logger.error(f"❌ Error listing sectors: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{sector}/benchmarks")
async def get_sector_benchmarks(
    sector: str,
    period: Optional[str] = Query(None, description="Period key"),
    ratios: Optional[List[str]] = Query(None, description="Specific ratios"),
    db: Session = Depends(get_db)
):
    """Get sector benchmark data"""
    try:
        from services.sector_benchmarks import SectorBenchmarkService
        
        benchmark_service = SectorBenchmarkService(db)
        benchmarks = await benchmark_service.get_sector_benchmarks(
            sector=sector,
            period=period,
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
    db: Session = Depends(get_db)
):
    """Get companies in a sector"""
    try:
        query = db.query(Company).filter(Company.sector_main == sector)
        
        if active_only:
            query = query.filter(Company.is_active == True)
        
        companies = query.order_by(Company.name).all()
        
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