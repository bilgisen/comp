"""
Admin API endpoints
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from services.isyatirim_client import isyatirim_client

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/fetch/trigger")
async def trigger_manual_fetch(
    tickers: List[str] = Query(..., description="Company tickers to fetch"),
    force: bool = Query(False, description="Force fetch even if data exists"),
    db: Session = Depends(get_db)
):
    """Trigger manual data fetch for specific companies"""
    try:
        results = []
        from models.company import Company
        from models.financial import FinancialStatementRaw, FetchLog
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        import json
        
        # Support "ALL" keyword to bootstrap all active companies in bulk
        if tickers and "ALL" in [t.upper().strip() for t in tickers]:
            active_companies = db.query(Company).filter(Company.is_active == True).all()
            tickers = [c.ticker for c in active_companies]
            logger.info(f"🚀 Triggering bulk manual fetch for all {len(tickers)} active companies")
        
        async with isyatirim_client:
            for ticker in tickers:
                ticker = ticker.upper().strip()
                
                # Get company metadata to get correct financial_group
                company = db.query(Company).filter(Company.ticker == ticker).first()
                if not company:
                    results.append({
                        "ticker": ticker,
                        "success": False,
                        "error": "Company not found in metadata",
                        "response_time_ms": 0,
                        "checksum": None
                    })
                    continue
                
                financial_group = company.financial_group or "XI_29"
                periods = isyatirim_client._get_periods_to_fetch()
                
                # Fetch data from İş Yatırım
                result = await isyatirim_client.fetch_mali_tablo(
                    ticker=ticker,
                    financial_group=financial_group,
                    periods=periods
                )
                
                rows_inserted = 0
                if result.success and result.data:
                    items = result.data.get("value", [])
                    fetched_at = datetime.utcnow()
                    insert_values = []
                    
                    for item in items:
                        item_code = item.get("itemCode")
                        item_desc_tr = item.get("itemDescTr")
                        item_desc_en = item.get("itemDescEng")
                        
                        for idx, (year, period) in enumerate(periods, 1):
                            val_key = f"value{idx}"
                            val_str = item.get(val_key)
                            
                            if val_str is None:
                                continue
                            
                            try:
                                # Parse value - API returns plain number strings (no formatting)
                                # e.g., "566760333000" or "0" or sometimes with decimals
                                if isinstance(val_str, str):
                                    val_str = val_str.strip()
                                    if not val_str or val_str == "":
                                        value_try = None
                                    else:
                                        # Remove thousand separators if any, replace comma with dot for decimals
                                        val_clean = val_str.replace(".", "").replace(",", ".")
                                        value_try = float(val_clean)
                                elif isinstance(val_str, (int, float)):
                                    value_try = float(val_str)
                                else:
                                    value_try = None
                            except (ValueError, AttributeError):
                                value_try = None
                            
                            period_key = f"{year}Q{period//3 if period != 12 else 4}"
                            
                            insert_values.append({
                                "ticker": ticker,
                                "period_key": period_key,
                                "year": year,
                                "period": period,
                                "financial_group": financial_group,
                                "item_code": item_code,
                                "item_desc_tr": item_desc_tr,
                                "item_desc_en": item_desc_en,
                                "value_try": value_try,
                                "fetched_at": fetched_at
                            })
                    
                    if insert_values:
                        stmt = pg_insert(FinancialStatementRaw).values(insert_values)
                        stmt = stmt.on_conflict_do_update(
                            constraint="uq_statements_ticker_period_item",
                            set_={
                                "value_try": stmt.excluded.value_try,
                                "fetched_at": stmt.excluded.fetched_at,
                                "item_desc_tr": stmt.excluded.item_desc_tr,
                                "item_desc_en": stmt.excluded.item_desc_en
                            }
                        )
                        db.execute(stmt)
                        rows_inserted = len(insert_values)
                    
                    # Create fetch log entry
                    log_entry = FetchLog(
                        ticker=ticker,
                        period_key=result.period_key,
                        fetched_at=fetched_at,
                        http_status=result.http_status,
                        response_size=len(json.dumps(result.data)),
                        processing_time_ms=result.response_time_ms,
                        checksum_md5=result.checksum,
                        is_new_data=True,
                        error_message=None
                    )
                    db.add(log_entry)
                    db.commit()
                
                results.append({
                    "ticker": ticker,
                    "success": result.success,
                    "error": result.error,
                    "response_time_ms": result.response_time_ms,
                    "checksum": result.checksum,
                    "rows_inserted": rows_inserted
                })
        
        return {
            "triggered_at": datetime.utcnow().isoformat(),
            "total_companies": len(tickers),
            "successful": len([r for r in results if r["success"]]),
            "failed": len([r for r in results if not r["success"]]),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"❌ Error in manual fetch: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/fetch/status")
async def get_fetch_status(
    limit: int = Query(50, description="Number of recent fetch logs to return"),
    db: Session = Depends(get_db)
):
    """Get recent fetch status and statistics"""
    try:
        from models.financial import FetchLog
        from sqlalchemy import func, desc
        
        # Recent fetch logs
        recent_logs = db.query(FetchLog)\
                       .order_by(desc(FetchLog.fetched_at))\
                       .limit(limit).all()
        
        # Statistics
        stats = db.query(
            func.count(FetchLog.id).label("total_fetches"),
            func.sum(func.case([(FetchLog.is_new_data == True, 1)], else_=0)).label("new_data_fetches"),
            func.avg(FetchLog.processing_time_ms).label("avg_processing_time"),
            func.count(func.distinct(FetchLog.ticker)).label("unique_companies")
        ).first()
        
        return {
            "statistics": {
                "total_fetches": stats.total_fetches or 0,
                "new_data_fetches": stats.new_data_fetches or 0,
                "avg_processing_time_ms": round(float(stats.avg_processing_time), 2) if stats.avg_processing_time else 0,
                "unique_companies": stats.unique_companies or 0
            },
            "recent_logs": [
                {
                    "ticker": log.ticker,
                    "period_key": log.period_key,
                    "fetched_at": log.fetched_at.isoformat(),
                    "http_status": log.http_status,
                    "is_new_data": log.is_new_data,
                    "processing_time_ms": log.processing_time_ms,
                    "error_message": log.error_message
                }
                for log in recent_logs
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting fetch status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/system/health")
async def system_health_check(db: Session = Depends(get_db)):
    """Comprehensive system health check"""
    try:
        from core.cache import redis_client
        
        health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {}
        }
        
        # Database health
        try:
            db.execute("SELECT 1")
            health["components"]["database"] = {"status": "healthy", "message": "Connected"}
        except Exception as e:
            health["components"]["database"] = {"status": "unhealthy", "message": str(e)}
            health["status"] = "unhealthy"
        
        # Cache health  
        try:
            if redis_client._connected:
                await redis_client.set("health_check", "ok", ttl=60)
                test_value = await redis_client.get("health_check")
                if test_value == "ok":
                    health["components"]["cache"] = {"status": "healthy", "message": "Connected and functional"}
                else:
                    health["components"]["cache"] = {"status": "degraded", "message": "Connected but not responding correctly"}
            else:
                health["components"]["cache"] = {"status": "unhealthy", "message": "Not connected"}
                health["status"] = "degraded"
        except Exception as e:
            health["components"]["cache"] = {"status": "unhealthy", "message": str(e)}
            health["status"] = "degraded"
        
        # İş Yatırım API health (simple connectivity check)
        try:
            async with isyatirim_client:
                # Don't actually fetch data, just check if we can connect
                health["components"]["isyatirim_api"] = {"status": "healthy", "message": "Client initialized"}
        except Exception as e:
            health["components"]["isyatirim_api"] = {"status": "unhealthy", "message": str(e)}
            health["status"] = "degraded"
        
        return health
        
    except Exception as e:
        logger.error(f"❌ Error in health check: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/benchmarks/calculate")
async def calculate_sector_benchmarks(
    sector_main: str = Query(..., description="Sector name to calculate"),
    period_key: str = Query(..., description="Period key (e.g. '2026Q1')"),
    db: Session = Depends(get_db)
):
    """Trigger calculation of sector benchmarks"""
    try:
        from services.sector_benchmarks import SectorBenchmarkService
        from core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as async_db:
            service = SectorBenchmarkService(async_db)
            results = await service.compute_sector_benchmarks(sector_main, period_key)
            
        return {
            "sector": sector_main,
            "period": period_key,
            "calculated_benchmarks_count": len(results),
            "results": [
                {
                    "ratio_code": r.ratio_code,
                    "reliability": r.reliability,
                    "median_ew": float(r.median_ew) if r.median_ew is not None else None
                }
                for r in results
            ]
        }
    except Exception as e:
        logger.error(f"❌ Error in sector benchmarks manual calculation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")