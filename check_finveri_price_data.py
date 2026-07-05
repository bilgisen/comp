"""Check if finveri has price data in the shared database"""
from sqlalchemy import text, inspect
from core.database import SessionLocal, engine

with SessionLocal() as db:
    # List all tables
    inspector = inspect(engine)
    all_tables = inspector.get_table_names()
    
    print("\n📊 All Tables in Database:")
    price_related = []
    for table in sorted(all_tables):
        if any(keyword in table.lower() for keyword in ['price', 'quote', 'market', 'ticker', 'instrument', 'history']):
            price_related.append(table)
            print(f"  ✓ {table}")
        else:
            print(f"    {table}")
    
    print(f"\n💰 Price-Related Tables: {len(price_related)}")
    
    # Check each price-related table for data
    for table in price_related:
        try:
            count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            sample = db.execute(text(f"SELECT * FROM {table} LIMIT 1")).first()
            
            if count > 0:
                print(f"\n  📈 {table}: {count:,} rows")
                if sample:
                    columns = sample._mapping.keys()
                    print(f"     Columns: {', '.join(list(columns)[:10])}")
            else:
                print(f"\n  ⚠️  {table}: EMPTY")
        except Exception as e:
            print(f"\n  ❌ {table}: Error - {str(e)[:100]}")
