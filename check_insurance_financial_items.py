"""Check what financial statement items insurance companies have"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Get ANSGR's financial items for latest period
    items = db.execute(text("""
        SELECT item_code, item_desc_tr, value_try
        FROM financial_statements_raw
        WHERE ticker = 'ANSGR' AND period_key = '2026Q1'
        ORDER BY item_code
    """)).fetchall()
    
    print("\n📊 ANSGR - 2026Q1 Financial Statement Items:")
    print(f"{'Code':<10} {'Name':<50} {'Value':>15}")
    print("-" * 80)
    
    for code, name, value in items:
        value_str = f"{value:,.0f}" if value else "0"
        name_display = name if name else ""
        print(f"{code:<10} {name_display:<50} {value_str:>15}")
    
    print(f"\nTotal items: {len(items)}")
    
    # Check for key profitability items
    print("\n🔍 Looking for profitability items:")
    profit_keywords = ['kar', 'zarar', 'net', 'dönem', 'gelir']
    
    for code, name, value in items:
        if name:
            name_lower = name.lower()
            if any(kw in name_lower for kw in profit_keywords):
                value_str = f"{value:,.0f}" if value else "0"
                print(f"  {code:<10} {name:<50} {value_str:>15}")
