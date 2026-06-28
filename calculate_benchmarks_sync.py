"""
Sync Sector Benchmark Calculator
Calculate sector benchmarks using F1-F5 filter pipeline
Uses sync sessions for reliable transaction management
"""

import logging
import math
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import numpy as np
from sqlalchemy import select, and_, text
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from models.benchmark import SectorBenchmark, SectorBenchmarkPeer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('benchmark_calculation.log'),
        logging.StreamHandler()
    ]
)
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
        "debt_to_equity": (-2.0, 25.0),
        "debt_ratio": (0.0, 15.0),
        "gross_margin": (-0.50, 0.95),
        "ebitda_margin": (-0.50, 0.80),
        "net_margin": (-2.00, 0.60),
        "roe": (-1.00, 1.50),
        "roa": (-0.30, 0.40),
        "pe_ratio": (0.0, 150.0),
        "ev_ebitda": (0.0, 60.0),
        "pb_ratio": (0.0, 20.0),
    },
    
    "Bankacılık & Finans": {
        "net_interest_margin": (-0.02, 0.12),
        "loan_to_deposit": (0.30, 2.50),
        "capital_adequacy": (0.08, 0.40),
        "npl_ratio": (0.0, 0.25),
        "roe": (-0.30, 0.50),
        "roa": (-0.05, 0.08),
        "pe_ratio": (0.0, 25.0),
        "pb_ratio": (0.0, 5.0),
    },
}


