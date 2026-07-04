"""
Quick Banking Ratio Calculation - Test for GARAN only
"""
import sys
import asyncio
from decimal import Decimal
from core.database import SessionLocal
from models.company import Company
from services.ratio_calculator import RatioCalculator


async def calculate_banking_ratios():
    """Calculate ratios for banking companies"""
    print("="*70)
    print("QUICK BANKING RATIO CALCULATION - GARAN")
    print("="*70)
    
    db = SessionLocal()
    calculator = RatioCalculator(db)
    
    tickers = ["GARAN"]
    period_key = "2026Q1"
    
    for ticker in tickers:
        print(f"\nCalculating ratios for {ticker}...")
        
        try:
            results = await calculator.calculate_company_ratios(ticker, period_key)
            
            print(f"\n{ticker} - {period_key}:")
            print("-" * 70)
            
            for result in results:
                if result.success and result.value is not None:
                    print(f"  ✅ {result.ratio_code:25s}: {result.value:>10.6f}")
                elif result.success:
                    print(f"  ⚠️  {result.ratio_code:25s}: Calculated but NULL")
                else:
                    print(f"  ❌ {result.ratio_code:25s}: {result.error}")
            
            # Count successes
            successful = len([r for r in results if r.success and r.value is not None])
            total = len(results)
            print(f"\n  Summary: {successful}/{total} ratios calculated successfully")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    db.close()


if __name__ == "__main__":
    asyncio.run(calculate_banking_ratios())
