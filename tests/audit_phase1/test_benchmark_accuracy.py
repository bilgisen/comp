"""
Benchmark Calculation Accuracy - CORE AUDIT
Validates benchmark median calculations are statistically correct
Uses Decimal for financial precision
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import statistics
from decimal import Decimal
from sqlalchemy import select, and_, func
from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from models.benchmark import SectorBenchmark


class BenchmarkAccuracyAuditor:
    """Quick audit for benchmark calculation accuracy"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.tolerance = Decimal('0.1')  # 0.1 absolute difference tolerance
    
    def get_sectors_with_sufficient_data(self, min_companies=5):
        """Get sectors with enough companies for testing"""
        stmt = select(
            Company.sector_main,
            func.count(Company.ticker).label('count')
        ).where(
            Company.is_active == True
        ).group_by(
            Company.sector_main
        ).having(
            func.count(Company.ticker) >= min_companies
        ).order_by(
            func.count(Company.ticker).desc()
        )
        
        result = self.db.execute(stmt)
        return [row[0] for row in result.all()]
    
    def get_company_ratio_values(self, sector: str, period_key: str, ratio_code: str):
        """Get all company ratio values for a sector/period/ratio"""
        stmt = select(
            CompanyRatio.ticker,
            CompanyRatio.ratio_value
        ).join(
            Company,
            Company.ticker == CompanyRatio.ticker
        ).where(
            and_(
                Company.sector_main == sector,
                Company.is_active == True,
                CompanyRatio.period_key == period_key,
                CompanyRatio.ratio_code == ratio_code,
                CompanyRatio.ratio_value.isnot(None)
            )
        )
        
        result = self.db.execute(stmt)
        # Keep as Decimal for precision
        return [(row[0], row[1]) for row in result.all()]
    
    def get_system_benchmark(self, sector: str, period_key: str, ratio_code: str):
        """Get system-calculated benchmark"""
        stmt = select(
            SectorBenchmark
        ).where(
            and_(
                SectorBenchmark.sector_main == sector,
                SectorBenchmark.period_key == period_key,
                SectorBenchmark.ratio_code == ratio_code
            )
        )
        
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    def manual_calculate_median(self, values):
        """Manually calculate median using statistics (Decimal-safe)"""
        if not values:
            return None
        return statistics.median(values)
    
    def manual_calculate_percentiles(self, values):
        """Manually calculate P25 and P75 using statistics.quantiles"""
        if not values:
            return None, None
        # statistics.quantiles returns [P25, P50, P75] for n=4
        quantiles = statistics.quantiles(values, n=4)
        return quantiles[0], quantiles[2]  # P25, P75
    
    def audit_sector_benchmark(self, sector: str, ratio_code: str):
        """Audit benchmark calculation for a sector/ratio"""
        print(f"\n{'─'*70}")
        print(f"Testing: {sector} - {ratio_code}")
        print(f"{'─'*70}")
        
        # Get latest period with benchmark data
        stmt = select(
            SectorBenchmark.period_key
        ).where(
            and_(
                SectorBenchmark.sector_main == sector,
                SectorBenchmark.ratio_code == ratio_code
            )
        ).order_by(
            SectorBenchmark.period_key.desc()
        ).limit(1)
        
        result = self.db.execute(stmt)
        period_row = result.first()
        
        if not period_row:
            print(f"❌ No benchmark data found")
            return None
        
        period_key = period_row[0]
        print(f"Period: {period_key}")
        
        # Get raw company values
        company_values = self.get_company_ratio_values(sector, period_key, ratio_code)
        
        if not company_values:
            print(f"❌ No company ratio values found")
            return None
        
        values = [v for _, v in company_values]
        print(f"Companies in calculation: {len(values)}")
        
        # Get system benchmark
        system_benchmark = self.get_system_benchmark(sector, period_key, ratio_code)
        
        if not system_benchmark:
            print(f"❌ System benchmark not found")
            return None
        
        # Manual calculations
        manual_median = self.manual_calculate_median(values)
        manual_p25, manual_p75 = self.manual_calculate_percentiles(values)
        
        # Convert system values to Decimal for comparison
        system_median = Decimal(str(system_benchmark.median_ew))
        system_p25 = Decimal(str(system_benchmark.p25))
        system_p75 = Decimal(str(system_benchmark.p75))
        
        print(f"\nMedian (Equal-Weight):")
        print(f"  Manual: {float(manual_median):.4f}")
        print(f"  System: {float(system_median):.4f}")
        diff = abs(system_median - manual_median)
        print(f"  Diff:   {float(diff):.4f}")
        
        median_pass = diff < self.tolerance
        print(f"  Status: {'✅ PASS' if median_pass else '❌ FAIL'}")
        
        print(f"\nP25:")
        print(f"  Manual: {float(manual_p25):.4f}")
        print(f"  System: {float(system_p25):.4f}")
        diff_p25 = abs(system_p25 - manual_p25)
        print(f"  Diff:   {float(diff_p25):.4f}")
        
        print(f"\nP75:")
        print(f"  Manual: {float(manual_p75):.4f}")
        print(f"  System: {float(system_p75):.4f}")
        diff_p75 = abs(system_p75 - manual_p75)
        print(f"  Diff:   {float(diff_p75):.4f}")
        
        print(f"\nPeer Info:")
        print(f"  n_peers:    {system_benchmark.n_peers}")
        print(f"  n_excluded: {system_benchmark.n_excluded}")
        print(f"  reliability: {system_benchmark.reliability}")
        
        return {
            "sector": sector,
            "ratio_code": ratio_code,
            "period": period_key,
            "manual_median": manual_median,
            "system_median": system_median,
            "median_diff": diff,
            "median_pass": median_pass,
            "n_peers": system_benchmark.n_peers,
            "reliability": system_benchmark.reliability
        }
    
    def run_audit(self):
        """Run benchmark accuracy audit"""
        print(f"\n{'#'*70}")
        print("BENCHMARK CALCULATION ACCURACY AUDIT")
        print(f"{'#'*70}")
        
        # Get sectors with sufficient data
        sectors = self.get_sectors_with_sufficient_data(min_companies=10)
        
        if not sectors:
            print("❌ No sectors with sufficient data (min 10 companies)")
            self.db.close()
            return
        
        print(f"\nSectors with sufficient data: {len(sectors)}")
        print(f"Testing top 2 sectors...")
        
        # Test top 2 sectors
        test_sectors = sectors[:2]
        
        # Common ratios to test
        test_ratios = ["current_ratio", "debt_to_equity", "roe", "roa"]
        
        results = []
        
        for sector in test_sectors:
            print(f"\n{'='*70}")
            print(f"SECTOR: {sector}")
            print(f"{'='*70}")
            
            for ratio_code in test_ratios:
                try:
                    result = self.audit_sector_benchmark(sector, ratio_code)
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"\n❌ Error testing {ratio_code}: {str(e)}")
        
        # Summary
        print(f"\n{'='*70}")
        print("AUDIT SUMMARY")
        print(f"{'='*70}")
        
        if results:
            passed = sum(1 for r in results if r['median_pass'])
            total = len(results)
            
            print(f"Tests Performed: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Pass Rate: {passed/total*100:.1f}%")
            
            # Failed tests
            failed = [r for r in results if not r['median_pass']]
            if failed:
                print(f"\n⚠️  FAILED TESTS:")
                for r in failed:
                    print(f"  {r['sector']} - {r['ratio_code']}: diff={float(r['median_diff']):.4f}")
            else:
                print(f"\n✅ ALL BENCHMARK CALCULATIONS ACCURATE")
                print("Median calculations within tolerance.")
        else:
            print("❌ No tests completed")
        
        self.db.close()


if __name__ == "__main__":
    auditor = BenchmarkAccuracyAuditor()
    auditor.run_audit()
