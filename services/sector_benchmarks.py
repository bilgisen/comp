"""
HissePro Sector Benchmark Service
Manages sector median calculations with F1-F5 filter pipeline

Author: Kiro AI Assistant
"""

import logging
import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, text
from sqlalchemy.orm import selectinload

from models.company import Company
from models.financial import CompanyRatio
from models.benchmark import SectorBenchmark, SectorBenchmarkPeer
from core.cache import redis_client

logger = logging.getLogger(__name__)


@dataclass
class FilterResult:
    """Result of F1-F5 filter pipeline"""
    included: List[Dict[str, Any]]
    excluded: List[Dict[str, Any]]
    n_peers: int
    reliability: str
    can_compute: bool


@dataclass  
class BenchmarkResult:
    """Sector benchmark calculation result"""
    sector_main: str
    ratio_code: str
    period_key: str
    median_ew: float
    median_wt: float
    p25: float
    p75: float
    n_peers: int
    n_excluded: int
    reliability: str
    computed_at: datetime


# Economic bounds for F3 filter (sector-specific validity checks)
ECONOMIC_BOUNDS: Dict[str, Dict[str, Tuple[float, float]]] = {
    "_default": {
        "current_ratio": (0.1, 15.0),
        "acid_test_ratio": (0.05, 12.0),
        "debt_to_equity": (-2.0, 25.0),  # Negative = cash-rich companies
        "debt_ratio": (0.0, 15.0),
        "gross_margin": (-0.50, 0.95),
        "ebitda_margin": (-0.50, 0.80),
        "net_margin": (-2.00, 0.60),
        "roe": (-1.00, 1.50),
        "roa": (-0.30, 0.40),
        "pe_ratio": (0.0, 150.0),  # Negative P/E excluded (loss-making)
        "ev_ebitda": (0.0, 60.0),
        "pb_ratio": (0.0, 20.0),
    },
    
    "Bankacılık & Finans": {
        "net_interest_margin": (-0.02, 0.12),
        "loan_to_deposit": (0.30, 2.50),
        "capital_adequacy": (0.08, 0.40),  # Basel minimum 8%
        "npl_ratio": (0.0, 0.25),
        "roe": (-0.30, 0.50),
        "roa": (-0.05, 0.08),
        "pe_ratio": (0.0, 25.0),
        "pb_ratio": (0.0, 5.0),
    },
    
    "Sigortacılık": {
        "loss_ratio": (0.20, 1.20),
        "expense_ratio": (0.05, 0.50),
        "combined_ratio": (0.40, 1.40),
        "premium_growth": (-0.30, 3.00),
        "roe": (-0.30, 0.80),
        "pe_ratio": (0.0, 30.0),
    },
    
    "GYO": {
        "nav_discount": (-0.85, 0.50),
        "rental_yield": (0.01, 0.25),
        "debt_ratio": (0.0, 10.0),  # REITs can have high leverage
        "ebitda_margin": (-0.20, 0.95),
        "pe_ratio": (0.0, 50.0),
        "pb_ratio": (0.0, 5.0),
    },
    
    "Enerji & Altyapı": {
        "current_ratio": (0.1, 10.0),
        "debt_to_equity": (-1.0, 20.0),  # Infrastructure high leverage
        "ebitda_margin": (-0.20, 0.85),
        "net_margin": (-1.00, 0.60),
        "pe_ratio": (0.0, 80.0),
        "ev_ebitda": (0.0, 25.0),
    },
    
    "Teknoloji & İletişim": {
        "gross_margin": (-0.10, 0.99),
        "ebitda_margin": (-1.00, 0.80),  # Early stage can have losses
        "net_margin": (-5.00, 0.70),     # Software startups deep losses
        "pe_ratio": (0.0, 200.0),        # High growth premium
        "pb_ratio": (0.0, 30.0),
    },
}


