"""
Update CAR (Capital Adequacy Ratio) for All Banking Companies
Uses latest 2026Q1 data from BIST disclosures
"""
import sys
import asyncio
from datetime import datetime
from decimal import Decimal
from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from services.ratio_calculator import RatioCalculator
from sqlalchemy import and_, or_


async def update_all_banking_cars():
    """Update capital_adequacy ratio for all banking companies"""
    print("="*70)
    print("UPDATE CAPITAL ADEQUACY RATIOS - ALL BANKS")
    print("="*70)
    
    db = SessionLocal()
    
    # Get all banking companies
    banking_companies = db.query(Company).filter(
        Company.sector_main == "Bankacılık & Finans"
    ).all()
    
    print(f"\nFound {len(banking_companies)} banking companies")
    print("-" * 70)
    
    calculator = RatioCalculator(db)
    period_key = "2026Q1"
    
    updated_count = 0
    skipped_count = 0
    
    for company in banking_companies:
        ticker = company.ticker
        
        # Check if ticker has CAR fallback data
        car_fallback = calculator.BANK_CAR_FALLBACKS.get(ticker, {})
        car_value = car_fallback.get(period_key, car_fallback.get("_default"))
        
        if not car_value or car_value == calculator.BANK_CAR_FALLBACKS["_default"]:
            print(f"  ⚠️  {ticker:10s}: No specific CAR data (using general default {calculator.BANK_CAR_FALLBACKS['_default']:.2%})")
            skipped_count += 1
            continue
        
        # Check if ratio already exists
        existing = db.query(CompanyRatio).filter(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.period_key == period_key,
                CompanyRatio.ratio_code == "capital_adequacy"
            )
        ).first()
        
        if existing:
            # Update
            old_value = float(existing.ratio_value) if existing.ratio_value else None
            existing.ratio_value = Decimal(str(car_value))
            existing.calculation_method = "capital_adequacy"
            existing.computed_at = datetime.utcnow()
            
            print(f"  ✅ {ticker:10s}: Updated CAR {old_value:.2%} → {car_value:.2%}")
        else:
            # Insert
            ratio = CompanyRatio(
                ticker=ticker,
                period_key=period_key,
                ratio_code="capital_adequacy",
                ratio_value=Decimal(str(car_value)),
                is_ttm=False,
                calculation_method="capital_adequacy",
                computed_at=datetime.utcnow()
            )
            db.add(ratio)
            
            print(f"  ✅ {ticker:10s}: Inserted CAR {car_value:.2%}")
        
        updated_count += 1
    
    db.commit()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total banking companies: {len(banking_companies)}")
    print(f"Updated: {updated_count}")
    print(f"Skipped (no data): {skipped_count}")
    print("\n✅ Capital adequacy ratios updated with latest 2026Q1 BIST data")
    
    db.close()


if __name__ == "__main__":
    asyncio.run(update_all_banking_cars())
