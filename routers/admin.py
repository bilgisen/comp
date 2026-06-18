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
        
        async with isyatirim_client:
            for ticker in tickers:
                ticker = ticker.upper()
                result = await isyatirim_client.fetch_mali_tablo(ticker)
                
                results.append({
                    "ticker": ticker,
                    "success": result.success,
                    "error": result.error,
                    "response_time_ms": result.response_time_ms,
                    "checksum": result.checksum
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
        raise HTTPException(status_code=500, detail="Internal server error")


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