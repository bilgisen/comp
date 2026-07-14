"""Fetch latest prices from Is Yatirim HisseTekil API"""
import logging
import httpx
from sqlalchemy import text
from core.database import SessionLocal
from datetime import datetime
import time
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_price_from_isyatirim(ticker: str) -> dict:
    """Fetch single ticker price from Is Yatirim"""
    url = f"https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={ticker}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            data = response.json()
            
            if not data.get('ok'):
                return None
            
            # Parse response
            result = data.get('value', [])
            if not result or len(result) == 0:
                return None
            
            ticker_data = result[0]
            
            return {
                'ticker': ticker,
                'close': float(ticker_data.get('son', 0)),
                'open': float(ticker_data.get('acilis', 0)),
                'high': float(ticker_data.get('yuksek', 0)),
                'low': float(ticker_data.get('dusuk', 0)),
                'volume': float(ticker_data.get('hacim', 0))
            }
    except Exception as e:
        logger.debug(f"    {ticker}: {str(e)[:50]}")
        return None

async def fetch_all_prices():
    """Fetch prices for all active companies"""
    
    with SessionLocal() as db:
        # Get all active tickers
        tickers = db.execute(text("""
            SELECT ticker FROM companies WHERE is_active = TRUE ORDER BY ticker
        """)).fetchall()
        
        ticker_list = [t[0] for t in tickers]
        logger.info(f"📊 Fetching latest prices for {len(ticker_list)} tickers from Is Yatirim...")
        
        success_count = 0
        fail_count = 0
        
        # Process in batches
        batch_size = 10
        for i in range(0, len(ticker_list), batch_size):
            batch = ticker_list[i:i+batch_size]
            logger.info(f"\n  Batch {i//batch_size + 1}/{(len(ticker_list)-1)//batch_size + 1} ({len(batch)} tickers)...")
            
            # Fetch batch concurrently
            tasks = [fetch_price_from_isyatirim(ticker) for ticker in batch]
            results = await asyncio.gather(*tasks)
            
            # Save to database
            for result in results:
                if result and result['close'] > 0:
                    try:
                        db.execute(text("""
                            INSERT INTO daily_prices (ticker, date, close, open, high, low, volume)
                            VALUES (:ticker, :date, :close, :open, :high, :low, :volume)
                            ON CONFLICT (ticker, date) DO UPDATE
                            SET close = :close, open = :open, high = :high, low = :low, volume = :volume
                        """), {
                            "ticker": result['ticker'],
                            "date": datetime.now().date(),
                            "close": result['close'],
                            "open": result['open'],
                            "high": result['high'],
                            "low": result['low'],
                            "volume": result['volume']
                        })
                        success_count += 1
                        logger.info(f"    ✅ {result['ticker']}: {result['close']:.2f} TL")
                    except Exception as e:
                        logger.error(f"    ❌ {result['ticker']}: DB error - {str(e)[:50]}")
                        fail_count += 1
                else:
                    if result:
                        logger.warning(f"    ⚠️  {result['ticker']}: No price data")
                    fail_count += 1
            
            db.commit()
            await asyncio.sleep(0.5)  # Small delay between batches
        
        logger.info(f"\n✅ Done!")
        logger.info(f"  Success: {success_count}/{len(ticker_list)} ({100*success_count/len(ticker_list):.1f}%)")
        logger.info(f"  Failed: {fail_count}/{len(ticker_list)}")
        
        return success_count

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("FETCH PRICES FROM IS YATIRIM")
    logger.info("="*70)
    start = datetime.now()
    
    success = asyncio.run(fetch_all_prices())
    
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"\n⏱️  Completed in {duration/60:.1f} minutes")
    logger.info("="*70)
    
    if success > 0:
        logger.info("\nNEXT: Run populate_company_metrics.py")
