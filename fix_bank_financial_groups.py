"""Fix financial_group for banks - they should use UFRS_K not XI_29"""

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
    # Banking & Finance sector companies should use UFRS_K
    # This includes banks, insurance companies, leasing, etc.
    banking_sectors = [
        "Bankacılık & Finans",
        "Bankacılık",
        "Finans",
        "Sigorta",
        "Leasing",
        "Faktoring"
    ]
    
    # Find companies in banking/finance sectors with wrong financial_group
    for sector in banking_sectors:
        companies = db.query(Company).filter(
            Company.sector_main.like(f"%{sector}%"),
            Company.financial_group != "UFRS_K"
        ).all()
        
        print(f"\n📊 {sector}: {len(companies)} companies need update")
        
        for company in companies:
            print(f"   Updating {company.ticker} ({company.name}): {company.financial_group} → UFRS_K")
            company.financial_group = "UFRS_K"
    
    # Also check for specific bank tickers (common Turkish banks)
    bank_tickers = [
        "GARAN", "AKBNK", "YKBNK", "ISCTR", "HALKB", "VAKBN", 
        "ALBRK", "SKBNK", "ICBCT", "QNBFB", "TSKB", "KLNMA",
        "THYAO"  # Turkish Airlines uses UFRS_K as well (special case)
    ]
    
    for ticker in bank_tickers:
        company = db.query(Company).filter(Company.ticker == ticker).first()
        if company and company.financial_group != "UFRS_K":
            print(f"   Updating {company.ticker} ({company.name}): {company.financial_group} → UFRS_K")
            company.financial_group = "UFRS_K"
    
    # Show summary before committing
    print("\n" + "="*60)
    updated_count = db.query(Company).filter(
        Company.sector_main.like("%Bankacılık%")
    ).count()
    print(f"📊 Total companies in Banking/Finance sector: {updated_count}")
    
    # Ask for confirmation
    confirm = input("\n✅ Commit these changes? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        db.commit()
        print("✅ Changes committed successfully!")
        
        # Verify GARAN
        garan = db.query(Company).filter(Company.ticker == "GARAN").first()
        if garan:
            print(f"\n✅ GARAN financial_group: {garan.financial_group}")
    else:
        db.rollback()
        print("❌ Changes rolled back")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
