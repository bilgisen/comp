"""Fix ratio calculation for insurance companies (ANSGR, ANHYT)"""
import logging
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_insurance_ratios():
    """Recalculate ratios for insurance companies with correct item codes"""
    
    with SessionLocal() as db:
        # Get insurance companies with financial data
        companies = ['ANSGR', 'ANHYT']
        
        for ticker in companies:
            logger.info(f"\n📊 Processing {ticker}")
            
            # Get periods
            periods = db.execute(text("""
                SELECT DISTINCT period_key 
                FROM financial_statements_raw
                WHERE ticker = :ticker AND financial_group = 'UFRS_K'
                ORDER BY period_key DESC
            """), {"ticker": ticker}).fetchall()
            
            if not periods:
                logger.warning(f"  ⚠️  No financial data for {ticker}")
                continue
            
            logger.info(f"  Found {len(periods)} periods")
            
            for (period_key,) in periods:
                # Get financial data
                data = db.execute(text("""
                    SELECT item_code, value_try
                    FROM financial_statements_raw
                    WHERE ticker = :ticker AND period_key = :period_key
                """), {"ticker": ticker, "period_key": period_key}).fetchall()
                
                fd = {row[0]: float(row[1]) for row in data if row[1] is not None}
                
                def get(code, default=None):
                    return fd.get(code, default)
                
                def safe_div(a, b):
                    if a is None or b is None or b == 0:
                        return None
                    return a / b
                
                # Insurance company specific item codes
                total_assets = get("1Z")  # Total assets
                shareholders_equity = get("2O")  # Shareholders equity
                net_income = get("3NJD")  # Net income (insurance companies use 3NJD, not 3ZA)
                
                logger.info(f"  Period {period_key}:")
                logger.info(f"    Total Assets: {total_assets:,.0f}" if total_assets else "    Total Assets: None")
                logger.info(f"    Shareholders Equity: {shareholders_equity:,.0f}" if shareholders_equity else "    Shareholders Equity: None")
                logger.info(f"    Net Income: {net_income:,.0f}" if net_income else "    Net Income: None")
                
                # Calculate ratios
                roe = safe_div(net_income, shareholders_equity)
                roa = safe_div(net_income, total_assets)
                
                logger.info(f"    ROE: {roe:.6f}" if roe else "    ROE: None")
                logger.info(f"    ROA: {roa:.6f}" if roa else "    ROA: None")
                
                # Update ratios
                ratios_updated = 0
                for ratio_code, ratio_value in [("roe", roe), ("roa", roa)]:
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
                        ratios_updated += 1
                
                logger.info(f"    ✅ Updated {ratios_updated} ratios")
                
                # Calculate and save score for latest period only
                if period_key == periods[0][0]:
                    if roe or roa:
                        score = min(max((roe * 300 + roa * 700) if (roe and roa) else 0, 0), 100)
                        
                        db.execute(text("""
                            INSERT INTO company_scores (ticker, period_key, score_genel, score_sektor, computed_at, is_stale)
                            VALUES (:ticker, :period_key, :score, :score, :computed_at, FALSE)
                            ON CONFLICT (ticker, period_key) DO UPDATE
                            SET score_genel = :score, score_sektor = :score, computed_at = :computed_at, is_stale = FALSE
                        """), {
                            "ticker": ticker,
                            "period_key": period_key,
                            "score": score,
                            "computed_at": datetime.now()
                        })
                        
                        logger.info(f"    💯 Score: {score:.2f}")
        
        db.commit()
        logger.info(f"\n✅ Completed!")

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("FIX INSURANCE RATIOS AND SCORES")
    logger.info("="*60)
    fix_insurance_ratios()
    logger.info("="*60)
