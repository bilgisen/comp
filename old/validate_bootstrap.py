"""
Bootstrap Validation Script
Validates completeness and quality after bootstrap

Usage:
    python validate_bootstrap.py
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import func, select, and_, distinct
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw, CompanyRatio, FetchLog
from models.benchmark import SectorBenchmark

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BootstrapValidator:
    """Validates bootstrap completion and data quality"""
    
    EXPECTED_MIN_COMPANIES = 580  # 95% of 610
    EXPECTED_MIN_RATIOS_PER_COMPANY = 15
    EXPECTED_MIN_SECTORS = 14
    
    def __init__(self):
        self.db: Session = SessionLocal()
        self.validation_results = []
        
    def run_all_validations(self):
        """Run all validation checks"""
        logger.info("=" * 60)
        logger.info("BOOTSTRAP VALIDATION REPORT")
        logger.info("=" * 60)
        logger.info(f"Generated: {datetime.utcnow().isoformat()}")
        logger.info("")
        
        self._validate_companies()
        self._validate_financial_data()
        self._validate_ratios()
        self._validate_benchmarks()
        self._validate_data_quality()
        self._validate_freshness()
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 60)
        
        passed = len([r for r in self.validation_results if r['passed']])
        total = len(self.validation_results)
        
        for result in self.validation_results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            logger.info(f"{status} - {result['check']}: {result['message']}")
        
        logger.info("")
        logger.info(f"Overall: {passed}/{total} checks passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            logger.info("🎉 Bootstrap validation PASSED!")
        else:
            logger.warning("⚠️ Bootstrap validation has FAILURES - review above")
        
        self.db.close()
    
    def _validate_companies(self):
        """Validate company data"""
        logger.info("1. COMPANY DATA")
        logger.info("-" * 60)
        
        total_companies = self.db.query(func.count(Company.id)).scalar()
        active_companies = self.db.query(func.count(Company.id)).filter(Company.is_active == True).scalar()
        
        # Check by financial group
        ufrs_k_count = self.db.query(func.count(Company.id)).filter(
            Company.financial_group == 'UFRS_K'
        ).scalar()
        xi_29_count = self.db.query(func.count(Company.id)).filter(
            Company.financial_group == 'XI_29'
        ).scalar()
        
        # Check sectors
        sectors = self.db.query(Company.sector_main).distinct().count()
        
        logger.info(f"  Total companies: {total_companies}")
        logger.info(f"  Active companies: {active_companies}")
        logger.info(f"  UFRS_K (Banking): {ufrs_k_count}")
        logger.info(f"  XI_29 (Industrial): {xi_29_count}")
        logger.info(f"  Unique sectors: {sectors}")
        logger.info("")
        
        self.validation_results.append({
            'check': 'Company Count',
            'passed': total_companies >= 600,
            'message': f"{total_companies} companies (expected ≥600)"
        })
        
        self.validation_results.append({
            'check': 'Sector Count',
            'passed': sectors >= self.EXPECTED_MIN_SECTORS,
            'message': f"{sectors} sectors (expected ≥{self.EXPECTED_MIN_SECTORS})"
        })
    
    def _validate_financial_data(self):
        """Validate financial statement data"""
        logger.info("2. FINANCIAL STATEMENTS")
        logger.info("-" * 60)
        
        total_rows = self.db.query(func.count(FinancialStatementRaw.id)).scalar()
        
        # Companies with data
        companies_with_data = self.db.query(
            func.count(distinct(FinancialStatementRaw.ticker))
        ).scalar()
        
        # Average rows per company
        avg_rows = total_rows / max(1, companies_with_data)
        
        # Periods covered
        periods = self.db.query(FinancialStatementRaw.period_key).distinct().count()
        
        # Recent fetch logs
        recent_fetches = self.db.query(func.count(FetchLog.id)).filter(
            FetchLog.fetched_at >= datetime.utcnow() - timedelta(hours=24)
        ).scalar()
        
        logger.info(f"  Total rows: {total_rows:,}")
        logger.info(f"  Companies with data: {companies_with_data}")
        logger.info(f"  Avg rows per company: {avg_rows:.0f}")
        logger.info(f"  Unique periods: {periods}")
        logger.info(f"  Recent fetches (24h): {recent_fetches}")
        logger.info("")
        
        self.validation_results.append({
            'check': 'Financial Data Coverage',
            'passed': companies_with_data >= self.EXPECTED_MIN_COMPANIES,
            'message': f"{companies_with_data} companies (expected ≥{self.EXPECTED_MIN_COMPANIES})"
        })
        
        self.validation_results.append({
            'check': 'Data Volume',
            'passed': total_rows >= 100000,
            'message': f"{total_rows:,} rows (expected ≥100,000)"
        })
    
    def _validate_ratios(self):
        """Validate ratio calculations"""
        logger.info("3. CALCULATED RATIOS")
        logger.info("-" * 60)
        
        total_ratios = self.db.query(func.count(CompanyRatio.id)).scalar()
        
        # Companies with ratios
        companies_with_ratios = self.db.query(
            func.count(distinct(CompanyRatio.ticker))
        ).scalar()
        
        # Average ratios per company
        avg_ratios = total_ratios / max(1, companies_with_ratios)
        
        # Ratio breakdown by category
        from services.ratio_calculator import RatioCalculator
        
        # Most common ratios
        common_ratios = self.db.query(
            CompanyRatio.ratio_code,
            func.count(CompanyRatio.id).label('count')
        ).group_by(CompanyRatio.ratio_code).order_by(func.count(CompanyRatio.id).desc()).limit(10).all()
        
        logger.info(f"  Total ratios: {total_ratios:,}")
        logger.info(f"  Companies with ratios: {companies_with_ratios}")
        logger.info(f"  Avg ratios per company: {avg_ratios:.1f}")
        logger.info("")
        logger.info("  Top 10 ratios:")
        for ratio_code, count in common_ratios:
            logger.info(f"    {ratio_code}: {count}")
        logger.info("")
        
        self.validation_results.append({
            'check': 'Ratio Coverage',
            'passed': companies_with_ratios >= self.EXPECTED_MIN_COMPANIES * 0.95,
            'message': f"{companies_with_ratios} companies (expected ≥{int(self.EXPECTED_MIN_COMPANIES * 0.95)})"
        })
        
        self.validation_results.append({
            'check': 'Ratio Density',
            'passed': avg_ratios >= self.EXPECTED_MIN_RATIOS_PER_COMPANY,
            'message': f"{avg_ratios:.1f} ratios/company (expected ≥{self.EXPECTED_MIN_RATIOS_PER_COMPANY})"
        })
    
    def _validate_benchmarks(self):
        """Validate sector benchmarks"""
        logger.info("4. SECTOR BENCHMARKS")
        logger.info("-" * 60)
        
        total_benchmarks = self.db.query(func.count(SectorBenchmark.id)).scalar()
        
        # Benchmarks by sector
        benchmarks_by_sector = self.db.query(
            SectorBenchmark.sector_main,
            func.count(SectorBenchmark.id).label('count')
        ).group_by(SectorBenchmark.sector_main).all()
        
        # Reliability distribution
        high_reliability = self.db.query(func.count(SectorBenchmark.id)).filter(
            SectorBenchmark.reliability == 'HIGH'
        ).scalar()
        medium_reliability = self.db.query(func.count(SectorBenchmark.id)).filter(
            SectorBenchmark.reliability == 'MEDIUM'
        ).scalar()
        low_reliability = self.db.query(func.count(SectorBenchmark.id)).filter(
            SectorBenchmark.reliability == 'LOW'
        ).scalar()
        
        logger.info(f"  Total benchmarks: {total_benchmarks}")
        logger.info("")
        logger.info("  Benchmarks by sector:")
        for sector, count in benchmarks_by_sector:
            logger.info(f"    {sector}: {count}")
        logger.info("")
        logger.info("  Reliability distribution:")
        logger.info(f"    HIGH: {high_reliability}")
        logger.info(f"    MEDIUM: {medium_reliability}")
        logger.info(f"    LOW: {low_reliability}")
        logger.info("")
        
        self.validation_results.append({
            'check': 'Benchmark Count',
            'passed': total_benchmarks >= 500,
            'message': f"{total_benchmarks} benchmarks (expected ≥500)"
        })
        
        self.validation_results.append({
            'check': 'Sector Coverage',
            'passed': len(benchmarks_by_sector) >= 10,
            'message': f"{len(benchmarks_by_sector)} sectors (expected ≥10)"
        })
    
    def _validate_data_quality(self):
        """Validate data quality metrics"""
        logger.info("5. DATA QUALITY")
        logger.info("-" * 60)
        
        # Average quality score
        avg_quality = self.db.query(
            func.avg(CompanyRatio.data_quality_score)
        ).filter(
            CompanyRatio.data_quality_score.isnot(None)
        ).scalar() or 0.0
        
        # Failed fetches
        total_fetch_logs = self.db.query(func.count(FetchLog.id)).scalar()
        failed_fetches = self.db.query(func.count(FetchLog.id)).filter(
            FetchLog.error_message.isnot(None)
        ).scalar()
        
        failure_rate = (failed_fetches / max(1, total_fetch_logs)) * 100
        
        # NULL ratio values
        total_ratio_records = self.db.query(func.count(CompanyRatio.id)).scalar()
        null_ratios = self.db.query(func.count(CompanyRatio.id)).filter(
            CompanyRatio.ratio_value.is_(None)
        ).scalar()
        
        null_rate = (null_ratios / max(1, total_ratio_records)) * 100
        
        logger.info(f"  Avg data quality score: {avg_quality:.2f}")
        logger.info(f"  Failed fetch rate: {failure_rate:.1f}%")
        logger.info(f"  NULL ratio rate: {null_rate:.1f}%")
        logger.info("")
        
        self.validation_results.append({
            'check': 'Data Quality Score',
            'passed': avg_quality >= 0.80,
            'message': f"{avg_quality:.2f} (expected ≥0.80)"
        })
        
        self.validation_results.append({
            'check': 'Fetch Success Rate',
            'passed': failure_rate < 10.0,
            'message': f"{100-failure_rate:.1f}% success (expected ≥90%)"
        })
    
    def _validate_freshness(self):
        """Validate data freshness"""
        logger.info("6. DATA FRESHNESS")
        logger.info("-" * 60)
        
        # Most recent fetch
        latest_fetch = self.db.query(func.max(FetchLog.fetched_at)).scalar()
        
        # Most recent ratio calculation
        latest_ratio = self.db.query(func.max(CompanyRatio.computed_at)).scalar()
        
        # Most recent benchmark
        latest_benchmark = self.db.query(func.max(SectorBenchmark.computed_at)).scalar()
        
        now = datetime.utcnow()
        
        fetch_age_hours = (now - latest_fetch).total_seconds() / 3600 if latest_fetch else 999
        ratio_age_hours = (now - latest_ratio).total_seconds() / 3600 if latest_ratio else 999
        benchmark_age_hours = (now - latest_benchmark).total_seconds() / 3600 if latest_benchmark else 999
        
        logger.info(f"  Latest fetch: {latest_fetch.isoformat() if latest_fetch else 'N/A'}")
        logger.info(f"  Latest ratio: {latest_ratio.isoformat() if latest_ratio else 'N/A'}")
        logger.info(f"  Latest benchmark: {latest_benchmark.isoformat() if latest_benchmark else 'N/A'}")
        logger.info("")
        logger.info(f"  Fetch age: {fetch_age_hours:.1f} hours")
        logger.info(f"  Ratio age: {ratio_age_hours:.1f} hours")
        logger.info(f"  Benchmark age: {benchmark_age_hours:.1f} hours")
        logger.info("")
        
        self.validation_results.append({
            'check': 'Data Freshness',
            'passed': fetch_age_hours < 48,  # Within 2 days
            'message': f"{fetch_age_hours:.1f} hours old (expected <48h)"
        })


def main():
    validator = BootstrapValidator()
    validator.run_all_validations()


if __name__ == "__main__":
    main()
