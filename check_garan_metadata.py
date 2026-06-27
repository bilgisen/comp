"""Check GARAN company metadata"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.company import Company
from core.config import settings

# Create sync engine
sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(sync_db_url)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

try:
    # Query GARAN
    garan = db.query(Company).filter(Company.ticker == "GARAN").first()
    
    if garan:
        print("✅ GARAN found in database:")
        print(f"   Ticker: {garan.ticker}")
        print(f"   Name: {garan.name}")
        print(f"   Sector Main: {garan.sector_main}")
        print(f"   Financial Group: {garan.financial_group}")
        print(f"   Is Active: {garan.is_active}")
        print(f"   Market Cap: {garan.market_cap}")
    else:
        print("❌ GARAN not found in companies table")
        
        # Check if any bank exists
        banks = db.query(Company).filter(Company.financial_group == "UFRS_K").limit(5).all()
        print(f"\n📊 Banks in database (UFRS_K): {len(banks)}")
        for bank in banks:
            print(f"   - {bank.ticker}: {bank.name}")
            
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
