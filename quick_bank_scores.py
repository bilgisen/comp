"""Quick score calculation for banks (UFRS_K) only"""
import logging
from datetime import datetime
from sqlalchemy import text

from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def quick_calculate_banks():
    """Quick calculation for banks"""
    
    with SessionLocal() as db:
        # Get bank tickers
        tickers = db.execute(text("""
            SELECT ticker FROM companies 
            WHERE industry = 'Bankacılık' AND is_active = TRUE AND financial_group = 'UFRS_K'
        """)).fetchall()
        
        tickers = [t[0] for t in tickers]
        logger.info(f"Processing {len(tickers)} banks: {tickers}")
        
        # Calculate scores for banks (using existing ratios)
        logger.info("\n📊 Calculating scores from existing ratios...")
        
        score_count = 0
        for ticker in tickers:
            # Get latest ratios
            ratios = db.execute(text("""
                SELECT period_key, ratio_code, ratio_value
                FROM company_ratios
                WHERE ticker = :ticker
                ORDER BY period_key DESC
                LIMIT 10
            """), {"ticker": ticker}).fetchall()
            
            if not ratios:
                logger.warning(f"  ⚠️  {ticker}: No ratios found")
                continue
            
            period_key = ratios[0][0]
            
            # Build ratio dict
            ratio_dict = {}
            for r in ratios:
                if r[0] == period_key:  # Same period
                    ratio_dict[r[1]] = r[2]
            
            # Calculate simple score based on ROE and ROA
            roe = ratio_dict.get('roe', 0)
            roa = ratio_dict.get('roa', 0)
            
            # Simple scoring: (ROE * 300 + ROA * 700) capped at 100
            score = min(max((roe * 300 + roa * 700), 0), 100) if (roe or roa) else 50
            
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
                "computed_at": datetime.now()
            })
            
            score_count += 1
            logger.info(f"  ✅ {ticker}: Score = {score:.1f} (ROE={roe:.3f}, ROA={roa:.3f})")
        
        db.commit()
        logger.info(f"\n✅ Completed: {score_count} bank scores calculated!")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("QUICK BANK SCORE CALCULATION")
    logger.info("="*60)
    start = datetime.now()
    quick_calculate_banks()
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"\n⏱️  Completed in {duration:.1f} seconds")
    logger.info("="*60)
