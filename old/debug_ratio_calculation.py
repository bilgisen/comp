"""
Debug Script: Rasyo Hesaplama Sorunları Analizi
"""
from core.database import SessionLocal
from models.financial import FinancialStatementRaw, CompanyRatio
from models.company import Company
from services.item_code_mapper import ItemCodeMapper
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_single_company(ticker):
    """Tek bir şirket için rasyo hesaplama sürecini debug et"""
    
    with SessionLocal() as db:
        company = db.query(Company).filter(Company.ticker == ticker).first()
        if not company:
            print(f"Şirket bulunamadı: {ticker}")
            return
        
        print(f"\n{'='*60}")
        print(f"DEBUG: {ticker} - {company.name}")
        print(f"Sektör: {company.sector_main}")
        print(f"Financial Group: {company.financial_group}")
        print(f"{'='*60}\n")
        
        # Mali tablo verilerini al
        statements = db.query(FinancialStatementRaw).filter(
            FinancialStatementRaw.ticker == ticker
        ).order_by(FinancialStatementRaw.year.desc(), FinancialStatementRaw.period.desc()).all()
        
        if not statements:
            print("❌ Mali tablo verisi yok!")
            return
        
        print(f"✅ Toplam mali tablo satırı: {len(statements)}")
        
        # Dönemleri grupla
        periods = {}
        for stmt in statements:
            key = (stmt.year, stmt.period)
            if key not in periods:
                periods[key] = []
            periods[key].append(stmt)
        
        print(f"\n📅 Dönemler ({len(periods)} adet):")
        for (year, period), stmts in sorted(periods.items(), reverse=True):
            print(f"   {year}Q{period//3 if period != 12 else 4}: {len(stmts)} item")
        
        # Item code mapping test
        print(f"\n🔗 Item Code Mapping Test:")
        mapper = ItemCodeMapper(db)
        
        # Önemli item code'ları kontrol et
        important_codes = {
            "XI_29": ["1Z", "1A", "1AD", "2O", "2A", "3A", "3C", "3E", "3Z"],
            "UFRS_K": ["1Z", "1AF", "2O", "2A", "3ZA", "3C", "3CH"]
        }
        
        financial_group = company.financial_group
        codes_to_check = important_codes.get(financial_group, important_codes["XI_29"])
        
        mapped_count = 0
        unmapped_count = 0
        
        for code in codes_to_check:
            semantic = mapper.get_semantic_name(code, financial_group)
            if semantic:
                print(f"   ✅ {code} -> {semantic}")
                mapped_count += 1
            else:
                print(f"   ❌ {code} -> MAPPING YOK!")
                unmapped_count += 1
        
        print(f"\n📊 Mapping Durumu: {mapped_count}/{len(codes_to_check)} başarılı")
        
        # Mevcut rasyoları kontrol et
        existing_ratios = db.query(CompanyRatio).filter(CompanyRatio.ticker == ticker).all()
        print(f"\n📈 Mevcut Rasyolar: {len(existing_ratios)}")
        for r in existing_ratios:
            print(f"   {r.period_key}: {r.ratio_code} = {r.ratio_value}")
        
        # Financial data extraction test
        print(f"\n🔍 Financial Data Extraction Test:")
        
        # Son dönem için veri çek
        latest_period = sorted(periods.keys(), reverse=True)[0]
        latest_stmts = periods[latest_period]
        
        print(f"   Son Dönem: {latest_period[0]}Q{latest_period[1]//3 if latest_period[1] != 12 else 4}")
        
        financial_data = {}
        for stmt in latest_stmts:
            semantic = mapper.get_semantic_name(stmt.item_code, financial_group)
            if semantic and stmt.value_try is not None:
                financial_data[semantic] = float(stmt.value_try)
        
        print(f"   Maplenmiş veri: {len(financial_data)} item")
        
        # Kritik verileri kontrol et
        critical_fields = [
            "total_assets", "current_assets", "shareholders_equity",
            "current_liabilities", "revenue", "net_income", "operating_income",
            "gross_profit", "cost_of_goods_sold", "short_term_borrowings", "long_term_borrowings"
        ]
        
        print(f"\n   Kritik Alanlar:")
        for field in critical_fields:
            value = financial_data.get(field)
            if value is not None:
                print(f"   ✅ {field}: {value:,.2f}")
            else:
                print(f"   ❌ {field}: YOK")

def analyze_all_companies():
    """Tüm şirketler için rasyo hesaplama durumunu analiz et"""
    
    with SessionLocal() as db:
        # Rasyo hesaplanmış şirket sayısı
        companies_with_ratios = db.execute(text('''
            SELECT COUNT(DISTINCT ticker) FROM company_ratios
        ''')).scalar()
        
        # Toplam şirket sayısı
        total_companies = db.query(Company).count()
        
        print(f"\n{'='*60}")
        print(f"GENEL DURUM ANALİZİ")
        print(f"{'='*60}")
        print(f"Toplam Şirket: {total_companies}")
        print(f"Rasyosu Olan Şirket: {companies_with_ratios}")
        print(f"Rasyosu Olmayan: {total_companies - companies_with_ratios}")
        
        # Financial group bazında analiz
        print(f"\nFinancial Group Bazında:")
        groups = db.execute(text('''
            SELECT c.financial_group, 
                   COUNT(DISTINCT c.ticker) as total,
                   COUNT(DISTINCT cr.ticker) as with_ratios
            FROM companies c
            LEFT JOIN company_ratios cr ON c.ticker = cr.ticker
            GROUP BY c.financial_group
        ''')).fetchall()
        
        for g in groups:
            print(f"   {g[0]}: {g[2]}/{g[1]} şirket rasyoya sahip")
        
        # İlk 5 şirket için debug
        print(f"\n{'='*60}")
        print(f"İLK 5 ŞİRKET DEBUG")
        print(f"{'='*60}")
        
        tickers = db.execute(text('''
            SELECT DISTINCT ticker FROM financial_statements_raw
            ORDER BY ticker
            LIMIT 5
        ''')).scalars().all()
        
        for ticker in tickers:
            debug_single_company(ticker)

if __name__ == "__main__":
    # İlk olarak genel analiz
    analyze_all_companies()
