"""
Check Banking & Finance sector composition
"""
from sqlalchemy import create_engine, text
from core.config import settings

sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(sync_db_url)

print("🔍 Bankacılık & Finans Sektör Analizi")
print("=" * 100)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT 
            ticker, 
            name, 
            sector_raw,
            financial_group
        FROM companies 
        WHERE sector_main = 'Bankacılık & Finans' 
          AND is_active = TRUE
        ORDER BY name
    """))
    
    companies = list(result)
    
    print(f"\nToplam: {len(companies)} şirket\n")
    
    # Group by sector_raw
    from collections import defaultdict
    by_sector_raw = defaultdict(list)
    
    for row in companies:
        by_sector_raw[row.sector_raw or 'N/A'].append(row)
    
    for sector_raw, companies_list in sorted(by_sector_raw.items()):
        print(f"\n📊 {sector_raw} ({len(companies_list)} şirket):")
        print("-" * 100)
        for row in companies_list:
            print(f"  {row.ticker:8} {row.name[:50]:50} {row.financial_group}")

print("\n" + "=" * 100)
