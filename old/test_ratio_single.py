"""Test ratio calculation for a single company"""
from core.database import SessionLocal
from models.financial import CompanyRatio, FinancialStatementRaw
from models.company import Company
from calculate_ratios_sync import SyncRatioCalculator
from datetime import datetime

def test_single_company(ticker):
    """Test ratio calculation for a single company"""
    with SessionLocal() as db:
        company = db.query(Company).filter(Company.ticker == ticker).first()
        if not company:
            print(f"Company {ticker} not found")
            return
        
        print(f"\nTesting: {ticker} - {company.name}")
        print(f"Sector: {company.sector_main}")
        print(f"Financial Group: {company.financial_group}")
        
        # Get periods
        periods = db.query(FinancialStatementRaw.period_key).filter(
            FinancialStatementRaw.ticker == ticker
        ).distinct().all()
        periods = [p[0] for p in periods]
        
        print(f"Periods: {periods}")
        
        # Calculate ratios
        calculator = SyncRatioCalculator(db)
        
        for period_key in periods[:1]:  # Only first period
            print(f"\nCalculating ratios for {period_key}...")
            
            results = calculator.calculate_company_ratios(ticker, period_key)
            
            print(f"\nResults ({len(results)} ratios):")
            for result in results:
                if result.success:
                    print(f"  ✅ {result.ratio_code}: {result.value:.4f}")
                else:
                    print(f"  ❌ {result.ratio_code}: {result.error}")
            
            # Save to database
            for result in results:
                if result.success and result.value is not None:
                    existing = db.query(CompanyRatio).filter(
                        CompanyRatio.ticker == ticker,
                        CompanyRatio.period_key == period_key,
                        CompanyRatio.ratio_code == result.ratio_code
                    ).first()
                    
                    if existing:
                        existing.ratio_value = result.value
                        existing.calculation_method = result.calculation_method
                        existing.data_quality_score = result.data_quality_score
                        existing.computed_at = datetime.now()
                    else:
                        ratio = CompanyRatio(
                            ticker=ticker,
                            period_key=period_key,
                            ratio_code=result.ratio_code,
                            ratio_value=result.value,
                            is_ttm='ttm' in (result.calculation_method or '').lower(),
                            calculation_method=result.calculation_method,
                            data_quality_score=result.data_quality_score,
                            computed_at=datetime.now()
                        )
                        db.add(ratio)
            
            db.commit()
            print(f"\nSaved {len([r for r in results if r.success])} ratios to database")

if __name__ == "__main__":
    test_single_company("A1YEN")
