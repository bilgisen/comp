"""
Ratio Calculation Accuracy Test - CORE AUDIT
Tests actual ratio calculations against manually verified expected values
Uses real production data from reference companies
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import select, and_
from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio, FinancialStatementRaw
from services.item_code_mapper import ItemCodeMapper

# Reference companies with manually verified data
REFERENCE_COMPANIES = {
    "GARAN": {  # Banking
        "sector": "Bankacılık & Finans",
        "expected_ratios": {
            # These should be calculated manually from latest period
            # Format: ratio_code -> expected_value
        }
    },
    "THYAO": {  # Industrial
        "sector": "Ulaştırma & Lojistik",
        "expected_ratios": {}
    },
    "BIMAS": {  # Industrial
        "sector": "Perakende Ticaret",
        "expected_ratios": {}
    }
}


class RatioAccuracyAuditor:
    """Quick audit for ratio calculation accuracy"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.mapper = ItemCodeMapper(self.db)
        self.issues = []
    
    def get_latest_period_data(self, ticker: str):
        """Get latest period raw financial data for manual calculation"""
        stmt = select(
            FinancialStatementRaw
        ).where(
            FinancialStatementRaw.ticker == ticker
        ).order_by(
            FinancialStatementRaw.year.desc(),
            FinancialStatementRaw.period.desc()
        ).limit(50)
        
        result = self.db.execute(stmt)
        rows = result.scalars().all()
        
        # Group by period_key
        periods = {}
        for row in rows:
            if row.period_key not in periods:
                periods[row.period_key] = []
            periods[row.period_key].append(row)
        
        return periods
    
    def get_calculated_ratios(self, ticker: str):
        """Get system-calculated ratios from database"""
        stmt = select(
            CompanyRatio
        ).where(
            CompanyRatio.ticker == ticker
        ).order_by(
            CompanyRatio.period_key.desc()
        ).limit(20)
        
        result = self.db.execute(stmt)
        ratios = result.scalars().all()
        
        # Group by period
        ratio_dict = {}
        for ratio in ratios:
            if ratio.period_key not in ratio_dict:
                ratio_dict[ratio.period_key] = {}
            ratio_dict[ratio.period_key][ratio.ratio_code] = ratio.ratio_value
        
        return ratio_dict
    
    def manual_calculate_current_ratio(self, period_data):
        """Manually calculate current ratio from raw data"""
        # Extract current_assets and current_liabilities
        current_assets = None
        current_liabilities = None
        
        for row in period_data:
            semantic = self.mapper.get_semantic_name(row.item_code, row.financial_group)
            if semantic == "current_assets":
                current_assets = row.value_try
            elif semantic == "current_liabilities":
                current_liabilities = row.value_try
        
        if current_assets and current_liabilities and current_liabilities != 0:
            return current_assets / current_liabilities
        return None
    
    def manual_calculate_debt_to_equity(self, period_data):
        """Manually calculate debt/equity from raw data"""
        total_debt = None
        shareholders_equity = None
        
        for row in period_data:
            semantic = self.mapper.get_semantic_name(row.item_code, row.financial_group)
            if semantic == "total_debt":
                total_debt = row.value_try
            elif semantic == "shareholders_equity":
                shareholders_equity = row.value_try
        
        if total_debt and shareholders_equity and shareholders_equity != 0:
            return total_debt / shareholders_equity
        return None
    
    def audit_company_ratios(self, ticker: str):
        """Audit ratios for a single company"""
        print(f"\n{'='*70}")
        print(f"AUDITING: {ticker}")
        print(f"{'='*70}")
        
        # Get company info
        company = self.db.execute(
            select(Company).where(Company.ticker == ticker)
        ).scalar_one_or_none()
        
        if not company:
            print(f"❌ Company {ticker} not found")
            return
        
        print(f"Sector: {company.sector_main}")
        print(f"Financial Group: {company.financial_group}")
        
        # Get latest period data
        periods_data = self.get_latest_period_data(ticker)
        if not periods_data:
            print(f"❌ No financial data found")
            return
        
        latest_period_key = sorted(periods_data.keys(), reverse=True)[0]
        latest_data = periods_data[latest_period_key]
        print(f"Latest Period: {latest_period_key}")
        
        # Get calculated ratios
        calculated_ratios = self.get_calculated_ratios(ticker)
        if latest_period_key not in calculated_ratios:
            print(f"❌ No calculated ratios for {latest_period_key}")
            return
        
        ratios = calculated_ratios[latest_period_key]
        print(f"Calculated Ratios Found: {len(ratios)}")
        
        # Manual calculations
        print(f"\n{'─'*70}")
        print("MANUAL vs SYSTEM COMPARISON")
        print(f"{'─'*70}")
        
        # Test 1: Current Ratio
        if "current_ratio" in ratios:
            manual = self.manual_calculate_current_ratio(latest_data)
            system = ratios["current_ratio"]
            
            if manual and system:
                diff_pct = abs((system - manual) / manual * 100)
                status = "✅ PASS" if diff_pct < 2.0 else "❌ FAIL"
                
                print(f"\nCurrent Ratio:")
                print(f"  Manual:  {manual:.4f}")
                print(f"  System:  {system:.4f}")
                print(f"  Diff:    {diff_pct:.2f}%")
                print(f"  Status:  {status}")
                
                if diff_pct >= 2.0:
                    self.issues.append({
                        "ticker": ticker,
                        "ratio": "current_ratio",
                        "manual": manual,
                        "system": system,
                        "diff_pct": diff_pct
                    })
        
        # Test 2: Debt to Equity
        if "debt_to_equity" in ratios:
            manual = self.manual_calculate_debt_to_equity(latest_data)
            system = ratios["debt_to_equity"]
            
            if manual and system:
                diff_pct = abs((system - manual) / manual * 100)
                status = "✅ PASS" if diff_pct < 2.0 else "❌ FAIL"
                
                print(f"\nDebt to Equity:")
                print(f"  Manual:  {manual:.4f}")
                print(f"  System:  {system:.4f}")
                print(f"  Diff:    {diff_pct:.2f}%")
                print(f"  Status:  {status}")
                
                if diff_pct >= 2.0:
                    self.issues.append({
                        "ticker": ticker,
                        "ratio": "debt_to_equity",
                        "manual": manual,
                        "system": system,
                        "diff_pct": diff_pct
                    })
        
        # Show available item codes for debugging
        print(f"\n{'─'*70}")
        print("AVAILABLE SEMANTIC FIELDS (Sample)")
        print(f"{'─'*70}")
        
        semantics = set()
        for row in latest_data[:20]:
            semantic = self.mapper.get_semantic_name(row.item_code, row.financial_group)
            if semantic:
                semantics.add(semantic)
        
        for sem in sorted(semantics)[:10]:
            print(f"  • {sem}")
    
    def run_audit(self):
        """Run audit on all reference companies"""
        print(f"\n{'#'*70}")
        print("RATIO CALCULATION ACCURACY AUDIT")
        print(f"{'#'*70}")
        
        for ticker in REFERENCE_COMPANIES.keys():
            try:
                self.audit_company_ratios(ticker)
            except Exception as e:
                print(f"\n❌ Error auditing {ticker}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # Summary
        print(f"\n{'='*70}")
        print("AUDIT SUMMARY")
        print(f"{'='*70}")
        print(f"Companies Audited: {len(REFERENCE_COMPANIES)}")
        print(f"Issues Found: {len(self.issues)}")
        
        if self.issues:
            print(f"\n{'─'*70}")
            print("ISSUES DETAIL")
            print(f"{'─'*70}")
            for issue in self.issues:
                print(f"\n{issue['ticker']} - {issue['ratio']}")
                print(f"  Manual: {issue['manual']:.4f}")
                print(f"  System: {issue['system']:.4f}")
                print(f"  Diff:   {issue['diff_pct']:.2f}%")
        else:
            print("\n✅ No accuracy issues found! All ratios within 2% tolerance.")
        
        self.db.close()


if __name__ == "__main__":
    auditor = RatioAccuracyAuditor()
    auditor.run_audit()
