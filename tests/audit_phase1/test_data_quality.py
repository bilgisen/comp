"""
Data Quality Check - CORE AUDIT
Quick assessment of data completeness, NULL rates, and coverage
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import select, func, and_
from core.database import SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw, CompanyRatio
from models.benchmark import SectorBenchmark


class DataQualityAuditor:
    """Quick data quality assessment"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def check_company_coverage(self):
        """Check how many companies have data"""
        print(f"\n{'='*70}")
        print("COMPANY DATA COVERAGE")
        print(f"{'='*70}")
        
        # Total active companies
        total_companies = self.db.execute(
            select(func.count(Company.ticker)).where(Company.is_active == True)
        ).scalar()
        
        # Companies with financial data
        companies_with_data = self.db.execute(
            select(func.count(func.distinct(FinancialStatementRaw.ticker)))
        ).scalar()
        
        # Companies with ratios
        companies_with_ratios = self.db.execute(
            select(func.count(func.distinct(CompanyRatio.ticker)))
        ).scalar()
        
        print(f"Total Active Companies:     {total_companies}")
        print(f"Companies with Raw Data:    {companies_with_data} ({companies_with_data/total_companies*100:.1f}%)")
        print(f"Companies with Ratios:      {companies_with_ratios} ({companies_with_ratios/total_companies*100:.1f}%)")
        
        # Coverage status
        if companies_with_data < total_companies * 0.9:
            print(f"\n⚠️  WARNING: Only {companies_with_data/total_companies*100:.1f}% of companies have financial data")
        else:
            print(f"\n✅ Good coverage: {companies_with_data/total_companies*100:.1f}% of companies have data")
        
        return {
            "total": total_companies,
            "with_data": companies_with_data,
            "with_ratios": companies_with_ratios
        }
    
    def check_period_completeness(self):
        """Check how many periods each company has"""
        print(f"\n{'='*70}")
        print("PERIOD COMPLETENESS")
        print(f"{'='*70}")
        
        # Get period count per company
        stmt = select(
            FinancialStatementRaw.ticker,
            func.count(func.distinct(FinancialStatementRaw.period_key)).label('period_count')
        ).group_by(
            FinancialStatementRaw.ticker
        )
        
        result = self.db.execute(stmt)
        period_counts = [(row[0], row[1]) for row in result.all()]
        
        # Statistics
        if period_counts:
            counts = [c[1] for c in period_counts]
            avg_periods = sum(counts) / len(counts)
            min_periods = min(counts)
            max_periods = max(counts)
            
            # Companies with <4 periods (insufficient for TTM)
            insufficient = [t for t, c in period_counts if c < 4]
            
            print(f"Average Periods per Company: {avg_periods:.1f}")
            print(f"Min Periods: {min_periods}")
            print(f"Max Periods: {max_periods}")
            print(f"Companies with <4 periods: {len(insufficient)} (insufficient for TTM)")
            
            if insufficient:
                print(f"\n⚠️  WARNING: {len(insufficient)} companies have insufficient data for TTM")
                print("Sample:", insufficient[:5])
            else:
                print(f"\n✅ All companies have sufficient periods")
        
        return period_counts
    
    def check_sector_distribution(self):
        """Check sector distribution"""
        print(f"\n{'='*70}")
        print("SECTOR DISTRIBUTION")
        print(f"{'='*70}")
        
        # Count by sector
        stmt = select(
            Company.sector_main,
            func.count(Company.ticker).label('count')
        ).where(
            Company.is_active == True
        ).group_by(
            Company.sector_main
        ).order_by(
            func.count(Company.ticker).desc()
        )
        
        result = self.db.execute(stmt)
        sectors = result.all()
        
        print(f"\n{'Sector':<35} {'Companies':>10}")
        print(f"{'-'*35} {'-'*10}")
        
        for sector, count in sectors:
            print(f"{sector:<35} {count:>10}")
        
        # Check for NULL sectors
        null_sectors = self.db.execute(
            select(func.count(Company.ticker)).where(
                and_(
                    Company.is_active == True,
                    Company.sector_main.is_(None)
                )
            )
        ).scalar()
        
        if null_sectors > 0:
            print(f"\n⚠️  WARNING: {null_sectors} companies have NULL sector_main")
        
        return sectors
    
    def check_benchmark_coverage(self):
        """Check benchmark calculation coverage"""
        print(f"\n{'='*70}")
        print("BENCHMARK COVERAGE")
        print(f"{'='*70}")
        
        # Total sectors
        total_sectors = self.db.execute(
            select(func.count(func.distinct(Company.sector_main))).where(
                Company.is_active == True
            )
        ).scalar()
        
        # Sectors with benchmarks
        sectors_with_benchmarks = self.db.execute(
            select(func.count(func.distinct(SectorBenchmark.sector_main)))
        ).scalar()
        
        # Total benchmarks
        total_benchmarks = self.db.execute(
            select(func.count()).select_from(SectorBenchmark)
        ).scalar()
        
        print(f"Total Active Sectors:       {total_sectors}")
        print(f"Sectors with Benchmarks:    {sectors_with_benchmarks}")
        print(f"Total Benchmark Records:    {total_benchmarks}")
        
        if sectors_with_benchmarks < total_sectors:
            missing = total_sectors - sectors_with_benchmarks
            print(f"\n⚠️  WARNING: {missing} sectors missing benchmark data")
        else:
            print(f"\n✅ All sectors have benchmark data")
        
        # Check reliability distribution
        stmt = select(
            SectorBenchmark.reliability,
            func.count().label('count')
        ).group_by(
            SectorBenchmark.reliability
        )
        
        result = self.db.execute(stmt)
        reliability_dist = result.all()
        
        print(f"\nReliability Distribution:")
        for reliability, count in reliability_dist:
            print(f"  {reliability}: {count}")
        
        return {
            "total_sectors": total_sectors,
            "with_benchmarks": sectors_with_benchmarks,
            "total_records": total_benchmarks
        }
    
    def check_null_rates(self):
        """Check NULL rates in financial data"""
        print(f"\n{'='*70}")
        print("NULL RATE ANALYSIS")
        print(f"{'='*70}")
        
        # Total records
        total_records = self.db.execute(
            select(func.count()).select_from(FinancialStatementRaw)
        ).scalar()
        
        # NULL value_try
        null_values = self.db.execute(
            select(func.count()).select_from(FinancialStatementRaw).where(
                FinancialStatementRaw.value_try.is_(None)
            )
        ).scalar()
        
        null_pct = (null_values / total_records * 100) if total_records > 0 else 0
        
        print(f"Total Records:     {total_records:,}")
        print(f"NULL Values:       {null_values:,} ({null_pct:.2f}%)")
        
        if null_pct > 5.0:
            print(f"\n⚠️  WARNING: {null_pct:.2f}% NULL rate is high")
        else:
            print(f"\n✅ NULL rate is acceptable: {null_pct:.2f}%")
        
        return {"total": total_records, "null": null_values, "null_pct": null_pct}
    
    def check_duplicate_records(self):
        """Check for duplicate records"""
        print(f"\n{'='*70}")
        print("DUPLICATE CHECK")
        print(f"{'='*70}")
        
        # Find duplicates (same ticker, period, item_code)
        stmt = select(
            FinancialStatementRaw.ticker,
            FinancialStatementRaw.period_key,
            FinancialStatementRaw.item_code,
            func.count().label('count')
        ).group_by(
            FinancialStatementRaw.ticker,
            FinancialStatementRaw.period_key,
            FinancialStatementRaw.item_code
        ).having(
            func.count() > 1
        )
        
        result = self.db.execute(stmt)
        duplicates = result.all()
        
        print(f"Duplicate Records Found: {len(duplicates)}")
        
        if duplicates:
            print(f"\n⚠️  WARNING: {len(duplicates)} duplicate records found")
            print("Sample duplicates:")
            for ticker, period, item_code, count in duplicates[:5]:
                print(f"  {ticker} | {period} | {item_code} | count={count}")
        else:
            print(f"\n✅ No duplicates found")
        
        return duplicates
    
    def run_audit(self):
        """Run complete data quality audit"""
        print(f"\n{'#'*70}")
        print("DATA QUALITY AUDIT")
        print(f"{'#'*70}")
        
        results = {}
        
        try:
            results['coverage'] = self.check_company_coverage()
            results['periods'] = self.check_period_completeness()
            results['sectors'] = self.check_sector_distribution()
            results['benchmarks'] = self.check_benchmark_coverage()
            results['null_rates'] = self.check_null_rates()
            results['duplicates'] = self.check_duplicate_records()
            
            # Overall assessment
            print(f"\n{'='*70}")
            print("OVERALL ASSESSMENT")
            print(f"{'='*70}")
            
            issues = []
            
            if results['coverage']['with_data'] < results['coverage']['total'] * 0.9:
                issues.append("Low data coverage")
            
            if results['null_rates']['null_pct'] > 5.0:
                issues.append("High NULL rate")
            
            if results['duplicates']:
                issues.append("Duplicate records found")
            
            if results['benchmarks']['with_benchmarks'] < results['benchmarks']['total_sectors']:
                issues.append("Missing benchmark data for some sectors")
            
            if issues:
                print(f"\n⚠️  ISSUES FOUND:")
                for issue in issues:
                    print(f"  • {issue}")
            else:
                print(f"\n✅ DATA QUALITY IS GOOD")
                print("No critical issues found.")
            
        except Exception as e:
            print(f"\n❌ Error during audit: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.db.close()


if __name__ == "__main__":
    auditor = DataQualityAuditor()
    auditor.run_audit()
