"""
Check database status - are there any records?
"""
from sqlalchemy import create_engine, text
from core.config import settings

# Create sync engine
sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(sync_db_url)

print("🔍 Checking database status...")
print("=" * 60)

with engine.connect() as conn:
    # Check companies
    result = conn.execute(text("SELECT COUNT(*) as count FROM companies"))
    companies_count = result.scalar()
    print(f"\n✅ Companies: {companies_count}")
    
    if companies_count > 0:
        result = conn.execute(text("SELECT ticker, name, sector_main, financial_group FROM companies LIMIT 5"))
        print("\n   Sample companies:")
        for row in result:
            print(f"   - {row.ticker}: {row.name} ({row.financial_group})")
    
    # Check financial_statements_raw
    result = conn.execute(text("SELECT COUNT(*) as count FROM financial_statements_raw"))
    statements_count = result.scalar()
    print(f"\n✅ Financial Statements (Raw): {statements_count}")
    
    if statements_count > 0:
        result = conn.execute(text("""
            SELECT ticker, period_key, COUNT(*) as items
            FROM financial_statements_raw
            GROUP BY ticker, period_key
            ORDER BY ticker, period_key DESC
            LIMIT 10
        """))
        print("\n   Sample data:")
        for row in result:
            print(f"   - {row.ticker} {row.period_key}: {row.items} items")
    
    # Check fetch_logs
    result = conn.execute(text("SELECT COUNT(*) as count FROM fetch_logs"))
    logs_count = result.scalar()
    print(f"\n✅ Fetch Logs: {logs_count}")
    
    if logs_count > 0:
        result = conn.execute(text("""
            SELECT ticker, period_key, fetched_at, is_new_data, http_status
            FROM fetch_logs
            ORDER BY fetched_at DESC
            LIMIT 5
        """))
        print("\n   Recent fetches:")
        for row in result:
            status = "✅ NEW" if row.is_new_data else "⚪ UNCHANGED"
            print(f"   - {row.ticker} {row.period_key}: {status} (HTTP {row.http_status})")
    
    # Check company_ratios
    result = conn.execute(text("SELECT COUNT(*) as count FROM company_ratios"))
    ratios_count = result.scalar()
    print(f"\n✅ Company Ratios: {ratios_count}")

print("\n" + "=" * 60)
print("✅ Database check complete!")
