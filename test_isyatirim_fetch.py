"""
Test İş Yatırım API fetch
"""
import asyncio
import logging
from services.isyatirim_client import IsYatirimClient

logging.basicConfig(level=logging.INFO)

async def test_fetch():
    """Test GARAN fetch"""
    async with IsYatirimClient() as client:
        print("\n🧪 Testing İş Yatırım API fetch for GARAN...")
        print("=" * 60)
        
        # Fetch GARAN (Bank - UFRS_K)
        result = await client.fetch_mali_tablo(
            ticker="GARAN",
            currency="TRY",
            financial_group="UFRS_K"
        )
        
        print(f"\n📊 Result:")
        print(f"  Success: {result.success}")
        print(f"  Ticker: {result.ticker}")
        print(f"  Period: {result.period_key}")
        print(f"  HTTP Status: {result.http_status}")
        print(f"  Response Time: {result.response_time_ms}ms")
        print(f"  Checksum: {result.checksum}")
        
        if result.success and result.data:
            items = result.data.get("value", [])
            print(f"  Items Count: {len(items)}")
            
            if items:
                print(f"\n📝 Sample items (first 5):")
                for i, item in enumerate(items[:5], 1):
                    itemCode = item.get("itemCode", "?")
                    itemDescTr = item.get("itemDescTr", "?")
                    value1 = item.get("value1", 0)
                    # Convert to float first
                    try:
                        val = float(value1) if value1 else 0
                        print(f"  {i}. {itemCode}: {itemDescTr} = {val:,.0f}")
                    except (ValueError, TypeError):
                        print(f"  {i}. {itemCode}: {itemDescTr} = {value1}")
        else:
            print(f"  ❌ Error: {result.error}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_fetch())
