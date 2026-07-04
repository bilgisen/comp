"""
Create sector mapping from İş Yatırım's 53 sectors to HissePro's 21 industries
Maps companies to new industry field for better peer comparisons
"""
import openpyxl
from sqlalchemy import create_engine, text
from core.config import settings
from collections import defaultdict

# İş Yatırım sektörlerinden HissePro industry'lerine mapping
# ≥10 şirket olan sektörler doğrudan kullanılır
# <10 şirket olanlar parent industry'ye gruplanır
SECTOR_TO_INDUSTRY = {
    # Direct mappings (≥10 şirket)
    "GYO": "GYO",
    "Gıda": "Gıda",
    "Holdingler": "Holdingler",
    "Elektrik Üretim": "Elektrik Üretim",
    "Teknoloji": "Teknoloji",
    "Tekstil Entegre": "Tekstil",
    "İnşaat Malzemeleri": "İnşaat Malzemeleri",
    "Kimyasal Ürün": "Kimya",
    "Yatırım Ortaklıkları": "Yatırım Ortaklıkları",
    "Çimento": "Çimento",
    "Bankacılık": "Bankacılık",
    "Demir-Çelik Temel": "Demir-Çelik",
    "Elektrik Enerji Ürt.Teğh/Tesis Kurulum": "Elektrik Ekipman",
    "Kağıt Ürünleri": "Kağıt",
    "Ulaştırma-Lojistik": "Ulaştırma-Lojistik",
    "Perakande - Ticaret": "Perakende",
    "Sağlık ve İlaç": "Sağlık",
    "Turizm": "Turizm",
    "Otomotiv Parçası": "Otomotiv Yan Sanayi",
    "Fin.Kiralama ve Faktoring": "Finansal Kiralama",
    "Aracı Kurumlar": "Aracı Kurumlar",
    
    # Grouped mappings (<10 şirket → parent industry'ye)
    "Meşrubat / İçecek": "Gıda",  # 9 → Gıda (50+9=59)
    "Dayanıklı Tüketim": "Tüketim Elektroniği",  # 9 → Yeni grup
    "Otomotiv": "Otomotiv",  # 8 → Yeni grup
    "Medya": "Medya",  # 8 → Yeni grup
    "Demir-Çelik Döküm": "Demir-Çelik",  # 8 → Demir-Çelik (16+8=24)
    "Sigorta": "Sigortacılık",  # 6 → Yeni grup
    "Tekstil Dokumasız": "Tekstil",  # 6 → Tekstil
    "Elektrik - Doğalgaz Dağıtım": "Elektrik Dağıtım",  # 5 → Yeni grup
    "İletişim": "Teknoloji",  # 5 → Teknoloji
    "Savunma": "Savunma Sanayi",  # 5 → Yeni grup
    "Tarım&Hayvancılık": "Gıda",  # 5 → Gıda
    "Hizmetler": "Diğer",  # 4 → Diğer
    "Kimya": "Kimya",  # 4 → Kimya
    "Spor": "Spor",  # 4 → Yeni grup
    "Cam": "İnşaat Malzemeleri",  # 3 → İnşaat
    "Metal Dışı Mineral Ürünler": "İnşaat Malzemeleri",  # 3 → İnşaat
    "Mobilya&Orman Ürünleri": "Mobilya",  # 3 → Yeni grup
    "Petrol Ürünleri": "Enerji",  # 3 → Yeni grup
    "Tekstil Terbiye": "Tekstil",  # 3 → Tekstil
    "Diğer": "Diğer",  # 8 → Diğer
}

def load_is_yatirim_sectors():
    """Load sector mapping from İş Yatırım Excel"""
    wb = openpyxl.load_workbook('sektorler.xlsx')
    ws = wb.active
    
    ticker_to_sector = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] and len(row) > 2:  # ticker and sector exist
            ticker = row[0]
            sector = row[2]  # 3rd column is real sector
            ticker_to_sector[ticker] = sector
    
    wb.close()
    return ticker_to_sector

def create_industry_mapping():
    """Create mapping and update database"""
    
    sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_db_url)
    
    print("=" * 100)
    print("HissePro INDUSTRY MAPPING")
    print("=" * 100)
    
    # Load İş Yatırım sectors
    print("\n1. Loading İş Yatırım sector data...")
    ticker_to_sector = load_is_yatirim_sectors()
    print(f"   Loaded {len(ticker_to_sector)} companies from Excel")
    
    # Map to industries
    print("\n2. Mapping to HissePro industries...")
    ticker_to_industry = {}
    industry_counts = defaultdict(int)
    
    for ticker, sector in ticker_to_sector.items():
        industry = SECTOR_TO_INDUSTRY.get(sector, "Diğer")
        ticker_to_industry[ticker] = industry
        industry_counts[industry] += 1
    
    # Show industry distribution
    print("\n3. New Industry Distribution:")
    print("-" * 100)
    for industry, count in sorted(industry_counts.items(), key=lambda x: x[1], reverse=True):
        reliability = "✅ HIGH" if count >= 10 else "⚠️ MEDIUM" if count >= 5 else "❌ LOW"
        print(f"   {industry:40} {count:3} şirket  {reliability}")
    
    print(f"\n   Total industries: {len(industry_counts)}")
    high_quality = sum(1 for c in industry_counts.values() if c >= 10)
    print(f"   High quality (≥10): {high_quality} industries")
    
    # Update database
    print("\n4. Updating database...")
    
    with engine.connect() as conn:
        # First, check if industry column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='companies' AND column_name='industry'
        """))
        
        if not result.fetchone():
            print("   Creating 'industry' column...")
            conn.execute(text("ALTER TABLE companies ADD COLUMN industry VARCHAR(100)"))
            conn.commit()
        
        # Update each company
        updated = 0
        not_found = []
        
        for ticker, industry in ticker_to_industry.items():
            result = conn.execute(
                text("UPDATE companies SET industry = :industry WHERE ticker = :ticker"),
                {"industry": industry, "ticker": ticker}
            )
            
            if result.rowcount > 0:
                updated += 1
            else:
                not_found.append(ticker)
        
        conn.commit()
        
        print(f"   ✅ Updated {updated} companies")
        if not_found:
            print(f"   ⚠️ Not found in database: {len(not_found)} tickers")
            if len(not_found) <= 10:
                print(f"      {', '.join(not_found)}")
    
    print("\n" + "=" * 100)
    print("✅ MAPPING COMPLETE")
    print("=" * 100)
    
    return industry_counts

if __name__ == "__main__":
    create_industry_mapping()
