"""
Comprehensive System Fix
- Fetch shares outstanding from external API
- Calculate missing ratios including EPS
- Populate prices and calculate P/E
"""

import logging
import asyncio
import httpx
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveFixer:
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    async def step1_fetch_shares_outstanding(self):
        """Fetch shares outstanding for all companies from Mynet API"""
        logger.info("="*70)
        logger.info("STEP 1: FETCH SHARES OUTSTANDING")
        logger.info("="*70)
        
        # Get all tickers
        tickers = self.db.execute(text("""
            SELECT ticker, name FROM companies WHERE is_active = TRUE ORDER BY ticker
        """)).fetchall()
        
        logger.info(f"📊 Fetching shares outstanding for {len(tickers)} companies...")
        
        success = 0
        fail = 0
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, row in enumerate(tickers):
                ticker = row.ticker
                
                try:
                    # Try Mynet API first (has shares outstanding)
                    url = f"https://www.mynet.com/borsa/hisse/{ticker}"
                    response = await client.get(url)
                    
                    if response.status_code == 200:
                        # Parse HTML for shares outstanding
                        # This is a placeholder - need to implement HTML parsing
                        # For now, calculate from market cap / price if available
                        pass
                    
                except Exception as e:
                    logger.debug(f"  {ticker}: {str(e)[:50]}")
                
                # Alternative: Calculate from market cap and price
                # Get latest price and market cap from Borsa Istanbul
                try:
                    # Use İş Yatırım API for price
                    url = f"https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={ticker}"
                    response = await client.get(url)
                    data = response.json()
                    
                    if data.get('ok') and data.get('value'):
                        ticker_data = data['value'][0]
                        price = float(ticker_data.get('son', 0))
                        market_cap_mn = float(ticker_data.get('piyasaDegeri', 0))  # in million TL
                        
                        if price > 0 and market_cap_mn > 0:
                            market_cap = market_cap_mn * 1_000_000  # convert to TL
                            shares = int(market_cap / price)
                            
                            # Update company_metrics
                            self.db.execute(text("""
                                INSERT INTO company_metrics (ticker, shares_outstanding, market_cap, last_price, price_updated_at)
                                VALUES (:ticker, :shares, :market_cap, :price, :updated_at)
                                ON CONFLICT (ticker) DO UPDATE
                                SET shares_outstanding = :shares,
                                    market_cap = :market_cap,
                                    last_price = :price,
                                    price_updated_at = :updated_at,
                                    updated_at = :updated_at
                            """), {
                                "ticker": ticker,
                                "shares": shares,
                                "market_cap": int(market_cap),
                                "price": price,
                                "updated_at": datetime.now()
                            })
                            
                            success += 1
                            if success % 10 == 0:
                                logger.info(f"  Progress: {success}/{len(tickers)} ({100*success/len(tickers):.1f}%)")
                                self.db.commit()
                        else:
                            fail += 1
                    else:
                        fail += 1
                
                except Exception as e:
                    logger.debug(f"  {ticker}: Failed - {str(e)[:30]}")
                    fail += 1
                
                # Rate limiting
                if i % 10 == 0:
                    await asyncio.sleep(0.5)
        
        self.db.commit()
        
        logger.info(f"\n✅ Done!")
        logger.info(f"  Success: {success}/{len(tickers)} ({100*success/len(tickers):.1f}%)")
        logger.info(f"  Failed: {fail}/{len(tickers)}")
        
        return success
    
    def step2_calculate_eps(self):
        """Calculate EPS for all companies with net income and shares"""
        logger.info("\n" + "="*70)
        logger.info("STEP 2: CALCULATE EPS")
        logger.info("="*70)
        
        # Get companies with both net income (TTM) and shares outstanding
        companies = self.db.execute(text("""
            SELECT DISTINCT c.ticker, c.financial_group
            FROM companies c
            JOIN company_metrics cm ON c.ticker = cm.ticker
            WHERE c.is_active = TRUE 
            AND cm.shares_outstanding IS NOT NULL
            AND cm.shares_outstanding > 0
            ORDER BY c.ticker
        """)).fetchall()
        
        logger.info(f"📊 Companies with shares outstanding: {len(companies)}")
        
        if len(companies) == 0:
            logger.warning("⚠️  No companies have shares_outstanding data")
            logger.info("  Run step 1 first to fetch shares outstanding")
            return 0
        
        # For each company, calculate EPS from TTM net income
        calculated = 0
        
        for row in companies:
            ticker = row.ticker
            
            # Get TTM net income (last 4 quarters or last 2 semesters)
            net_income_quarters = self.db.execute(text("""
                SELECT period_key, item_value
                FROM financial_statements_raw
                WHERE ticker = :ticker
                AND period_type = '3ay'
                AND item_code IN ('3ZC', '3NJD')  -- Net income codes for different groups
                ORDER BY period_key DESC
                LIMIT 4
            """), {"ticker": ticker}).fetchall()
            
            net_income_ttm = None
            
            if len(net_income_quarters) >= 4:
                net_income_ttm = sum(q.item_value for q in net_income_quarters)
            else:
                # Try semesters
                net_income_semesters = self.db.execute(text("""
                    SELECT period_key, item_value
                    FROM financial_statements_raw
                    WHERE ticker = :ticker
                    AND period_type = '6ay'
                    AND item_code IN ('3ZC', '3NJD')
                    ORDER BY period_key DESC
                    LIMIT 2
                """), {"ticker": ticker}).fetchall()
                
                if len(net_income_semesters) >= 2:
                    net_income_ttm = sum(s.item_value for s in net_income_semesters)
            
            if net_income_ttm is None:
                continue
            
            # Get shares outstanding
            shares = self.db.execute(text("""
                SELECT shares_outstanding FROM company_metrics WHERE ticker = :ticker
            """), {"ticker": ticker}).scalar()
            
            if shares and shares > 0:
                eps = net_income_ttm / shares
                
                # Get latest period for storing
                latest_period = self.db.execute(text("""
                    SELECT MAX(period_key) FROM financial_statements_raw
                    WHERE ticker = :ticker
                """), {"ticker": ticker}).scalar()
                
                # Store EPS in company_ratios
                self.db.execute(text("""
                    INSERT INTO company_ratios (
                        ticker, ratio_code, ratio_value, period_key, period_type, computed_at
                    )
                    VALUES (:ticker, 'eps', :eps, :period_key, 'ttm', :computed_at)
                    ON CONFLICT (ticker, ratio_code, period_key) DO UPDATE
                    SET ratio_value = :eps, computed_at = :computed_at
                """), {
                    "ticker": ticker,
                    "eps": eps,
                    "period_key": latest_period,
                    "computed_at": datetime.now()
                })
                
                calculated += 1
                
                if calculated % 50 == 0:
                    logger.info(f"  Calculated EPS for {calculated} companies...")
                    self.db.commit()
        
        self.db.commit()
        
        logger.info(f"\n✅ Calculated EPS for {calculated} companies")
        return calculated
    
    def step3_calculate_pe_ratios(self):
        """Calculate P/E ratios from price and EPS"""
        logger.info("\n" + "="*70)
        logger.info("STEP 3: CALCULATE P/E RATIOS")
        logger.info("="*70)
        
        # Get companies with price and EPS
        companies = self.db.execute(text("""
            SELECT cm.ticker, cm.last_price, cr.ratio_value as eps
            FROM company_metrics cm
            JOIN company_ratios cr ON cm.ticker = cr.ticker
            WHERE cm.last_price IS NOT NULL
            AND cm.last_price > 0
            AND cr.ratio_code = 'eps'
            AND cr.ratio_value IS NOT NULL
            AND cr.ratio_value > 0
        """)).fetchall()
        
        logger.info(f"📊 Companies with price and EPS: {len(companies)}")
        
        calculated = 0
        
        for row in companies:
            pe_ratio = row.last_price / row.eps
            
            self.db.execute(text("""
                UPDATE company_metrics
                SET pe_ratio = :pe_ratio, updated_at = :updated_at
                WHERE ticker = :ticker
            """), {
                "ticker": row.ticker,
                "pe_ratio": pe_ratio,
                "updated_at": datetime.now()
            })
            
            calculated += 1
        
        self.db.commit()
        
        logger.info(f"✅ Calculated P/E for {calculated} companies")
        return calculated
    
    def step4_verify(self):
        """Verify final state"""
        logger.info("\n" + "="*70)
        logger.info("VERIFICATION")
        logger.info("="*70)
        
        total_companies = self.db.execute(text(
            "SELECT COUNT(*) FROM companies WHERE is_active = TRUE"
        )).scalar()
        
        with_shares = self.db.execute(text("""
            SELECT COUNT(*) FROM company_metrics 
            WHERE shares_outstanding IS NOT NULL AND shares_outstanding > 0
        """)).scalar()
        
        with_eps = self.db.execute(text("""
            SELECT COUNT(DISTINCT ticker) FROM company_ratios WHERE ratio_code = 'eps'
        """)).scalar()
        
        with_pe = self.db.execute(text("""
            SELECT COUNT(*) FROM company_metrics WHERE pe_ratio IS NOT NULL
        """)).scalar()
        
        logger.info(f"\n📊 Final Coverage:")
        logger.info(f"  Total Companies: {total_companies}")
        logger.info(f"  With Shares Outstanding: {with_shares} ({100*with_shares/total_companies:.1f}%)")
        logger.info(f"  With EPS: {with_eps} ({100*with_eps/total_companies:.1f}%)")
        logger.info(f"  With P/E: {with_pe} ({100*with_pe/total_companies:.1f}%)")
        
        if with_pe >= total_companies * 0.7:
            logger.info("\n✅ System is now HEALTHY")
        elif with_pe >= total_companies * 0.5:
            logger.warning("\n⚠️  System is FUNCTIONAL but needs more data")
        else:
            logger.error("\n❌ System still needs work")

async def main():
    logger.info("="*70)
    logger.info("COMPREHENSIVE SYSTEM FIX")
    logger.info("="*70)
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    with ComprehensiveFixer() as fixer:
        # Step 1: Fetch shares outstanding and prices
        shares_success = await fixer.step1_fetch_shares_outstanding()
        
        if shares_success > 0:
            # Step 2: Calculate EPS
            eps_calculated = fixer.step2_calculate_eps()
            
            # Step 3: Calculate P/E ratios
            if eps_calculated > 0:
                fixer.step3_calculate_pe_ratios()
        
        # Step 4: Verify
        fixer.step4_verify()
    
    logger.info(f"\n{'='*70}")
    logger.info(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)

if __name__ == "__main__":
    asyncio.run(main())
