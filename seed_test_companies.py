"""
Seed test companies to database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.company import Company
from core.database import Base

# Create sync engine
sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(sync_db_url)
SessionLocal = sessionmaker(bind=engine)

def seed_companies():
    """Add test companies"""
    db = SessionLocal()
    
    test_companies = [
        {
            "ticker": "GARAN",
            "name": "T. Garanti Bankası A.Ş.",
            "name_en": "Garanti BBVA",
            "sector_raw": "Bankacılık",
            "sector_main": "Bankacılık & Finans",
            "financial_group": "UFRS_K",
            "is_active": True
        },
        {
            "ticker": "YKBNK",
            "name": "Yapı ve Kredi Bankası A.Ş.",
            "name_en": "Yapı Kredi Bank",
            "sector_raw": "Bankacılık",
            "sector_main": "Bankacılık & Finans",
            "financial_group": "UFRS_K",
            "is_active": True
        },
        {
            "ticker": "AKBNK",
            "name": "Akbank T.A.Ş.",
            "name_en": "Akbank",
            "sector_raw": "Bankacılık",
            "sector_main": "Bankacılık & Finans",
            "financial_group": "UFRS_K",
            "is_active": True
        },
        {
            "ticker": "THYAO",
            "name": "Türk Hava Yolları A.O.",
            "name_en": "Turkish Airlines",
            "sector_raw": "Havayolu",
            "sector_main": "Ulaştırma & Lojistik",
            "financial_group": "XI_29",
            "is_active": True
        },
        {
            "ticker": "BIMAS",
            "name": "BİM Birleşik Mağazalar A.Ş.",
            "name_en": "BIM",
            "sector_raw": "Perakende",
            "sector_main": "Tüketim & Perakende & Tekstil",
            "financial_group": "XI_29",
            "is_active": True
        }
    ]
    
    for comp_data in test_companies:
        # Check if exists
        existing = db.query(Company).filter(Company.ticker == comp_data["ticker"]).first()
        if existing:
            print(f"✅ {comp_data['ticker']} already exists")
            continue
        
        # Create new
        company = Company(**comp_data)
        db.add(company)
        print(f"➕ Added {comp_data['ticker']}: {comp_data['name']}")
    
    db.commit()
    db.close()
    print(f"\n✅ Seeding complete!")

if __name__ == "__main__":
    print("🌱 Seeding test companies...")
    seed_companies()
