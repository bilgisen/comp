"""
Check GARAN specific data
"""
from sqlalchemy import create_engine, text
from core.config import settings

sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(sync_db_url)

print("🔍 Checking GARAN data...")
print("=" * 60)

with engine.connect() as conn:
    # Check financial statements
    result = conn.execute(text("""
        SELECT period_key, COUNT(*) as items
        FROM financial_statements_raw
        WHERE ticker = 'GARAN'
        GROUP BY period_key
        ORDER BY period_key DESC
    """))
    
    print("\n📊 Financial Statements:")
    garan_statements = list(result)
    if garan_statements:
        for row in garan_statements:
            print(f"   {row.period_key}: {row.items} items")
    else:
        print("   ⚠️ No data found")
    
    # Check ratios
    result = conn.execute(text("""
        SELECT period_key, COUNT(*) as ratio_count
        FROM company_ratios
        WHERE ticker = 'GARAN'
        GROUP BY period_key
        ORDER BY period_key DESC
    """))
    
    print("\n📈 Calculated Ratios:")
    garan_ratios = list(result)
    if garan_ratios:
        for row in garan_ratios:
            print(f"   {row.period_key}: {row.ratio_count} ratios")
    else:
        print("   ⚠️ No ratios calculated")
    
    # If ratios exist, show sample
    if garan_ratios:
        result = conn.execute(text("""
            SELECT ratio_code, ratio_value, is_ttm
            FROM company_ratios
            WHERE ticker = 'GARAN' AND period_key = '2026Q1'
            ORDER BY ratio_code
            LIMIT 10
        """))
        print("\n   Sample ratios (2026Q1):")
        for row in result:
            ttm = " (TTM)" if row.is_ttm else ""
            print(f"   - {row.ratio_code}: {row.ratio_value:.4f}{ttm}")

print("\n" + "=" * 60)
