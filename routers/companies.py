"""
Company API endpoints
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, desc, select

from core.database import get_db, get_async_db
from core.cache import redis_client
from models.company import Company, CompanyMetrics
from models.financial import CompanyRatio
from services.ratio_calculator import RatioCalculator

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{ticker}/ratios")
async def get_company_ratios(
    ticker: str,
    period: Optional[str] = Query(None, description="Period key (e.g., '2026Q1')"),
    ratios: Optional[List[str]] = Query(None, description="Specific ratios to return"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get financial ratios for a company
    
    Returns all calculated ratios for the company, optionally filtered by period and ratio codes.
    """
    ticker = ticker.upper()
    
    try:
        # Check if company exists
        company_query = select(Company).where(Company.ticker == ticker)
        company_result = await db.execute(company_query)
        company = company_result.scalar_one_or_none()
        
        if not company:
            raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
        
        # Check cache first
        cache_key = f"ratios:{ticker}:{period or 'latest'}"
        cached_ratios = await redis_client.get(cache_key)
        if cached_ratios:
            logger.info(f"📋 Cache hit for {ticker} ratios")
            return cached_ratios
        
        # Build query
        query = select(CompanyRatio).where(CompanyRatio.ticker == ticker)
        
        if period:
            query = query.where(CompanyRatio.period_key == period)
        else:
            # Get latest period
            latest_period_query = select(CompanyRatio.period_key)\
                             .where(CompanyRatio.ticker == ticker)\
                             .order_by(desc(CompanyRatio.computed_at))\
                             .limit(1)
            latest_period_result = await db.execute(latest_period_query)
            latest_period = latest_period_result.first()
            if latest_period:
                query = query.where(CompanyRatio.period_key == latest_period[0])
        
        if ratios:
            query = query.where(CompanyRatio.ratio_code.in_(ratios))
        
        # Execute query
        ratio_records_result = await db.execute(query.order_by(CompanyRatio.ratio_code))
        ratio_records = ratio_records_result.scalars().all()
        
        if not ratio_records:
            raise HTTPException(
                status_code=404, 
                detail=f"No ratios found for {ticker}" + (f" in period {period}" if period else "")
            )
        
        # Get sector benchmarks for comparison
        from services.sector_benchmarks import SectorBenchmarkService
        benchmark_service = SectorBenchmarkService(db)
        
        # Format response
        result = {
            "ticker": ticker,
            "company_name": company.name,
            "sector": company.sector_main,
            "period": ratio_records[0].period_key if ratio_records else None,
            "ratios": {},
            "metadata": {
                "total_ratios": len(ratio_records),
                "last_updated": max(r.computed_at for r in ratio_records).isoformat() if ratio_records else None,
                "data_quality": {
                    "avg_score": round(sum(r.data_quality_score or 0 for r in ratio_records) / len(ratio_records), 2) if ratio_records else 0,
                    "ratios_with_quality_score": len([r for r in ratio_records if r.data_quality_score is not None])
                }
            }
        }
        
        # Fetch all sector benchmarks for this period to optimize
        benchmarks_response = await benchmark_service.get_sector_benchmarks(
            company.sector_main,
            ratio_records[0].period_key
        )
        benchmarks = benchmarks_response.get("benchmarks", {})
        
        # Process each ratio
        for ratio in ratio_records:
            benchmark = benchmarks.get(ratio.ratio_code)
            
            ratio_data = {
                "value": float(ratio.ratio_value) if ratio.ratio_value is not None else None,
                "is_ttm": ratio.is_ttm,
                "calculation_method": ratio.calculation_method,
                "data_quality_score": float(ratio.data_quality_score) if ratio.data_quality_score else None,
                "computed_at": ratio.computed_at.isoformat(),
                "sector_comparison": None
            }
            
            # Add sector comparison if benchmark available
            if benchmark and ratio.ratio_value is not None:
                sector_median = benchmark.get("median_ew")
                if sector_median is not None:
                    # Calculate percentile
                    percentile = await benchmark_service.get_company_percentile(
                        company.ticker,
                        ratio.ratio_code,
                        ratio.period_key
                    )
                    
                    percentile_value = percentile.get("percentile") if percentile else None
                    
                    ratio_data["sector_comparison"] = {
                        "sector_median": float(sector_median),
                        "company_percentile": percentile_value,
                        "vs_sector": "above" if float(ratio.ratio_value) > float(sector_median) else "below",
                        "sector_p25": float(benchmark["p25"]) if benchmark.get("p25") else None,
                        "sector_p75": float(benchmark["p75"]) if benchmark.get("p75") else None,
                        "n_peers": benchmark.get("n_peers", 0),
                        "reliability": benchmark.get("reliability", "UNKNOWN")
                    }
            
            result["ratios"][ratio.ratio_code] = ratio_data
        
        # Cache result
        await redis_client.set(cache_key, result, ttl=3600)  # 1 hour cache
        
        logger.info(f"✅ Retrieved {len(ratio_records)} ratios for {ticker}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving ratios for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{ticker}/compare")
