"""
Test Backfill for Just a Few Companies
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import asyncio
from datetime import datetime
from decimal import Decimal
from sqlalchemy import select, and_
from core.database import SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw


async def main():
    print("="*70)
    print("TEST BACKFILL - FEW COMPANIES")
    print("="*70)
    
    db = SessionLocal()
    
    # Test with just 3 companies
    test_tickers = ["AAGYO", "AKHAN", "ARENA"]
    
    from services.isyatirim_client import IsYatirimClient
    
    async with IsYatirimClient() as client:
        success_count = 0
        error_count = 0
        
        for ticker in test_tickers:
            try:
                company = db.query(Company).filter(Company.ticker == ticker).first()
                
                if not company:
                    print(f"⚠️  {ticker}: Company not found")
                    continue
                
                # Fetch default 4 periods
                periods = client._get_periods_to_fetch()
                
                print(f"\n📥 Fetching {ticker} ({company.name})...")
                print(f"   Periods: {periods}")
                
                result = await client.fetch_mali_tablo(
                    ticker=ticker,
                    financial_group=company.financial_group,
                    periods=periods
                )
                
                print(f"   Success: {result.success}")
                print(f"   HTTP: {result.http_status}")
                print(f"   Error: {result.error}")
                
                if result.success and result.data:
                    items = result.data.get("value", [])
                    print(f"   Items: {len(items)}")
                    
                    # Save to database
                    saved_count = 0
                    for stmt_data in items:
                        try:
                            year = None
                            period = None
                            
                            # Parse from values
                            for i in range(1, 5):
                                val_key = f"value{i}"
                                if stmt_data.get(val_key) is not None:
                                    # This period has data
                                    year = periods[i-1][0]
                                    period = periods[i-1][1]
                                    period_key = f"{year}Q{period//3 if period != 12 else 4}"
                                    
                                    # Check if exists
                                    existing = db.execute(
                                        select(FinancialStatementRaw).where(
                                            and_(
                                                FinancialStatementRaw.ticker == ticker,
                                                FinancialStatementRaw.period_key == period_key,
                                                FinancialStatementRaw.item_code == stmt_data["itemCode"]
                                            )
                                        )
                                    ).scalar_one_or_none()
                                    
                                    if not existing:
                                        stmt = FinancialStatementRaw(
                                            ticker=ticker,
                                            period_key=period_key,
                                            year=year,
                                            period=period,
                                            financial_group=company.financial_group,
                                            item_code=stmt_data["itemCode"],
                                            item_desc_tr=stmt_data.get("itemDescTr"),
                                            item_desc_en=stmt_data.get("itemDescEng"),
                                            value_try=Decimal(str(stmt_data[val_key])),
                                            fetched_at=datetime.utcnow()
                                        )
                                        db.add(stmt)
                                        saved_count += 1
                        except Exception as e:
                            print(f"     Error: {e}")
                            continue
                    
                    db.commit()
                    print(f"   ✅ Saved {saved_count} new records")
                    success_count += 1
                else:
                    print(f"   ❌ Failed")
                    error_count += 1
                
                # Rate limiting
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                error_count += 1
                continue
    
    print(f"\n{'='*70}")
    print(f"Complete: {success_count} success, {error_count} errors")
    
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
