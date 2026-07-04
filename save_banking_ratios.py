"""
Save Banking Ratios to Database - Quick test for GARAN, AKBNK, YKBNK
"""
import sys
import asyncio
from datetime import datetime
from decimal import Decimal
from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from services.ratio_calculator import RatioCalculator
from sqlalchemy import and_


async def save_banking_ratios():
    """Calculate and save ratios for banking companies"""
    print("="*70)
    print("SAVE BANKING RATIOS TO DATABASE")
    print("="*70)
    
    db = SessionLocal()
    calculator = RatioCalculator(db)
    
    tickers = ["GARAN", "AKBNK", "YKBNK"]
    period_key = "2026Q1"
    
    for ticker in tickers:
        print(f"\nProcessing {ticker}...")
        
        try:
            results = await calculator.calculate_company_ratios(ticker, period_key)
            
            saved_count = 0
            for result in results:
                if result.success and result.value is not None:
                    # Check if ratio already exists
                    existing = db.query(CompanyRatio).filter(
                        and_(
                            CompanyRatio.ticker == ticker,
                            CompanyRatio.period_key == period_key,
                            CompanyRatio.ratio_code == result.ratio_code
                        )
                    ).first()
                    
                    if existing:
                        # Update
                        existing.ratio_value = Decimal(str(result.value))
                        existing.is_ttm = (result.calculation_method and "TTM" in result.calculation_method)
                        existing.calculation_method = result.ratio_code
                        existing.computed_at = datetime.utcnow()
                    else:
                        # Insert
                        ratio = CompanyRatio(
                            ticker=ticker,
                            period_key=period_key,
                            ratio_code=result.ratio_code,
                            ratio_value=Decimal(str(result.value)),
                            is_ttm=(result.calculation_method and "TTM" in result.calculation_method),
                            calculation_method=result.ratio_code,
                            computed_at=datetime.utcnow()
                        )
                        db.add(ratio)
                    
                    saved_count += 1
            
            db.commit()
            print(f"  ✅ Saved {saved_count} ratios for {ticker}")
            
        except Exception as e:
            db.rollback()
            print(f"  ❌ Error: {e}")
    
    db.close()
    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(save_banking_ratios())