async def compare_company(
    ticker: str,
    compare_to: str = Query(..., description="'sector' or specific ticker to compare with"),
    metrics: Optional[List[str]] = Query(None, description="Specific metrics to compare"),
    period: Optional[str] = Query(None, description="Period for comparison"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Compare company with sector or another company
    
    Provides detailed comparison analysis with percentiles and relative performance.
    """
    ticker = ticker.upper()
    
    try:
        # Validate company
        company_query = select(Company).where(Company.ticker == ticker)
        company_result = await db.execute(company_query)
        company = company_result.scalar_one_or_none()
        
        if not company:
            raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
        
        from services.comparison_service import ComparisonService
        
        comparison_service = ComparisonService(db)
        
        if compare_to.lower() == "sector":
            # Sector comparison
            result = await comparison_service.compare_with_sector(
                ticker=ticker,
                metrics=metrics,
                period=period
            )
        else:
            # Company-to-company comparison
            compare_to = compare_to.upper()
            result = await comparison_service.compare_companies(
                ticker1=ticker,
                ticker2=compare_to,
                metrics=metrics,
                period=period
            )
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error comparing {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{ticker}/trends")
async def get_company_trends(
    ticker: str,
    ratios: Optional[List[str]] = Query(None, description="Specific ratios to analyze"),
    periods: int = Query(8, description="Number of periods to analyze", ge=2, le=20),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get trend analysis for company ratios
    
    Returns historical trend data and analysis for specified ratios.
    """
    ticker = ticker.upper()
    
    try:
        # Validate company
        company_query = select(Company).where(Company.ticker == ticker)
        company_result = await db.execute(company_query)
        company = company_result.scalar_one_or_none()
        
        if not company:
            raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
        
        from services.trend_analysis import TrendAnalysisService
        
        trend_service = TrendAnalysisService(db)
        trends = await trend_service.analyze_trends(
            ticker=ticker,
            ratio_codes=ratios,
            periods=periods
        )
        
        return {
            "ticker": ticker,
            "company_name": company.name,
            "analysis_period": f"Last {periods} periods",
            "trends": trends,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error analyzing trends for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{ticker}/profile")
async def get_company_profile(
    ticker: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get comprehensive company profile
    
    Returns company information, latest metrics, and key ratios.
    """
    ticker = ticker.upper()
    
    try:
        # Get company data
        company_query = select(Company).where(Company.ticker == ticker)
        company_result = await db.execute(company_query)
        company = company_result.scalar_one_or_none()
        
        if not company:
            raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
        
        # Get latest metrics
        metrics_query = select(CompanyMetrics).where(CompanyMetrics.ticker == ticker)
        metrics_result = await db.execute(metrics_query)
        metrics = metrics_result.scalar_one_or_none()
        
        # Get key ratios (latest period)
        key_ratios = ["current_ratio", "debt_to_equity", "roe", "net_margin", "pe_ratio"]
        ratios_query = select(CompanyRatio).where(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.ratio_code.in_(key_ratios)
            )
        ).order_by(desc(CompanyRatio.computed_at)).limit(len(key_ratios))
        ratios_result = await db.execute(ratios_query)
        ratios = ratios_result.scalars().all()
        
        # Format response
        result = {
            "ticker": ticker,
            "name": company.name,
            "name_en": company.name_en,
            "sector_raw": company.sector_raw,
            "sector_main": company.sector_main,
            "financial_group": company.financial_group,
            "city": company.city,
            "website": company.website,
            "about": company.about,
            "is_active": company.is_active,
            "market_data": None,
            "key_ratios": {},
            "last_updated": company.updated_at.isoformat()
        }
        
        # Add market data if available
        if metrics:
            result["market_data"] = {
                "last_price": float(metrics.last_price) if metrics.last_price else None,
                "market_cap": metrics.market_cap,
                "shares_outstanding": metrics.shares_outstanding,
                "free_float_pct": float(metrics.free_float_pct) if metrics.free_float_pct else None,
                "volume_1d": metrics.volume_1d,
                "pe_ratio": float(metrics.pe_ratio) if metrics.pe_ratio else None,
                "pb_ratio": float(metrics.pb_ratio) if metrics.pb_ratio else None,
                "price_updated_at": metrics.price_updated_at.isoformat() if metrics.price_updated_at else None
            }
        
        # Add key ratios
        for ratio in ratios:
            result["key_ratios"][ratio.ratio_code] = {
                "value": float(ratio.ratio_value) if ratio.ratio_value else None,
                "period": ratio.period_key,
                "computed_at": ratio.computed_at.isoformat()
            }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving profile for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/{ticker}/calculate")
async def trigger_ratio_calculation(
    ticker: str,
    period: Optional[str] = Query(None, description="Specific period to calculate"),
    force: bool = Query(False, description="Force recalculation even if data exists"),
    db: Session = Depends(get_db)
):
    """
    Trigger ratio calculation for a company
    
    Admin endpoint to manually trigger ratio calculations.
    """
    ticker = ticker.upper()
    
    # Validate company
    company = db.query(Company).filter(Company.ticker == ticker).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {ticker} not found")
    
    try:
        calculator = RatioCalculator(db)
        
        if period:
            # Calculate specific period
            results = await calculator.calculate_company_ratios(ticker, period)
        else:
            # Calculate latest available period
            from models.financial import FinancialStatementRaw
            latest_period = db.query(FinancialStatementRaw.period_key)\
                             .filter(FinancialStatementRaw.ticker == ticker)\
                             .order_by(desc(FinancialStatementRaw.year), desc(FinancialStatementRaw.period))\
                             .first()
            
            if not latest_period:
                raise HTTPException(status_code=404, detail=f"No financial data found for {ticker}")
            
            results = await calculator.calculate_company_ratios(ticker, latest_period[0])
        
        # Save results to database
        successful_calculations = 0
        for result in results:
            if result.success:
                # Upsert ratio
                existing = db.query(CompanyRatio).filter(
                    and_(
                        CompanyRatio.ticker == ticker,
                        CompanyRatio.period_key == (period or latest_period[0]),
                        CompanyRatio.ratio_code == result.ratio_code
                    )
                ).first()
                
                if existing and not force:
                    continue
                
                if existing:
                    existing.ratio_value = result.value
                    existing.calculation_method = result.calculation_method
                    existing.data_quality_score = result.data_quality_score
                    existing.computed_at = datetime.utcnow()
                else:
                    ratio = CompanyRatio(
                        ticker=ticker,
                        period_key=period or latest_period[0],
                        ratio_code=result.ratio_code,
                        ratio_value=result.value,
                        is_ttm=result.calculation_method and "ttm" in result.calculation_method.lower(),
                        calculation_method=result.calculation_method,
                        data_quality_score=result.data_quality_score,
                        computed_at=datetime.utcnow()
                    )
                    db.add(ratio)
                
                successful_calculations += 1
        
        db.commit()
        
        # Invalidate cache
        await redis_client.delete_pattern(f"ratios:{ticker}:*")
        
        return {
            "ticker": ticker,
            "period": period or latest_period[0],
            "total_ratios": len(results),
            "successful": successful_calculations,
            "failed": len(results) - successful_calculations,
            "errors": [r.error for r in results if not r.success],
            "calculated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error calculating ratios for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
