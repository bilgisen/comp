"""
Scoring Worker Module
Batch processing for company scores

Usage:
    python -m services.scoring.worker --period 2026Q1
    python -m services.scoring.worker --all-periods
"""

import argparse
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from models.benchmark import SectorBenchmark
from models.score import CompanyScore, CompanyScoreDetail, GlobalBenchmark
from services.scoring.engine import compute_company_score, CompanyScoreResult
from services.scoring.pillar_config import get_pillar_config, GENEL_PILLARS, get_all_ratio_codes, get_genel_ratio_codes

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ScoringWorker:
    """
    Batch scoring worker that computes scores for all companies.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def run_scoring_for_period(self, period_key: str) -> Dict[str, Any]:
        """
        Compute scores for all active companies for a specific period.
        
        Args:
            period_key: Period key (e.g., '2026Q1')
        
        Returns:
            Summary statistics
        """
        logger.info(f"Starting scoring for period: {period_key}")
        start_time = datetime.utcnow()
        
        # Load all companies with their ratios
        companies = self._load_companies()
        logger.info(f"Loaded {len(companies)} active companies")
        
        # Load all ratios for this period
        company_ratios = self._load_company_ratios(period_key)
        logger.info(f"Loaded ratios for {len(company_ratios)} companies")
        
        # Load sector benchmarks
        sector_benchmarks = self._load_sector_benchmarks(period_key)
        logger.info(f"Loaded {len(sector_benchmarks)} sector benchmarks")
        
        # Compute or load global benchmarks
        global_benchmarks = self._compute_global_benchmarks(period_key, company_ratios)
        logger.info(f"Computed {len(global_benchmarks)} global benchmarks")
        
        # Score each company
        results = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
        for company in companies:
            try:
                ticker = company.ticker
                sector_main = company.sector_main
                
                if ticker not in company_ratios:
                    results['skipped'] += 1
                    continue
                
                # Get company's ratios
                ratios = company_ratios[ticker]
                
                # Get sector peer data
                sektor_peer_values, sektor_median_data, n_peers_sektor = self._prepare_sector_data(
                    sector_main, ratios, sector_benchmarks, company_ratios
                )
                
                # Get global peer data
                genel_peer_values, genel_median_data, n_peers_genel = self._prepare_genel_data(
                    ratios, global_benchmarks, company_ratios
                )
                
                # Compute scores
                score_result = compute_company_score(
                    ticker=ticker,
                    period_key=period_key,
                    sector_main=sector_main,
                    company_ratios=ratios,
                    sektor_peer_values=sektor_peer_values,
                    sektor_median_data=sektor_median_data,
                    n_peers_sektor=n_peers_sektor,
                    genel_peer_values=genel_peer_values,
                    genel_median_data=genel_median_data,
                    n_peers_genel=n_peers_genel,
                )
                
                # Save to database
                self._save_score(score_result)
                
                results['success'] += 1
                
                if results['success'] % 50 == 0:
                    logger.info(f"Progress: {results['success']} companies scored")
                
            except Exception as e:
                logger.error(f"Error scoring {company.ticker}: {e}")
                results['failed'] += 1
                results['errors'].append(f"{company.ticker}: {str(e)}")
        
        self.db.commit()
        
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"Scoring complete: {results['success']} success, {results['failed']} failed, {results['skipped']} skipped")
        logger.info(f"Elapsed time: {elapsed:.1f} seconds")
        
        return results
    
    def _load_companies(self) -> List[Company]:
        """Load all active companies."""
        return self.db.query(Company).filter(Company.is_active == True).all()
    
    def _load_company_ratios(self, period_key: str) -> Dict[str, Dict[str, float]]:
        """Load all ratios for a period, grouped by ticker."""
        query = text("""
            SELECT ticker, ratio_code, ratio_value
            FROM company_ratios
            WHERE period_key = :period_key
              AND ratio_value IS NOT NULL
        """)
        
        rows = self.db.execute(query, {"period_key": period_key}).fetchall()
        
        company_ratios: Dict[str, Dict[str, float]] = defaultdict(dict)
        for row in rows:
            ticker, ratio_code, ratio_value = row
            company_ratios[ticker][ratio_code] = float(ratio_value)
        
        return dict(company_ratios)
    
    def _load_sector_benchmarks(self, period_key: str) -> Dict[str, Dict[str, Dict]]:
        """Load sector benchmarks grouped by sector and ratio."""
        query = text("""
            SELECT sector_main, ratio_code, median_ew, p25, p75, reliability, n_peers
            FROM sector_benchmarks
            WHERE period_key = :period_key
              AND is_stale = FALSE
        """)
        
        rows = self.db.execute(query, {"period_key": period_key}).fetchall()
        
        benchmarks: Dict[str, Dict[str, Dict]] = defaultdict(dict)
        for row in rows:
            sector_main, ratio_code, median_ew, p25, p75, reliability, n_peers = row
            benchmarks[sector_main][ratio_code] = {
                'median_ew': float(median_ew) if median_ew else None,
                'p25': float(p25) if p25 else None,
                'p75': float(p75) if p75 else None,
                'reliability': reliability,
                'n_peers': n_peers,
            }
        
        return dict(benchmarks)
    
    def _compute_global_benchmarks(
        self, 
        period_key: str,
        company_ratios: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict]:
        """Compute global (market-wide) benchmarks."""
        ratio_codes = get_genel_ratio_codes()
        
        global_benchmarks: Dict[str, Dict] = {}
        
        for ratio_code in ratio_codes:
            values = []
            for ticker, ratios in company_ratios.items():
                if ratio_code in ratios:
                    val = ratios[ratio_code]
                    if val is not None and np.isfinite(val):
                        values.append(val)
            
            if len(values) >= 3:
                arr = np.array(values)
                global_benchmarks[ratio_code] = {
                    'median_ew': float(np.median(arr)),
                    'p25': float(np.percentile(arr, 25)),
                    'p75': float(np.percentile(arr, 75)),
                    'reliability': 'HIGH' if len(values) >= 10 else 'MEDIUM',
                    'n_peers': len(values),
                }
        
        return global_benchmarks
    
    def _prepare_sector_data(
        self,
        sector_main: str,
        company_ratios: Dict[str, float],
        sector_benchmarks: Dict[str, Dict[str, Dict]],
        all_company_ratios: Dict[str, Dict[str, float]],
    ) -> tuple[Dict[str, List[float]], Dict[str, Dict], int]:
        """Prepare sector peer data for scoring."""
        
        # Get ratio codes for this sector
        ratio_codes = get_all_ratio_codes(sector_main)
        
        # Get peer values for each ratio
        peer_values: Dict[str, List[float]] = {}
        for ratio_code in ratio_codes:
            values = []
            for ticker, ratios in all_company_ratios.items():
                # Check if company is in same sector (simplified - would need sector lookup)
                if ratio_code in ratios:
                    val = ratios[ratio_code]
                    if val is not None and np.isfinite(val):
                        values.append(val)
            peer_values[ratio_code] = values
        
        # Get median data from benchmarks
        median_data = sector_benchmarks.get(sector_main, {})
        
        # Count peers
        n_peers = len([
            t for t, r in all_company_ratios.items()
            if any(rc in r for rc in ratio_codes)
        ])
        
        return peer_values, median_data, n_peers
    
    def _prepare_genel_data(
        self,
        company_ratios: Dict[str, float],
        global_benchmarks: Dict[str, Dict],
        all_company_ratios: Dict[str, Dict[str, float]],
    ) -> tuple[Dict[str, List[float]], Dict[str, Dict], int]:
        """Prepare global (market-wide) peer data for scoring."""
        
        ratio_codes = get_genel_ratio_codes()
        
        # Get peer values for each ratio
        peer_values: Dict[str, List[float]] = {}
        for ratio_code in ratio_codes:
            values = []
            for ticker, ratios in all_company_ratios.items():
                if ratio_code in ratios:
                    val = ratios[ratio_code]
                    if val is not None and np.isfinite(val):
                        values.append(val)
            peer_values[ratio_code] = values
        
        # Use global benchmarks as median data
        n_peers = len(all_company_ratios)
        
        return peer_values, global_benchmarks, n_peers
    
    def _save_score(self, result: CompanyScoreResult) -> None:
        """Save score result to database."""
        
        # Check if score exists
        existing = self.db.query(CompanyScore).filter(
            CompanyScore.ticker == result.ticker,
            CompanyScore.period_key == result.period_key
        ).first()
        
        if existing:
            # Update existing
            existing.score_sektor = result.score_sektor
            existing.score_genel = result.score_genel
            existing.reliability_sektor = result.reliability_sektor
            existing.reliability_genel = result.reliability_genel
            existing.n_peers_sektor = result.n_peers_sektor
            existing.n_peers_genel = result.n_peers_genel
            existing.pillar_coverage = result.pillar_coverage
            existing.data_quality_score = result.data_quality_score
            existing.computed_at = datetime.utcnow()
            existing.is_stale = False
            
            # Update pillar scores
            for pr in result.pillar_scores:
                if pr.pillar_score is not None:
                    setattr(existing, f"score_{pr.pillar_name}", pr.pillar_score)
            
            score_id = existing.id
            
            # Delete old details
            self.db.query(CompanyScoreDetail).filter(
                CompanyScoreDetail.score_id == score_id
            ).delete()
        
        else:
            # Create new
            score = CompanyScore(
                ticker=result.ticker,
                period_key=result.period_key,
                score_sektor=result.score_sektor,
                score_genel=result.score_genel,
                reliability_sektor=result.reliability_sektor,
                reliability_genel=result.reliability_genel,
                n_peers_sektor=result.n_peers_sektor,
                n_peers_genel=result.n_peers_genel,
                pillar_coverage=result.pillar_coverage,
                data_quality_score=result.data_quality_score,
                computed_at=datetime.utcnow(),
            )
            
            # Set pillar scores
            for pr in result.pillar_scores:
                if pr.pillar_score is not None:
                    setattr(score, f"score_{pr.pillar_name}", pr.pillar_score)
            
            self.db.add(score)
            self.db.flush()  # Get ID
            score_id = score.id
        
        # Add details
        for detail in result.score_details:
            score_detail = CompanyScoreDetail(
                score_id=score_id,
                ticker=result.ticker,
                period_key=result.period_key,
                ratio_code=detail.ratio_code,
                ratio_value=detail.ratio_value,
                peer_median=detail.peer_median,
                peer_p25=detail.peer_p25,
                peer_p75=detail.peer_p75,
                ratio_score=detail.ratio_score,
                ratio_score_raw=detail.ratio_score_raw,
                pillar=detail.pillar,
                scope=detail.scope,
                higher_is_better=detail.higher_is_better,
                reliability=detail.reliability,
                computed_at=datetime.utcnow(),
            )
            self.db.add(score_detail)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scoring Worker")
    parser.add_argument("--period", type=str, help="Period key (e.g., 2026Q1)")
    parser.add_argument("--all-periods", action="store_true", help="Score all periods")
    args = parser.parse_args()
    
    db = SessionLocal()
    
    try:
        worker = ScoringWorker(db)
        
        if args.all_periods:
            # Get all periods with ratios
            periods = db.execute(text("""
                SELECT DISTINCT period_key 
                FROM company_ratios 
                ORDER BY period_key DESC
            """)).fetchall()
            
            for (period_key,) in periods:
                logger.info(f"\n{'='*50}")
                logger.info(f"Processing period: {period_key}")
                logger.info(f"{'='*50}")
                worker.run_scoring_for_period(period_key)
        
        elif args.period:
            worker.run_scoring_for_period(args.period)
        
        else:
            # Default: score latest period
            latest_period = db.execute(text("""
                SELECT MAX(period_key) FROM company_ratios
            """)).scalar()
            
            if latest_period:
                worker.run_scoring_for_period(latest_period)
            else:
                logger.error("No periods found in company_ratios")
                sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
