"""
Quick System Stabilization
Focus on what we CAN do now with existing data
"""

import logging
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("="*70)
    logger.info("QUICK SYSTEM STABILIZATION")
    logger.info("="*70)
    
    with SessionLocal() as db:
        # Step 1: Calculate missing ratios for companies that have financial data
        logger.info("\n📊 STEP 1: Calculate Missing Ratios")
        logger.info("-"*70)
        
        # Get companies with statements but no ratios
        missing = db.execute(text("""
            SELECT DISTINCT c.ticker, c.name, c.financial_group
            FROM companies c
            JOIN financial_statements_raw fs ON c.ticker = fs.ticker
            LEFT JOIN company_ratios cr ON c.ticker = cr.ticker
            WHERE c.is_active = TRUE AND cr.ticker IS NULL
            ORDER BY c.financial_group, c.ticker
        """)).fetchall()
        
        logger.info(f"Found {len(missing)} companies needing ratio calculation:")
        
        # Group by financial_group
        by_group = {}
        for row in missing:
            if row.financial_group not in by_group:
                by_group[row.financial_group] = []
            by_group[row.financial_group].append(row.ticker)
        
        for group, tickers in sorted(by_group.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"  {group:<15} {len(tickers):>3} companies")
            logger.info(f"    Sample: {', '.join(tickers[:5])}")
        
        logger.info("\n⚠️  RECOMMENDATION:")
        logger.info("  Run ratio calculation for these companies:")
        logger.info("  python calculate_ratios_sync.py")
        
        # Step 2: Check price data source
        logger.info("\n📊 STEP 2: Price Data Status")
        logger.info("-"*70)
        
        daily_prices_count = db.execute(text("""
            SELECT COUNT(DISTINCT ticker) FROM daily_prices
        """)).scalar()
        
        latest_date = db.execute(text("SELECT MAX(date) FROM daily_prices")).scalar()
        days_old = (datetime.now().date() - latest_date).days if latest_date else None
        
        logger.info(f"  Tickers in daily_prices: {daily_prices_count}")
        logger.info(f"  Latest date: {latest_date} ({days_old} days old)" if days_old is not None else "  Latest date: N/A")
        
        if daily_prices_count < 100:
            logger.warning(f"\n⚠️  CRITICAL: Only {daily_prices_count} tickers have price data")
            logger.info("  finveri needs to be restarted with updated tickers.json")
            logger.info("  Path: c:\\Users\\ASUS\\hp\\finveri\\data\\tickers.json (already updated)")
            logger.info("\n  ACTION REQUIRED:")
            logger.info("  1. Restart finveri process")
            logger.info("  2. Run historical sync: POST /admin/sync-all-history")
            logger.info("  3. Wait 30-60 minutes for completion")
        
        # Step 3: Sync available prices to company_metrics
        logger.info("\n📊 STEP 3: Sync Available Prices")
        logger.info("-"*70)
        
        # Get latest price for each ticker
        latest_prices = db.execute(text("""
            WITH latest_date AS (
                SELECT ticker, MAX(date) as last_date
                FROM daily_prices
                GROUP BY ticker
            )
            SELECT dp.ticker, dp.close as last_price, dp.volume
            FROM daily_prices dp
            JOIN latest_date ld ON dp.ticker = ld.ticker AND dp.date = ld.last_date
            WHERE dp.ticker IN (SELECT ticker FROM companies WHERE is_active = TRUE)
        """)).fetchall()
        
        if len(latest_prices) > 0:
            logger.info(f"Syncing {len(latest_prices)} prices to company_metrics...")
            
            for row in latest_prices:
                db.execute(text("""
                    INSERT INTO company_metrics (ticker, last_price, volume_1d, price_updated_at)
                    VALUES (:ticker, :price, :volume, :updated_at)
                    ON CONFLICT (ticker) DO UPDATE
                    SET last_price = :price,
                        volume_1d = :volume,
                        price_updated_at = :updated_at,
                        updated_at = :updated_at
                """), {
                    "ticker": row.ticker,
                    "price": float(row.last_price),
                    "volume": int(row.volume) if row.volume else None,
                    "updated_at": datetime.now()
                })
            
            db.commit()
            logger.info(f"✅ Synced {len(latest_prices)} prices")
        else:
            logger.warning("⚠️  No price data to sync")
        
        # Step 4: Summary
        logger.info("\n" + "="*70)
        logger.info("SUMMARY")
        logger.info("="*70)
        
        total = db.execute(text("SELECT COUNT(*) FROM companies WHERE is_active = TRUE")).scalar()
        with_statements = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM financial_statements_raw")).scalar()
        with_ratios = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM company_ratios")).scalar()
        with_scores = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM company_scores WHERE is_stale = FALSE")).scalar()
        with_price = db.execute(text("SELECT COUNT(*) FROM company_metrics WHERE last_price IS NOT NULL")).scalar()
        
        logger.info(f"\n📊 Current State:")
        logger.info(f"  Financial Statements: {with_statements}/{total} ({100*with_statements/total:.1f}%)")
        logger.info(f"  Ratios: {with_ratios}/{total} ({100*with_ratios/total:.1f}%)")
        logger.info(f"  Scores: {with_scores}/{total} ({100*with_scores/total:.1f}%)")
        logger.info(f"  Prices: {with_price}/{total} ({100*with_price/total:.1f}%)")
        
        # Priority actions
        logger.info(f"\n🎯 PRIORITY ACTIONS:")
        
        if with_ratios < with_statements:
            logger.info(f"  1. HIGH: Calculate missing ratios ({with_statements - with_ratios} companies)")
            logger.info(f"     python calculate_ratios_sync.py")
        
        if with_price < total * 0.5:
            logger.info(f"  2. CRITICAL: Fix price data coverage (currently {100*with_price/total:.1f}%)")
            logger.info(f"     - Restart finveri with updated tickers.json")
            logger.info(f"     - Run historical sync")
        
        if with_price >= total * 0.8 and with_ratios >= with_statements * 0.95:
            logger.info(f"  ✅ System is healthy - ready for production")
    
    logger.info("\n" + "="*70)
    logger.info("DONE")
    logger.info("="*70)

if __name__ == "__main__":
    main()
