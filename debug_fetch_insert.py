"""
Debug fetch and insert logic
"""
import asyncio
import logging
from services.isyatirim_client import IsYatirimClient

logging.basicConfig(level=logging.INFO)

async def debug_fetch():
    """Debug GARAN fetch and check data structure"""
    async with IsYatirimClient() as client:
        result = await client.fetch_mali_tablo(
            ticker="GARAN",
            financial_group="UFRS_K"
        )
        
        if result.success and result.data:
            items = result.data.get("value", [])
            print(f"\n📊 Total items: {len(items)}")
            
            if items:
                # Check first few items structure
                print(f"\n🔍 First 3 items structure:")
                for i, item in enumerate(items[:3], 1):
                    print(f"\n  Item {i}:")
                    print(f"    Keys: {list(item.keys())}")
                    print(f"    itemCode: {item.get('itemCode')}")
                    print(f"    itemDescTr: {item.get('itemDescTr')}")
                    print(f"    value1: {item.get('value1')} (type: {type(item.get('value1'))})")
                    print(f"    value2: {item.get('value2')} (type: {type(item.get('value2'))})")
                
                # Test value parsing
                print(f"\n🧪 Testing value parsing:")
                test_item = items[0]
                val_str = test_item.get("value1")
                print(f"  Original value1: {val_str} (type: {type(val_str)})")
                
                if val_str is not None:
                    try:
                        val_clean = val_str.strip().replace(".", "").replace(",", ".") if isinstance(val_str, str) else str(val_str)
                        value_try = float(val_clean) if val_clean else 0.0
                        print(f"  Parsed: {value_try:,.2f}")
                    except Exception as e:
                        print(f"  ❌ Parse error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_fetch())
