"""
Backfill Historical Data for Companies with <4 Periods
Extends data for 39 companies that have insufficient TTM data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from datetime import datetime
from sqlalchemy import select, func
from core.database import SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw


async def main():
    print("="*70)
    print("BACKFILL HISTORICAL DATA - TTM FIX")
    print("="*70)
    
    db = SessionLocal()
    
    # Find companies with <4 periods
    stmt = select(
        FinancialStatementRaw.ticker,
        func.count(func.distinct(FinancialStatementRaw.period_key)).label('period_count')
    ).group_by(
        FinancialStatementRaw.ticker
    ).having(
        func.count(func.distinct(FinancialStatementRaw.period_key)) < 4
    )
    
    result = db.execute(stmt)
    insufficient_companies = [(row[0], row[1]) for row in result.all()]
    
    print(f"\nCompanies with <4 periods: {len(insufficient_companies)}")
    
    if not insufficient_companies:
        print("\n✅ All companies have sufficient data!")
        db.close()
        return
    
    print("\nSample companies to backfill:")
    for ticker, count in insufficient_companies[:10]:
        print(f"  {ticker}: {count} periods")
    
    # Confirmation
    print(f"\n⚠️  This will fetch historical data for {len(insufficient_companies)} companies")
    print("Estimated time: ~5-10 minutes")
    response = input("\nProceed? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("❌ Cancelled")
        db.close()
        return
    
    # Initialize client
    from services.isyatirim_client import IsYatirimClient
    
    async with IsYatirimClient() as client:
        success_count = 0
        error_count = 0
        
        for ticker, current_periods in insufficient_companies:
            try:
                # Get company info
                company = db.execute(
                    select(Company).where(Company.ticker == ticker)
                ).scalar_one_or_none()
                
                if not company:
                    print(f"⚠️  {ticker}: Company not found")
                    continue
                
                # Fetch 8 periods instead of 4
                periods_to_fetch = client._get_periods_to_fetch()
                
                # Add 4 more historical periods
                extended_periods = []
                y, p = periods_to_fetch[-1]  # Last period from default 4
                quarter_map = {12: 9, 9: 6, 6: 3, 3: 12}
                
                # Get 4 more
                for _ in range(4):
                    prev_p = quarter_map[p]
                    if prev_p == 12:
                        y -= 1
                    p = prev_p
                    extended_periods.append((y, p))
                
                all_periods = periods_to_fetch + extended_periods
                
                print(f"\n📥 Fetching {ticker} ({company.name})...")
                print(f"   Current: {current_periods} periods")
                print(f"   Fetching: {len(all_periods)} periods")
                
                # Fetch data
                result = await client.fetch_mali_tablo(
                    ticker=ticker,
                    financial_group=company.financial_group,
                    periods=all_periods
                )
                
                print(f"   API Response: success={result.success}, http={result.http_status}, error={result.error}")
                
                if not result.success:
                    print(f"   ❌ API Error: {result.error}")
                    error_count += 1
                    continue
                
                if not result.data:
                    print(f"   ⚠️  No data in response")
                    error_count += 1
                    continue
                
                items = result.data.get("value", [])
                if len(items) == 0:
                    print(f"   ⚠️  Empty data (0 items)")
                    error_count += 1
                    continue
                # Save to database synchronously
                from decimal import Decimal
                
                print(f"   Processing {len(items)} items...")
                
                for stmt_data in items:
                        try:
                            # Build period key
                            year = stmt_data.get("year")
                            period = stmt_data.get("period")
                            period_key = f"{year}Q{period//3 if period != 12 else 4}"
                            
                            # Check if exists
                            existing = db.execute(
                                select(FinancialStatementRaw).where(
                                    FinancialStatementRaw.ticker == ticker,
                                    FinancialStatementRaw.period_key == period_key,
                                    FinancialStatementRaw.item_code == stmt_data["itemCode"]
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
                                    value_try=Decimal(str(stmt_data["value"])) if stmt_data.get("value") is not None else None,
                                    fetched_at=datetime.utcnow()
                                )
                                db.add(stmt)
                        except Exception as e:
                            print(f"     Error saving statement: {e}")
                            continue
                    
                    db.commit()
                    saved = len(items)
                    print(f"   ✅ Saved {saved} records")
                    success_count += 1
                else:
                    print(f"   ⚠️  No data returned from API")
                    error_count += 1
                
                # Rate limiting
                await asyncio.sleep(3)  # 20 requests per minute = 3 seconds between
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                error_count += 1
                continue
    
    # Summary
    print(f"\n{'='*70}")
    print("BACKFILL COMPLETE")
    print(f"{'='*70}")
    print(f"Total companies: {len(insufficient_companies)}")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"\n✅ Now run ratio and benchmark recalculation for these companies")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
