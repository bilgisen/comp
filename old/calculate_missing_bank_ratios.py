"""Calculate ratios for banks without ratios"""
import logging
from datetime import datetime
from sqlalchemy import text

from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_missing_ratios():
    """Calculate ratios for banks without them"""
    
    with SessionLocal() as db:
        # Find banks without ratios
        missing = db.execute(text("""
            SELECT c.ticker, c.name
            FROM companies c
            WHERE c.industry = 'Bankacılık' 
              AND c.is_active = TRUE
              AND c.financial_group = 'UFRS_K'
              AND NOT EXISTS (
                  SELECT 1 FROM company_ratios cr 
                  WHERE cr.ticker = c.ticker
              )
        """)).fetchall()
        
        logger.info(f"Found {len(missing)} banks without ratios:")
        for m in missing:
            logger.info(f"  - {m[0]}: {m[1]}")
        
        if not missing:
            logger.info("✅ All banks have ratios!")
            return
        
        # Calculate ratios for each
        total_ratios = 0
        for ticker, name in missing:
            logger.info(f"\n📊 Processing {ticker} - {name}")
            
            # Get periods
            periods = db.execute(text("""
                SELECT DISTINCT period_key, year, period
                FROM financial_statements_raw
                WHERE ticker = :ticker AND financial_group = 'UFRS_K'
                ORDER BY period_key DESC
            """), {"ticker": ticker}).fetchall()
            
            if not periods:
                logger.warning(f"  ⚠️  No financial data found")
                continue
            
            logger.info(f"  Found {len(periods)} periods")
            
            for period in periods:
                period_key = period[0]
                
                # Get financial data
                data = db.execute(text("""
                    SELECT item_code, value_try
                    FROM financial_statements_raw
                    WHERE ticker = :ticker AND period_key = :period_key
                """), {"ticker": ticker, "period_key": period_key}).fetchall()
                
                fd = {row[0]: float(row[1]) for row in data if row[1] is not None}
                
                # Bank ratios (UFRS_K)
                def get(code, default=None):
                    return fd.get(code, default)
                
                def safe_div(a, b):
                    if a is None or b is None or b == 0:
                        return None
                    return a / b
                
                total_assets = get("1Z")
                gross_loans = get("1AF")
                deposits = get("2A")
                shareholders_equity = get("2O") or get("2OA")
                net_income = get("3ZA") or get("3Z")
                
                ratios = {
                    "loan_to_deposit": safe_div(gross_loans, deposits),
                    "roe": safe_div(net_income, shareholders_equity),
                    "roa": safe_div(net_income, total_assets),
                }
                
                # Save ratios
                for ratio_code, ratio_value in ratios.items():
                    if ratio_value is not None:
                        db.execute(text("""
                            INSERT INTO company_ratios (ticker, period_key, ratio_code, ratio_value, is_ttm, computed_at)
                            VALUES (:ticker, :period_key, :ratio_code, :ratio_value, FALSE, :computed_at)
                            ON CONFLICT (ticker, period_key, ratio_code) DO UPDATE
                            SET ratio_value = :ratio_value, computed_at = :computed_at
                        """), {
                            "ticker": ticker,
                            "period_key": period_key,
                            "ratio_code": ratio_code,
                            "ratio_value": ratio_value,
                            "computed_at": datetime.now()
                        })
                        total_ratios += 1
            
            logger.info(f"  ✅ Saved ratios for {ticker}")
        
        db.commit()
        logger.info(f"\n✅ Total ratios calculated: {total_ratios}")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("CALCULATE MISSING BANK RATIOS")
    logger.info("="*60)
    start = datetime.now()
    calculate_missing_ratios()
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"\n⏱️  Completed in {duration:.1f} seconds")
    logger.info("="*60)
