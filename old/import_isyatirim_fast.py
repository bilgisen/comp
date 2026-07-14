"""
Fast Import İş Yatırım Financial Ratios
Optimized version with batch processing
"""

import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RATIO_MAPPING = {
    'F/K': 'pe_ratio',
    'PD/DD': 'pb_ratio',
    'FD/FAVÖK': 'ev_ebitda',
    'FD/Satışlar': 'ev_sales',
}

def main():
    logger.info("="*70)
    logger.info("İŞ YATIRIM RATIO IMPORT (FAST)")
    logger.info("="*70)
    
    # Read Excel
    df = pd.read_excel('finansal-oranlar.xlsx', sheet_name='isyatirim')
    logger.info(f"\n✅ Loaded {len(df)} companies")
    
    with SessionLocal() as db:
        # Step 1: Schema (if needed)
        try:
            db.execute(text("ALTER TABLE company_ratios ADD COLUMN IF NOT EXISTS source VARCHAR(20) DEFAULT 'calculated'"))
            db.execute(text("ALTER TABLE company_ratios ADD COLUMN IF NOT EXISTS data_quality VARCHAR(20)"))
            db.commit()
        except:
            db.rollback()
        
        # Step 2: Get valid tickers
        valid_tickers = set(row[0] for row in db.execute(text("SELECT ticker FROM companies WHERE is_active = TRUE")).fetchall())
        logger.info(f"  ✅ Found {len(valid_tickers)} valid companies")
        
        # Step 3: Import prices (batch)
        logger.info("\n💰 Importing prices...")
        price_sql = []
        for _, row in df.iterrows():
            ticker = row['Kod']
            if ticker not in valid_tickers:
                continue
                
            price = row['Kapanış (TL)']
            if pd.notna(price) and price > 0:
                price_sql.append(f"('{ticker}', {float(price)}, NOW())")
        
        if price_sql:
            try:
                db.execute(text(f"""
                    INSERT INTO company_metrics (ticker, last_price, price_updated_at)
                    VALUES {', '.join(price_sql[:200])}
                    ON CONFLICT (ticker) DO UPDATE
                    SET last_price = EXCLUDED.last_price,
                        price_updated_at = EXCLUDED.price_updated_at
                """))
                db.commit()
                logger.info(f"  ✅ Imported {min(len(price_sql), 200)} prices")
            except Exception as e:
                logger.error(f"  ❌ Price import failed: {str(e)[:200]}")
                db.rollback()
        
        # Step 4: Import ratios (batch by ratio type)
        logger.info("\n📊 Importing ratios...")
        
        stats = {}
        for excel_col, ratio_code in RATIO_MAPPING.items():
            logger.info(f"\n  Processing {ratio_code}...")
            
            ratio_sql = []
            for _, row in df.iterrows():
                ticker = row['Kod']
                if ticker not in valid_tickers:
                    continue
                    
                value = row.get(excel_col)
                
                # Validate
                if pd.isna(value) or (isinstance(value, str) and value.strip() in ['A/D', 'N/A', '-']):
                    continue
                
                try:
                    value_float = float(value)
                    if value_float == 0:
                        continue
                    
                    ratio_sql.append(f"('{ticker}', '{ratio_code}', {value_float}, '2026Q1', TRUE, 'isyatirim', 'external', NOW())")
                except:
                    continue
            
            # Batch insert
            if ratio_sql:
                # Process in chunks of 100
                for i in range(0, len(ratio_sql), 100):
                    chunk = ratio_sql[i:i+100]
                    try:
                        db.execute(text(f"""
                            INSERT INTO company_ratios (
                                ticker, ratio_code, ratio_value, period_key, is_ttm,
                                source, data_quality, computed_at
                            )
                            VALUES {', '.join(chunk)}
                            ON CONFLICT (ticker, ratio_code, period_key) DO UPDATE
                            SET ratio_value = EXCLUDED.ratio_value,
                                source = EXCLUDED.source,
                                data_quality = EXCLUDED.data_quality,
                                computed_at = EXCLUDED.computed_at
                        """))
                        db.commit()
                    except Exception as e:
                        logger.error(f"    Chunk {i//100 + 1} failed: {str(e)[:100]}")
                        db.rollback()
                
                logger.info(f"    ✅ Imported {len(ratio_sql)} values")
                stats[ratio_code] = len(ratio_sql)
        
        # Report
        logger.info("\n" + "="*70)
        logger.info("IMPORT SUMMARY")
        logger.info("="*70)
        
        for ratio_code, count in stats.items():
            pct = 100 * count / 610
            logger.info(f"  {ratio_code:<15} {count:>3}/610 ({pct:>5.1f}%)")
        
        # Final coverage check
        logger.info("\n📈 Final Coverage:")
        for ratio_code in RATIO_MAPPING.values():
            count = db.execute(text("""
                SELECT COUNT(DISTINCT ticker) 
                FROM company_ratios 
                WHERE ratio_code = :ratio_code
            """), {"ratio_code": ratio_code}).scalar()
            
            pct = 100 * count / 610
            status = "✅" if pct > 70 else "⚠️" if pct > 40 else "❌"
            logger.info(f"  {ratio_code:<15} {count:>3}/610 ({pct:>5.1f}%) {status}")
        
        logger.info("\n✅ IMPORT COMPLETED")

if __name__ == "__main__":
    main()