class SectorBenchmarkService:
    """
    Manages sector benchmark calculations with advanced filtering
    
    Implements F1-F5 filter pipeline for reliable peer comparisons:
    F1: NULL/Infinite values
    F2: Minimum reporting periods (data quality)
    F3: Economic validity (sector-specific bounds)
    F4: Statistical outlier removal (Winsorization)
    F5: Minimum peer count validation
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_sector_benchmarks(
        self, 
        sector_main: str, 
        period_key: Optional[str] = None,
        ratio_codes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get sector benchmark data with caching
        
        Args:
            sector_main: Sector name (e.g., "Teknoloji & İletişim")
            period_key: Specific period (e.g., "2026Q1"), latest if None
            ratio_codes: Specific ratios, all if None
        """
        try:
            # Get latest period if not specified
            if not period_key:
                period_key = await self._get_latest_period()
            
            # Check cache first
            cache_key = f"benchmarks:{sector_main}:{period_key}"
            cached_result = await redis_client.get(cache_key)
            
            if cached_result:
                logger.debug(f"📊 Cache hit: sector benchmarks for {sector_main}")
                return cached_result
            
            # Query benchmarks from database
            query = select(SectorBenchmark).where(
                and_(
                    SectorBenchmark.sector_main == sector_main,
                    SectorBenchmark.period_key == period_key,
                    SectorBenchmark.is_stale == False
                )
            )
            
            if ratio_codes:
                query = query.where(SectorBenchmark.ratio_code.in_(ratio_codes))
            
            result = await self.db.execute(query)
            benchmarks = result.scalars().all()
            
            # Format response
            benchmark_data = {}
            for benchmark in benchmarks:
                benchmark_data[benchmark.ratio_code] = {
                    "median_ew": float(benchmark.median_ew) if benchmark.median_ew else None,
                    "median_wt": float(benchmark.median_wt) if benchmark.median_wt else None,
                    "p25": float(benchmark.p25) if benchmark.p25 else None,
                    "p75": float(benchmark.p75) if benchmark.p75 else None,
                    "n_peers": benchmark.n_peers,
                    "reliability": benchmark.reliability,
                    "computed_at": benchmark.computed_at.isoformat()
                }
            
            response = {
                "sector_main": sector_main,
                "period_key": period_key,
                "benchmarks": benchmark_data,
                "total_ratios": len(benchmark_data),
                "cache_ttl": 3600  # 1 hour
            }
            
            # Cache result
            await redis_client.setex(cache_key, 3600, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get sector benchmarks: {e}", exc_info=True)
            raise

    async def compute_sector_benchmarks(
        self, 
        sector_main: str, 
        period_key: str,
        ratio_codes: Optional[List[str]] = None
    ) -> List[BenchmarkResult]:
        """
        Compute sector benchmarks using F1-F5 filter pipeline
        
        This is the core calculation engine triggered when company data updates
        """
        try:
            logger.info(f"🧮 Computing benchmarks: {sector_main} {period_key}")
            
            # Get all ratios for this sector/period
            if not ratio_codes:
                ratio_codes = await self._get_available_ratios(sector_main, period_key)
            
            results = []
            
            for ratio_code in ratio_codes:
                try:
                    # Get peer data for this ratio
                    peers = await self._get_peer_data(sector_main, ratio_code, period_key)
                    
                    if not peers:
                        logger.warning(f"⚠️ No peer data: {sector_main} {ratio_code}")
                        continue
                    
                    # Run F1-F5 filter pipeline
                    filter_result = self._run_filter_pipeline(
                        peers, ratio_code, sector_main
                    )
                    
                    if not filter_result.can_compute:
                        logger.info(f"📊 Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
                        # Save with insufficient data flag
                        await self._save_insufficient_benchmark(
                            sector_main, ratio_code, period_key, filter_result
                        )
                        continue
                    
                    # Calculate benchmarks
                    benchmark = await self._calculate_benchmarks(
                        filter_result, sector_main, ratio_code, period_key
                    )
                    
                    # Save to database
                    await self._save_benchmark(benchmark, filter_result)
                    
                    results.append(benchmark)
                    
                    logger.debug(f"✅ Computed: {ratio_code} n={benchmark.n_peers} reliability={benchmark.reliability}")
                    
                except Exception as e:
                    logger.error(f"Failed to compute {ratio_code}: {e}")
                    continue
            
            logger.info(f"✅ Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
            
            # Invalidate cache
            await self._invalidate_cache(sector_main, period_key)
            
            return results
            
        except Exception as e:
            logger.error(f"Benchmark computation failed: {e}", exc_info=True)
            raise

    async def _get_peer_data(
        self, 
        sector_main: str, 
        ratio_code: str, 
        period_key: str
    ) -> List[Dict[str, Any]]:
        """Get peer company data for ratio calculation"""
        
        query = text("""
            SELECT 
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                COUNT(*) OVER (PARTITION BY cr.ticker) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = :sector_main
              AND cr.ratio_code = :ratio_code  
              AND cr.period_key = :period_key
              AND c.is_active = true
        """)
        
        result = await self.db.execute(query, {
            "sector_main": sector_main,
            "ratio_code": ratio_code,
            "period_key": period_key
        })
        
        return [
            {
                "ticker": row.ticker,
                "ratio_value": float(row.ratio_value) if row.ratio_value else None,
                "market_cap": float(row.market_cap) if row.market_cap else 0,
                "available_periods": row.available_periods
            }
            for row in result.fetchall()
        ]

    def _run_filter_pipeline(
        self, 
        peers: List[Dict[str, Any]], 
        ratio_code: str, 
        sector_main: str,
        min_periods: int = 3
    ) -> FilterResult:
        """
        Execute F1-F5 filter pipeline for peer validation
        
        Returns FilterResult with included/excluded peers and reliability assessment
        """
        included = []
        excluded = []
        
        for peer in peers:
            ticker = peer["ticker"]
            value = peer["ratio_value"]
            available_periods = peer["available_periods"]
            
            # F1: NULL / Infinite values
            if value is None or not math.isfinite(value):
                excluded.append({
                    "ticker": ticker,
                    "value": value,
                    "reason": "F1_NULL_OR_INFINITE"
                })
                continue
            
            # F2: Minimum reporting periods (data quality)
            if available_periods < min_periods:
                excluded.append({
                    "ticker": ticker, 
                    "value": value,
                    "reason": f"F2_INSUFFICIENT_PERIODS({available_periods})"
                })
                continue
            
            # F3: Economic validity (sector-specific bounds)
            is_valid, exclusion_reason = self._f3_economic_validity(
                ratio_code, value, sector_main
            )
            if not is_valid:
                excluded.append({
                    "ticker": ticker,
                    "value": value, 
                    "reason": f"F3_{exclusion_reason}"
                })
                continue
            
            # Passed F1-F3, add to included list for F4
            included.append({
                "ticker": ticker,
                "value": value,
                "market_cap": peer["market_cap"]
            })
        
        # F4: Statistical outlier removal (Winsorization P5-P95)
        if len(included) >= 5:
            values = [p["value"] for p in included]
            p5 = np.percentile(values, 5)
            p95 = np.percentile(values, 95)
            
            # Apply winsorization (clip to P5-P95, don't exclude)
            for peer in included:
                if peer["value"] < p5:
                    peer["value"] = p5
                    peer["winsorized"] = "P5"
                elif peer["value"] > p95:
                    peer["value"] = p95
                    peer["winsorized"] = "P95"
        
        # F5: Minimum peer count validation
        n = len(included)
        reliability = self._assess_reliability(n)
        can_compute = n >= 3
        
        return FilterResult(
            included=included,
            excluded=excluded,
            n_peers=n,
            reliability=reliability,
            can_compute=can_compute
        )

    def _f3_economic_validity(
        self, 
        ratio_code: str, 
        ratio_value: float, 
        sector_main: str
    ) -> Tuple[bool, Optional[str]]:
        """
        F3: Economic validity filter with sector-specific bounds
        
        Returns (is_valid, exclusion_reason)
        """
        # Get sector-specific bounds, fallback to default
        sector_bounds = ECONOMIC_BOUNDS.get(sector_main, {})
        default_bounds = ECONOMIC_BOUNDS["_default"]
        
        bounds = sector_bounds.get(ratio_code) or default_bounds.get(ratio_code)
        
        if bounds is None:
            # This ratio not defined for this sector
            return False, "RATIO_NOT_APPLICABLE"
        
        min_val, max_val = bounds
        
        if min_val is not None and ratio_value < min_val:
            return False, f"BELOW_ECONOMIC_MIN({min_val})"
        
        if max_val is not None and ratio_value > max_val:
            return False, f"ABOVE_ECONOMIC_MAX({max_val})"
        
        return True, None

    def _assess_reliability(self, n_peers: int) -> str:
        """Assess benchmark reliability based on peer count"""
        if n_peers >= 10:
            return "HIGH"
        elif n_peers >= 5:
            return "MEDIUM"  
        elif n_peers >= 3:
            return "LOW"
        else:
            return "INSUFFICIENT"

    async def _calculate_benchmarks(
        self, 
        filter_result: FilterResult,
        sector_main: str,
        ratio_code: str, 
        period_key: str
    ) -> BenchmarkResult:
        """Calculate equal-weight and market-cap weighted medians"""
        
        values = [p["value"] for p in filter_result.included]
        market_caps = [p["market_cap"] for p in filter_result.included]
        
        # Equal-weight median (standard median)
        median_ew = float(np.median(values))
        
        # Market-cap weighted median (weighted quantile)
        median_wt = self._weighted_quantile(values, market_caps, 0.5)
        
        # Percentiles (always equal-weight)
        p25 = float(np.percentile(values, 25))
        p75 = float(np.percentile(values, 75))
        
        return BenchmarkResult(
            sector_main=sector_main,
            ratio_code=ratio_code,
            period_key=period_key,
            median_ew=median_ew,
            median_wt=median_wt,
            p25=p25,
            p75=p75,
            n_peers=filter_result.n_peers,
            n_excluded=len(filter_result.excluded),
            reliability=filter_result.reliability,
            computed_at=datetime.utcnow()
        )

    def _weighted_quantile(
        self, 
        values: List[float], 
        weights: List[float], 
        quantile: float
    ) -> float:
        """Calculate weighted quantile (e.g., market-cap weighted median)"""
        
        # Handle edge cases
        if not values or not weights:
            return 0.0
        
        if len(values) != len(weights):
            raise ValueError("Values and weights must have same length")
        
        # Convert to numpy arrays
        values = np.array(values)
        weights = np.array(weights)
        
        # Handle zero/negative weights
        weights = np.maximum(weights, 0.01)  # Minimum weight
        
        # Sort by values
        sorted_indices = np.argsort(values)
        sorted_values = values[sorted_indices]
        sorted_weights = weights[sorted_indices]
        
        # Calculate cumulative weights
        cumsum_weights = np.cumsum(sorted_weights)
        total_weight = cumsum_weights[-1]
        
        # Find quantile position
        target_weight = quantile * total_weight
        
        # Find index where cumulative weight exceeds target
        idx = np.searchsorted(cumsum_weights, target_weight, side='right')
        
        if idx == 0:
            return float(sorted_values[0])
        elif idx >= len(sorted_values):
            return float(sorted_values[-1])
        else:
            # Linear interpolation between adjacent values
            w1 = cumsum_weights[idx-1] if idx > 0 else 0
            w2 = cumsum_weights[idx]
            v1 = sorted_values[idx-1]
            v2 = sorted_values[idx]
            
            # Interpolation factor
            alpha = (target_weight - w1) / (w2 - w1)
            return float(v1 + alpha * (v2 - v1))

    async def _save_benchmark(
        self, 
        benchmark: BenchmarkResult, 
        filter_result: FilterResult
    ):
        """Save benchmark to database with audit trail"""
        
        # Upsert main benchmark record
        from sqlalchemy.dialects.postgresql import insert
        
        benchmark_stmt = insert(SectorBenchmark).values(
            sector_main=benchmark.sector_main,
            ratio_code=benchmark.ratio_code,
            period_key=benchmark.period_key,
            median_ew=benchmark.median_ew,
            median_wt=benchmark.median_wt,
            p25=benchmark.p25,
            p75=benchmark.p75,
            n_peers=benchmark.n_peers,
            n_excluded=benchmark.n_excluded,
            reliability=benchmark.reliability,
            computed_at=benchmark.computed_at,
            is_stale=False
        )
        
        benchmark_stmt = benchmark_stmt.on_conflict_do_update(
            index_elements=['sector_main', 'ratio_code', 'period_key'],
            set_={
                'median_ew': benchmark_stmt.excluded.median_ew,
                'median_wt': benchmark_stmt.excluded.median_wt,
                'p25': benchmark_stmt.excluded.p25,
                'p75': benchmark_stmt.excluded.p75,
                'n_peers': benchmark_stmt.excluded.n_peers,
                'n_excluded': benchmark_stmt.excluded.n_excluded,
                'reliability': benchmark_stmt.excluded.reliability,
                'computed_at': benchmark_stmt.excluded.computed_at,
                'is_stale': False
            }
        ).returning(SectorBenchmark.id)
        
        result = await self.db.execute(benchmark_stmt)
        benchmark_id = result.scalar_one()
        
        # Clear existing peer records
        delete_peers = select(SectorBenchmarkPeer).where(
            SectorBenchmarkPeer.benchmark_id == benchmark_id
        )
        await self.db.execute(delete_peers)
        
        # Insert peer audit trail
        peer_records = []
        
        # Included peers
        for peer in filter_result.included:
            peer_records.append({
                'benchmark_id': benchmark_id,
                'ticker': peer['ticker'],
                'ratio_value': peer['value'],
                'is_included': True,
                'exclusion_reason': peer.get('winsorized')  # P5/P95 if winsorized
            })
        
        # Excluded peers  
        for peer in filter_result.excluded:
            peer_records.append({
                'benchmark_id': benchmark_id,
                'ticker': peer['ticker'],
                'ratio_value': peer.get('value'),
                'is_included': False,
                'exclusion_reason': peer['reason']
            })
        
        if peer_records:
            await self.db.execute(
                insert(SectorBenchmarkPeer),
                peer_records
            )
        
        await self.db.commit()

    async def _save_insufficient_benchmark(
        self, 
        sector_main: str,
        ratio_code: str, 
        period_key: str,
        filter_result: FilterResult
    ):
        """Save benchmark record for insufficient peer scenarios"""
        
        from sqlalchemy.dialects.postgresql import insert
        
        stmt = insert(SectorBenchmark).values(
            sector_main=sector_main,
            ratio_code=ratio_code,
            period_key=period_key,
            median_ew=None,
            median_wt=None,
            p25=None,
            p75=None,
            n_peers=filter_result.n_peers,
            n_excluded=len(filter_result.excluded),
            reliability="INSUFFICIENT",
            computed_at=datetime.utcnow(),
            is_stale=False
        ).on_conflict_do_update(
            index_elements=['sector_main', 'ratio_code', 'period_key'],
            set_={
                'n_peers': stmt.excluded.n_peers,
                'n_excluded': stmt.excluded.n_excluded,
                'reliability': "INSUFFICIENT",
                'computed_at': stmt.excluded.computed_at,
                'is_stale': False
            }
        )
        
        await self.db.execute(stmt)
        await self.db.commit()

    async def _get_available_ratios(
        self, 
        sector_main: str, 
        period_key: str
    ) -> List[str]:
        """Get list of ratios available for this sector/period"""
        
        query = text("""
            SELECT DISTINCT cr.ratio_code
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = :sector_main
              AND cr.period_key = :period_key
              AND c.is_active = true
        """)
        
        result = await self.db.execute(query, {
            "sector_main": sector_main,
            "period_key": period_key
        })
        
        return [row.ratio_code for row in result.fetchall()]

    async def _get_latest_period(self) -> str:
        """Get the latest available period key"""
        
        query = text("""
            SELECT period_key 
            FROM company_ratios 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        result = await self.db.execute(query)
        row = result.fetchone()
        
        return row.period_key if row else "2026Q1"

    async def _invalidate_cache(self, sector_main: str, period_key: str):
        """Invalidate Redis cache for sector benchmarks"""
        cache_key = f"benchmarks:{sector_main}:{period_key}"
        await redis_client.delete(cache_key)
        
        # Also invalidate wildcard patterns
        pattern = f"benchmarks:{sector_main}:*"
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)

    async def invalidate_sector_benchmarks(self, ticker: str):
        """
        Invalidate benchmarks when a company's data is updated
        
        Called from ratio calculation worker when new ratios are computed
        """
        try:
            # Get company sector
            query = select(Company.sector_main).where(Company.ticker == ticker)
            result = await self.db.execute(query)
            sector_main = result.scalar_one_or_none()
            
            if not sector_main:
                logger.warning(f"No sector found for {ticker}")
                return
            
            # Mark benchmarks as stale for recomputation
            update_stmt = text("""
                UPDATE sector_benchmarks 
                SET is_stale = true 
                WHERE sector_main = :sector_main
            """)
            
            await self.db.execute(update_stmt, {"sector_main": sector_main})
            await self.db.commit()
            
            # Invalidate cache
            await self._invalidate_cache(sector_main, "*")
            
            logger.info(f"✅ Invalidated benchmarks for sector: {sector_main}")
            
        except Exception as e:
            logger.error(f"Failed to invalidate benchmarks: {e}", exc_info=True)

    async def get_company_percentile(
        self, 
        ticker: str, 
        ratio_code: str, 
        period_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate company's percentile rank within sector for specific ratio
        
        Returns percentile rank (0-100) and comparison context
        """
        try:
            # Get company data
            company_query = select(Company).where(Company.ticker == ticker)
            company_result = await self.db.execute(company_query)
            company = company_result.scalar_one_or_none()
            
            if not company:
                return None
            
            # Get latest period if not specified
            if not period_key:
                period_key = await self._get_latest_period()
            
            # Get company ratio value
            ratio_query = select(CompanyRatio.ratio_value).where(
                and_(
                    CompanyRatio.ticker == ticker,
                    CompanyRatio.ratio_code == ratio_code,
                    CompanyRatio.period_key == period_key
                )
            )
            ratio_result = await self.db.execute(ratio_query)
            company_value = ratio_result.scalar_one_or_none()
            
            if company_value is None:
                return None
            
            # Get all peer values for percentile calculation
            peers = await self._get_peer_data(
                company.sector_main, ratio_code, period_key
            )
            
            if len(peers) < 3:
                return None
            
            # Apply F1-F3 filters (but not F4 winsorization for percentile calc)
            valid_values = []
            for peer in peers:
                value = peer["ratio_value"]
                if value is None or not math.isfinite(value):
                    continue
                
                is_valid, _ = self._f3_economic_validity(
                    ratio_code, value, company.sector_main
                )
                if is_valid:
                    valid_values.append(value)
            
            if len(valid_values) < 3:
                return None
            
            # Calculate percentile rank
            valid_values = np.array(valid_values)
            percentile = (np.sum(valid_values <= company_value) / len(valid_values)) * 100
            
            # Get sector benchmark for comparison
            benchmark_query = select(SectorBenchmark).where(
                and_(
                    SectorBenchmark.sector_main == company.sector_main,
                    SectorBenchmark.ratio_code == ratio_code,
                    SectorBenchmark.period_key == period_key
                )
            )
            benchmark_result = await self.db.execute(benchmark_query)
            benchmark = benchmark_result.scalar_one_or_none()
            
            response = {
                "ticker": ticker,
                "ratio_code": ratio_code,
                "company_value": float(company_value),
                "percentile": round(percentile, 1),
                "peer_count": len(valid_values),
                "vs_sector": "above" if percentile > 50 else "below"
            }
            
            if benchmark:
                response["sector_median"] = float(benchmark.median_ew)
                response["sector_p25"] = float(benchmark.p25) if benchmark.p25 else None
                response["sector_p75"] = float(benchmark.p75) if benchmark.p75 else None
                response["reliability"] = benchmark.reliability
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to calculate percentile: {e}", exc_info=True)
            return None