class SyncBenchmarkCalculator:
    """Sync benchmark calculator with reliable transaction management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def compute_sector_benchmarks(
        self, 
        sector_main: str, 
        period_key: str,
        ratio_codes: Optional[List[str]] = None
    ) -> List[BenchmarkResult]:
        """
        Compute sector benchmarks using F1-F5 filter pipeline (sync version)
        """
        try:
            logger.info(f"Computing benchmarks: {sector_main} {period_key}")
            
            # Get all ratios for this sector/period
            if not ratio_codes:
                ratio_codes = self._get_available_ratios(sector_main, period_key)
            
            results = []
            
            for ratio_code in ratio_codes:
                try:
                    # Get peer data for this ratio
                    peers = self._get_peer_data(sector_main, ratio_code, period_key)
                    
                    if not peers:
                        logger.warning(f"No peer data: {sector_main} {ratio_code}")
                        continue
                    
                    # Run F1-F5 filter pipeline
                    filter_result = self._run_filter_pipeline(
                        peers, ratio_code, sector_main
                    )
                    
                    if not filter_result.can_compute:
                        logger.info(f"Insufficient peers for {ratio_code}: n={filter_result.n_peers}")
                        continue
                    
                    # Calculate benchmarks
                    benchmark = self._calculate_benchmarks(
                        filter_result, sector_main, ratio_code, period_key
                    )
                    
                    # Save to database
                    self._save_benchmark(benchmark, filter_result)
                    
                    results.append(benchmark)
                    
                    logger.debug(f"Computed: {ratio_code} n={benchmark.n_peers} reliability={benchmark.reliability}")
                    
                except Exception as e:
                    logger.error(f"Failed to compute {ratio_code}: {e}")
                    continue
            
            logger.info(f"Benchmarks computed: {len(results)}/{len(ratio_codes)} ratios")
            
            return results
            
        except Exception as e:
            logger.error(f"Benchmark computation failed: {e}", exc_info=True)
            raise
    
    def _get_peer_data(
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
                (
                    SELECT COUNT(*) 
                    FROM company_ratios cr2 
                    WHERE cr2.ticker = cr.ticker 
                      AND cr2.ratio_code = :ratio_code
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = :sector_main
              AND cr.ratio_code = :ratio_code  
              AND cr.period_key = :period_key
              AND c.is_active = true
        """)
        
        result = self.db.execute(query, {
            "sector_main": sector_main,
            "ratio_code": ratio_code,
            "period_key": period_key
        })
        
        return [
            {
                "ticker": row.ticker,
                "ratio_value": float(row.ratio_value) if row.ratio_value is not None else None,
                "market_cap": float(row.market_cap) if row.market_cap else 0,
                "available_periods": row.available_periods
            }
            for row in result.fetchall()
        ]
    
    def _get_available_ratios(
        self, 
        sector_main: str, 
        period_key: str
    ) -> List[str]:
        """Get list of ratio codes available for this sector/period"""
        
        query = text("""
            SELECT DISTINCT cr.ratio_code
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = :sector_main
              AND cr.period_key = :period_key
              AND c.is_active = true
            ORDER BY cr.ratio_code
        """)
        
        result = self.db.execute(query, {
            "sector_main": sector_main,
            "period_key": period_key
        })
        
        return [row.ratio_code for row in result.fetchall()]
    
    def _run_filter_pipeline(
        self, 
        peers: List[Dict[str, Any]], 
        ratio_code: str, 
        sector_main: str,
        min_periods: int = 1
    ) -> FilterResult:
        """
        Execute F1-F5 filter pipeline for peer validation
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
    
    def _calculate_benchmarks(
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
        """
        Calculate weighted quantile (e.g., weighted median)
        
        Args:
            values: Data values
            weights: Corresponding weights (market caps)
            quantile: Quantile to compute (0.5 = median)
        """
        if not values or not weights:
            return 0.0
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            # Fall back to equal-weight if all weights are zero
            return float(np.percentile(values, quantile * 100))
        
        normalized_weights = [w / total_weight for w in weights]
        
        # Sort by values
        sorted_indices = np.argsort(values)
        sorted_values = [values[i] for i in sorted_indices]
        sorted_weights = [normalized_weights[i] for i in sorted_indices]
        
        # Calculate cumulative weights
        cumulative = 0.0
        for i, (value, weight) in enumerate(zip(sorted_values, sorted_weights)):
            cumulative += weight
            if cumulative >= quantile:
                return float(value)
        
        return float(sorted_values[-1])
    
    def _save_benchmark(
        self, 
        benchmark: BenchmarkResult, 
        filter_result: FilterResult
    ):
        """Save benchmark to database"""
        
        # Check if benchmark already exists
        existing = self.db.query(SectorBenchmark).filter(
            and_(
                SectorBenchmark.sector_main == benchmark.sector_main,
                SectorBenchmark.ratio_code == benchmark.ratio_code,
                SectorBenchmark.period_key == benchmark.period_key
            )
        ).first()
        
        if existing:
            # Update existing
            existing.median_ew = benchmark.median_ew
            existing.median_wt = benchmark.median_wt
            existing.p25 = benchmark.p25
            existing.p75 = benchmark.p75
            existing.n_peers = benchmark.n_peers
            existing.n_excluded = benchmark.n_excluded
            existing.reliability = benchmark.reliability
            existing.computed_at = benchmark.computed_at
            existing.is_stale = False
        else:
            # Create new
            new_benchmark = SectorBenchmark(
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
            self.db.add(new_benchmark)
        
        self.db.commit()


def calculate_all_benchmarks():
    """Main function to calculate benchmarks for all sectors"""
    logger.info("=" * 60)
    logger.info("SYNC BENCHMARK CALCULATION STARTING")
    logger.info("=" * 60)
    
    start_time = datetime.utcnow()
    
    # Get all sector-period combinations with ratios
    with SessionLocal() as db:
        query = text("""
            SELECT DISTINCT c.sector_main, cr.period_key
            FROM companies c
            JOIN company_ratios cr ON c.ticker = cr.ticker
            WHERE c.is_active = TRUE
            ORDER BY c.sector_main, cr.period_key DESC
        """)
        
        result = db.execute(query)
        sector_periods = result.fetchall()
    
    logger.info(f"Found {len(sector_periods)} sector-period combinations")
    
    total_benchmarks = 0
    failed_sectors = 0
    
    for sector_main, period_key in sector_periods:
        try:
            # Create a fresh session for each sector-period
            with SessionLocal() as db:
                calculator = SyncBenchmarkCalculator(db)
                benchmarks = calculator.compute_sector_benchmarks(
                    sector_main, period_key
                )
                
                total_benchmarks += len(benchmarks)
                
                logger.info(f"Computed {len(benchmarks)} benchmarks for {sector_main} {period_key}")
        
        except Exception as e:
            logger.error(f"Error computing benchmarks for {sector_main} {period_key}: {e}")
            failed_sectors += 1
            continue
    
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds() / 60
    
    logger.info("=" * 60)
    logger.info("BENCHMARK CALCULATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Duration: {duration:.1f} minutes")
    logger.info(f"Total benchmarks: {total_benchmarks}")
    logger.info(f"Failed sectors: {failed_sectors}")
    logger.info("=" * 60)


if __name__ == "__main__":
    calculate_all_benchmarks()
