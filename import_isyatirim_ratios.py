"""
Import İş Yatırım Financial Ratios from Excel
Source: finansal-oranlar.xlsx

Imports:
- F/K (P/E Ratio)
- PD/DD (P/B Ratio)
- FD/FAVÖK (EV/EBITDA)
- FD/Satışlar (EV/Sales)
- Kapanış (Closing Price)
"""

import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ratio mapping: Excel column -> our ratio_code
RATIO_MAPPING = {
    'F/K': 'pe_ratio',
    'PD/DD': 'pb_ratio',
    'FD/FAVÖK': 'ev_ebitda',
    'FD/Satışlar': 'ev_sales',
}

def parse_period(period_str):
    """Parse period string like '3/2026' to period_key like '2026Q1'"""
    try:
        if pd.isna(period_str):
            return '2026Q1'  # Default
        
        month, year = period_str.split('/')
        month = int(month)
        
        # Convert to quarter
        if month <= 3:
            quarter = 1
        elif month <= 6:
            quarter = 2
        elif month <= 9:
            quarter = 3
        else:
            quarter = 4
        
        return f"{year}Q{quarter}"
    except:
        return '2026Q1'  # Default fallback

def is_valid_ratio_value(value):
    """Check if value is valid (not A/D, not NaN, is numeric)"""
    if pd.isna(value):
        return False
    if isinstance(value, str):
        if value.strip() in ['A/D', 'N/A', '-', '']:
            return False
        try:
            float(value)
            return True
        except:
            return False
    return isinstance(value, (int, float)) and value != 0

def import_isyatirim_ratios():
    """Import ratios from İş Yatırım Excel file"""
    
    logger.info("="*70)
    logger.info("İŞ YATIRIM RATIO IMPORT")
    logger.info("="*70)
    
    # Read Excel
    logger.info("\n📂 Reading finansal-oranlar.xlsx...")
    try:
        df = pd.read_excel('finansal-oranlar.xlsx', sheet_name='isyatirim')
        logger.info(f"  ✅ Loaded {len(df)} companies")
    except Exception as e:
        logger.error(f"  ❌ Failed to read Excel: {e}")
        return
    
    # Step 1: Add source column if not exists (separate transaction)
    logger.info("\n🔧 Checking database schema...")
    with SessionLocal() as db:
        try:
            db.execute(text("""
                ALTER TABLE company_ratios 
                ADD COLUMN IF NOT EXISTS source VARCHAR(20) DEFAULT 'calculated'
            """))
            db.execute(text("""
                ALTER TABLE company_ratios 
                ADD COLUMN IF NOT EXISTS data_quality VARCHAR(20)
            """))
            db.commit()
            logger.info("  ✅ Schema updated")
        except Exception as e:
            logger.warning(f"  ⚠️  Schema update: {e}")
            db.rollback()
    
    # Step 2: Import data (new transaction)
    with SessionLocal() as db:
        # Import prices to company_metrics
        logger.info("\n💰 Importing prices to company_metrics...")
        price_count = 0
        price_errors = 0
        
        for _, row in df.iterrows():
            ticker = row['Kod']
            price = row['Kapanış (TL)']
            
            if pd.notna(price) and price > 0:
                try:
                    db.execute(text("""
                        INSERT INTO company_metrics (ticker, last_price, price_updated_at)
                        VALUES (:ticker, :price, :updated_at)
                        ON CONFLICT (ticker) DO UPDATE
                        SET last_price = :price,
                            price_updated_at = :updated_at,
                            updated_at = :updated_at
                    """), {
                        "ticker": ticker,
                        "price": float(price),
                        "updated_at": datetime.now()
                    })
                    db.commit()  # Commit each price separately
                    price_count += 1
                except Exception as e:
                    db.rollback()  # Rollback on error
                    price_errors += 1
                    logger.debug(f"  {ticker}: Price import failed - {str(e)[:50]}")
        
        logger.info(f"  ✅ Imported {price_count} prices ({price_errors} errors)")
        
        # Step 3: Import ratios to company_ratios
        logger.info("\n📊 Importing ratios to company_ratios...")
        
        stats = {ratio_code: {'imported': 0, 'skipped': 0} for ratio_code in RATIO_MAPPING.values()}
        
        for _, row in df.iterrows():
            ticker = row['Kod']
            period_key = parse_period(row.get('Son Dönem'))
            
            # Check if company exists
            exists = db.execute(text("""
                SELECT 1 FROM companies WHERE ticker = :ticker AND is_active = TRUE
            """), {"ticker": ticker}).scalar()
            
            if not exists:
                logger.debug(f"  ⚠️  {ticker}: Company not found in database")
                continue
            
            # Import each ratio
            for excel_col, ratio_code in RATIO_MAPPING.items():
                value = row.get(excel_col)
                
                if not is_valid_ratio_value(value):
                    stats[ratio_code]['skipped'] += 1
                    continue
                
                try:
                    value_float = float(value)
                    
                    # Insert or update
                    db.execute(text("""
                        INSERT INTO company_ratios (
                            ticker, ratio_code, ratio_value, period_key, period_type,
                            source, data_quality, computed_at
                        )
                        VALUES (
                            :ticker, :ratio_code, :value, :period_key, 'ttm',
                            'isyatirim', 'external', :computed_at
                        )
                        ON CONFLICT (ticker, ratio_code, period_key) DO UPDATE
                        SET ratio_value = :value,
                            source = 'isyatirim',
                            data_quality = 'external',
                            computed_at = :computed_at
                    """), {
                        "ticker": ticker,
                        "ratio_code": ratio_code,
                        "value": value_float,
                        "period_key": period_key,
                        "computed_at": datetime.now()
                    })
                    
                    db.commit()  # Commit each ratio separately
                    stats[ratio_code]['imported'] += 1
                    
                except Exception as e:
                    db.rollback()  # Rollback on error
                    logger.debug(f"  {ticker} {ratio_code}: {str(e)[:50]}")
                    stats[ratio_code]['skipped'] += 1
        
        # Report
        logger.info("\n" + "="*70)
        logger.info("IMPORT SUMMARY")
        logger.info("="*70)
        
        logger.info(f"\n💰 Prices:")
        logger.info(f"  Imported: {price_count}/610")
        
        logger.info(f"\n📊 Ratios:")
        total_imported = 0
        total_skipped = 0
        
        for ratio_code, counts in stats.items():
            imported = counts['imported']
            skipped = counts['skipped']
            total_imported += imported
            total_skipped += skipped
            
            logger.info(f"  {ratio_code:<15} {imported:>3} imported, {skipped:>3} skipped")
        
        logger.info(f"\n  TOTAL:           {total_imported:>3} ratios imported")
        
        # Coverage report
        logger.info(f"\n📈 Coverage After Import:")
        
        for ratio_code in RATIO_MAPPING.values():
            count = db.execute(text("""
                SELECT COUNT(DISTINCT ticker) 
                FROM company_ratios 
                WHERE ratio_code = :ratio_code
            """), {"ratio_code": ratio_code}).scalar()
            
            pct = 100 * count / 610
            status = "✅" if pct > 70 else "⚠️" if pct > 40 else "❌"
            logger.info(f"  {ratio_code:<15} {count:>3}/610 ({pct:>5.1f}%) {status}")
        
        logger.info("\n" + "="*70)
        logger.info("✅ IMPORT COMPLETED")
        logger.info("="*70)

if __name__ == "__main__":
    import_isyatirim_ratios()
