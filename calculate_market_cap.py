"""
Calculate market cap from price and shares outstanding
Then calculate P/E ratios
"""
import logging
from sqlalchemy import text
from core.database import SessionLocal
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("CALCULATE MARKET CAP & P/E")
    logger.info("="*60)
    
    with SessionLocal() as db:
        # Step 1: Get companies with price data
        logger.info("\n📊 Step 1: Companies with price data...")
        
        companies = db.execute(text("""
            SELECT c.ticker, c.name, cm.last_price, c.shares_outstanding
            FROM companies c
            JOIN company_metrics cm ON c.ticker = cm.ticker
            WHERE c.is_active = TRUE 
            AND cm.last_price IS NOT NULL
            AND cm.last_price > 0
        """)).fetchall()
        
        logger.info(f"  Found {len(companies)} companies with price")
        
        # Step 2: Calculate market cap for those with shares_outstanding
        logger.info("\n📊 Step 2: Calculating market cap...")
        
        updated = 0
        for comp in companies:
            if comp.shares_outstanding and comp.shares_outstanding > 0:
                market_cap = int(comp.last_price * comp.shares_outstanding)
                
                db.execute(text("""
                    UPDATE company_metrics
                    SET market_cap = :market_cap, updated_at = :updated_at
                    WHERE ticker = :ticker
                """), {
                    "ticker": comp.ticker,
                    "market_cap": market_cap,
                    "updated_at": datetime.now()
                })
                
                updated += 1
                logger.info(f"    {comp.ticker}: {market_cap:,} TL")
        
        db.commit()
        logger.info(f"\n  ✅ Updated market_cap for {updated} companies")
        
        # Step 3: Now calculate P/E from market_cap / net_income_ttm
        logger.info("\n📊 Step 3: Calculating P/E ratios...")
        
        # Get companies with market_cap and net_income
        pe_candidates = db.execute(text("""
            SELECT cm.ticker, cm.market_cap, cr.ratio_value as net_income
            FROM company_metrics cm
            JOIN company_ratios cr ON cm.ticker = cr.ticker
            WHERE cm.market_cap IS NOT NULL
            AND cm.market_cap > 0
            AND cr.ratio_code IN ('net_income', 'net_margin')
            AND cr.ratio_value IS NOT NULL
        """)).fetchall()
        
        logger.info(f"  Found {len(pe_candidates)} candidates for P/E")
        
        # Actually, we need net_income_ttm not net_margin
        # Let's check what income data we have
        logger.info("\n📊 Checking income data availability...")
        
        income_ratios = db.execute(text("""
            SELECT ratio_code, COUNT(DISTINCT ticker) as count
            FROM company_ratios
            WHERE ratio_code LIKE '%income%' OR ratio_code LIKE '%margin%'
            GROUP BY ratio_code
            ORDER BY count DESC
        """)).fetchall()
        
        logger.info("  Income-related ratios:")
        for r in income_ratios:
            logger.info(f"    {r.ratio_code:<20} {r.count:>3} companies")
        
        logger.info("\n" + "="*60)
        logger.info("SUMMARY")
        logger.info("="*60)
        logger.info(f"  Market cap calculated: {updated} companies")
        logger.info(f"  P/E calculation: Need net_income_ttm data")
        logger.info(f"  Alternative: Use net_margin * revenue")

if __name__ == "__main__":
    main()
