"""Quick score calculation for yatırım ortaklıkları only"""
import logging
from datetime import datetime
from sqlalchemy import text

from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def quick_calculate():
    """Quick calculation for yatırım ortaklıkları"""
    
    with SessionLocal() as db:
        # Get yatırım ortaklıkları tickers
        tickers = db.execute(text("""
            SELECT ticker FROM companies 
            WHERE industry = 'Yatırım Ortaklıkları' AND is_active = TRUE
        """)).fetchall()
        
        tickers = [t[0] for t in tickers]
        logger.info(f"Processing {len(tickers)} yatırım ortaklıkları: {tickers}")
        
        # Delete existing ratios for these tickers
        db.execute(text("""
            DELETE FROM company_ratios 
            WHERE ticker IN :tickers
        """), {"tickers": tuple(tickers)})
        db.commit()
        logger.info("Cleared existing ratios")
        
        # Calculate ratios for each ticker
        total_ratios = 0
        for ticker in tickers:
            periods = db.execute(text("""
                SELECT DISTINCT period_key, year, period
                FROM financial_statements_raw
                WHERE ticker = :ticker AND financial_group = 'XI_29'
                ORDER BY period_key DESC
            """), {"ticker": ticker}).fetchall()
            
            for period in periods:
                period_key = period[0]
                
                # Get financial data
                data = db.execute(text("""
                    SELECT item_code, value_try
                    FROM financial_statements_raw
                    WHERE ticker = :ticker AND period_key = :period_key
                """), {"ticker": ticker, "period_key": period_key}).fetchall()
                
                fd = {row[0]: float(row[1]) for row in data if row[1] is not None}
                
                # Calculate ratios
                def get(code, default=0):
                    return fd.get(code, default)
                
                def safe_div(a, b):
                    if a is None or b is None or b == 0:
                        return None
                    return a / b
                
                total_assets = get("1BL") or get("2ODB")
                current_assets = get("1A")
                current_liabilities = get("2A")
                shareholders_equity = get("2O")
                revenue = get("3C")
                net_income = get("3Z")
                
                ratios = {
                    "current_ratio": safe_div(current_assets, current_liabilities),
                    "roe": safe_div(net_income, shareholders_equity),
                    "roa": safe_div(net_income, total_assets),
                    "net_margin": safe_div(net_income, revenue),
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
                            "computed_at": datetime.utcnow()
                        })
                        total_ratios += 1
            
            logger.info(f"  ✅ {ticker}: {len(periods)} periods processed")
        
        db.commit()
        logger.info(f"\n✅ Completed: {total_ratios} ratios calculated")
        
        # Now calculate simple scores based on ratios
        logger.info("\n📊 Calculating scores...")
        
        # For simplicity, just use ROE as score (scaled 0-100)
        for ticker in tickers:
            latest_period = db.execute(text("""
                SELECT period_key, ratio_value
                FROM company_ratios
                WHERE ticker = :ticker AND ratio_code = 'roe'
                ORDER BY period_key DESC
                LIMIT 1
            """), {"ticker": ticker}).fetchone()
            
            if latest_period:
                period_key = latest_period[0]
                roe = latest_period[1]
                
                # Simple scoring: ROE * 500 capped at 100
                score = min(max(roe * 500, 0), 100) if roe else 50
                
                # Insert or update score
                db.execute(text("""
                    INSERT INTO company_scores (ticker, period_key, score_genel, score_sektor, computed_at, is_stale)
                    VALUES (:ticker, :period_key, :score, :score, :computed_at, FALSE)
                    ON CONFLICT (ticker, period_key) DO UPDATE
                    SET score_genel = :score, score_sektor = :score, computed_at = :computed_at
                """), {
                    "ticker": ticker,
                    "period_key": period_key,
                    "score": score,
                    "computed_at": datetime.utcnow()
                })
                
                logger.info(f"  ✅ {ticker}: Score = {score:.1f}")
        
        db.commit()
        logger.info("\n✅ All scores calculated!")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("QUICK YATIRIM ORTAKLIKLARI SCORE CALCULATION")
    logger.info("="*60)
    start = datetime.now()
    quick_calculate()
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"\n⏱️  Completed in {duration:.1f} seconds")
    logger.info("="*60)
