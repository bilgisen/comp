"""Calculate scores for ANSGR and ANHYT specifically"""
import logging
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_insurance_scores():
    """Calculate scores for insurance companies with ratios but no scores"""
    
    with SessionLocal() as db:
        # Get insurance companies with ratios but no scores for latest period
        companies = db.execute(text("""
            WITH latest_ratios AS (
                SELECT ticker, MAX(period_key) as latest_period
                FROM company_ratios
                WHERE ticker IN (
                    SELECT ticker FROM companies 
                    WHERE industry = 'Sigortacılık' AND is_active = TRUE
                )
                GROUP BY ticker
            )
            SELECT lr.ticker, c.name, lr.latest_period
            FROM latest_ratios lr
            JOIN companies c ON lr.ticker = c.ticker
            LEFT JOIN company_scores cs ON cs.ticker = lr.ticker AND cs.period_key = lr.latest_period
            WHERE cs.ticker IS NULL
            ORDER BY lr.ticker
        """)).fetchall()
        
        logger.info(f"Found {len(companies)} insurance companies with ratios but no scores")
        
        for ticker, name, period_key in companies:
            logger.info(f"\n📊 Processing {ticker} ({name}) - Period: {period_key}")
            
            # Get ratios for this period
            ratios = db.execute(text("""
                SELECT ratio_code, ratio_value
                FROM company_ratios
                WHERE ticker = :ticker AND period_key = :period_key
            """), {"ticker": ticker, "period_key": period_key}).fetchall()
            
            ratio_dict = {r[0]: r[1] for r in ratios}
            logger.info(f"  Found ratios: {list(ratio_dict.keys())}")
            
            # Calculate score (ROE * 300 + ROA * 700)
            roe = ratio_dict.get('roe', 0) or 0
            roa = ratio_dict.get('roa', 0) or 0
            
            logger.info(f"  ROE: {roe:.4f}, ROA: {roa:.4f}")
            
            score = min(max((roe * 300 + roa * 700), 0), 100)
            logger.info(f"  Calculated Score: {score:.2f}")
            
            # Insert score
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
            
            logger.info(f"  ✅ Score saved: {score:.2f}")
        
        db.commit()
        logger.info(f"\n✅ Completed: {len(companies)} insurance companies scored")

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("CALCULATE MISSING INSURANCE SCORES")
    logger.info("="*60)
    calculate_insurance_scores()
    logger.info("="*60)
