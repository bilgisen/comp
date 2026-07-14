"""Populate company_metrics table from daily_prices and calculate P/E ratios"""
import logging
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_company_metrics():
    """Populate company_metrics with latest prices and calculate P/E ratios"""
    
    with SessionLocal() as db:
        # Step 1: Get latest price for each ticker from daily_prices
        logger.info("📊 Step 1: Getting latest prices from daily_prices...")
        
        latest_prices = db.execute(text("""
            WITH latest_date AS (
                SELECT ticker, MAX(date) as last_date
                FROM daily_prices
                GROUP BY ticker
            )
            SELECT dp.ticker, dp.close as last_price, dp.date, dp.volume
            FROM daily_prices dp
            JOIN latest_date ld ON dp.ticker = ld.ticker AND dp.date = ld.last_date
            WHERE dp.ticker IN (SELECT ticker FROM companies WHERE is_active = TRUE)
            ORDER BY dp.ticker
        """)).fetchall()
        
        logger.info(f"  Found {len(latest_prices)} tickers with price data")
        
        # Step 2: Get latest EPS for each ticker from company_ratios
        logger.info("\n📊 Step 2: Getting EPS data...")
        
        eps_data = {}
        eps_results = db.execute(text("""
            WITH latest_eps AS (
                SELECT ticker, period_key, ratio_value as eps,
                       ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY period_key DESC) as rn
                FROM company_ratios
                WHERE ratio_code = 'eps' AND ratio_value IS NOT NULL
            )
            SELECT ticker, eps, period_key
            FROM latest_eps
            WHERE rn = 1
        """)).fetchall()
        
        for row in eps_results:
            eps_data[row.ticker] = row.eps
        
        logger.info(f"  Found {len(eps_data)} tickers with EPS data")
        
        # Step 3: Insert/update company_metrics
        logger.info("\n📊 Step 3: Populating company_metrics...")
        
        inserted = 0
        with_pe = 0
        
        for row in latest_prices:
            ticker = row.ticker
            last_price = float(row.last_price) if row.last_price else None
            volume = int(row.volume) if row.volume else None
            
            if not last_price:
                continue
            
            # Calculate P/E ratio if EPS exists
            eps = eps_data.get(ticker)
            pe_ratio = None
            
            if eps and eps > 0 and last_price:
                pe_ratio = last_price / eps
                with_pe += 1
            
            # Check if exists, then update or insert
            existing = db.execute(text("""
                SELECT id FROM company_metrics WHERE ticker = :ticker
            """), {"ticker": ticker}).scalar()
            
            if existing:
                db.execute(text("""
                    UPDATE company_metrics
                    SET last_price = :last_price,
                        pe_ratio = :pe_ratio,
                        volume_1d = :volume,
                        price_updated_at = :updated_at,
                        updated_at = :updated_at
                    WHERE ticker = :ticker
                """), {
                    "ticker": ticker,
                    "last_price": last_price,
                    "pe_ratio": pe_ratio,
                    "volume": volume,
                    "updated_at": datetime.now()
                })
            else:
                db.execute(text("""
                    INSERT INTO company_metrics (
                        ticker, last_price, pe_ratio, volume_1d, price_updated_at
                    )
                    VALUES (:ticker, :last_price, :pe_ratio, :volume, :updated_at)
                """), {
                    "ticker": ticker,
                    "last_price": last_price,
                    "pe_ratio": pe_ratio,
                    "volume": volume,
                    "updated_at": datetime.now()
                })
            
            inserted += 1
            
            if inserted % 10 == 0:
                logger.info(f"    Processed {inserted} tickers...")
        
        db.commit()
        
        logger.info(f"\n✅ Done!")
        logger.info(f"  Total inserted/updated: {inserted}")
        logger.info(f"  With P/E ratio: {with_pe}")
        logger.info(f"  Without P/E: {inserted - with_pe} (no EPS data)")

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("POPULATE COMPANY METRICS")
    logger.info("="*60)
    populate_company_metrics()
    logger.info("="*60)
