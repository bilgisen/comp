"""
Test Single Company Backfill - Debug
"""
import sys
import asyncio
from core.database import SessionLocal
from models.company import Company
from services.isyatirim_client import IsYatirimClient


async def test_single_fetch():
    """Test fetch for a single company"""
    db = SessionLocal()
    
    # Try AAGYO first
    ticker = "AAGYO"
    company = db.query(Company).filter(Company.ticker == ticker).first()
    
    if not company:
        print(f"❌ {ticker} not found")
        return
    
    print(f"\nTesting {ticker} ({company.name})")
    print(f"Financial Group: {company.financial_group}")
    print("-" * 70)
    
    async with IsYatirimClient() as client:
        # Try default 4 periods first
        periods_default = client._get_periods_to_fetch()
        print(f"\nDefault periods: {periods_default}")
        
        result = await client.fetch_mali_tablo(
            ticker=ticker,
            financial_group=company.financial_group,
            periods=periods_default
        )
        
        print(f"\nResult:")
        print(f"  Success: {result.success}")
        print(f"  HTTP Status: {result.http_status}")
        print(f"  Error: {result.error}")
        
        if result.data:
            items = result.data.get("value", [])
            print(f"  Items: {len(items)}")
            if len(items) > 0:
                print(f"\n  Sample item:")
                print(f"    {items[0]}")
        
        # Try with extended periods (8)
        print(f"\n" + "="*70)
        print("Testing with 8 periods:")
        print("="*70)
        
        y, p = periods_default[-1]
        quarter_map = {12: 9, 9: 6, 6: 3, 3: 12}
        
        extended_periods = []
        for _ in range(4):
            prev_p = quarter_map[p]
            if prev_p == 12:
                y -= 1
            p = prev_p
            extended_periods.append((y, p))
        
        all_periods = periods_default + extended_periods
        print(f"Extended periods: {all_periods}")
        
        # Can only fetch 4 at a time, so fetch the older 4
        result2 = await client.fetch_mali_tablo(
            ticker=ticker,
            financial_group=company.financial_group,
            periods=extended_periods
        )
        
        print(f"\nResult for older periods:")
        print(f"  Success: {result2.success}")
        print(f"  HTTP Status: {result2.http_status}")
        print(f"  Error: {result2.error}")
        
        if result2.data:
            items = result2.data.get("value", [])
            print(f"  Items: {len(items)}")
    
    db.close()


if __name__ == "__main__":
    asyncio.run(test_single_fetch())
