"""Fast fetch of latest prices for all companies using yfinance"""
import logging
import yfinance as yf
from sqlalchemy import text
from core.database import SessionLocal
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_latest_prices():
    """Fetch latest prices for all active companies"""
    
    with SessionLocal() as db:
        # Get all active tickers
        tickers = db.execute(text("""
            SELECT ticker FROM companies WHERE is_active = TRUE ORDER BY ticker
        """)).fetchall()
        
        ticker_list = [t[0] for t in tickers]
        logger.info(f"📊 Fetching latest prices for {len(ticker_list)} tickers...")
        
        success_count = 0
        fail_count = 0
        batch_size = 50
        
        for i in range(0, len(ticker_list), batch_size):
            batch = ticker_list[i:i+batch_size]
            logger.info(f"\n  Processing batch {i//batch_size + 1}/{(len(ticker_list)-1)//batch_size + 1} ({len(batch)} tickers)...")
            
            for ticker in batch:
                try:
                    # Add .IS suffix for Turkish stocks
                    yf_symbol = f"{ticker}.IS"
                    
                    # Fetch latest data (faster than history)
                    stock = yf.Ticker(yf_symbol)
                    info = stock.info
                    
                    if not info or 'regularMarketPrice' not in info:
                        # Try with history if info fails
                        hist = stock.history(period='1d')
                        if hist.empty:
                            logger.warning(f"    {ticker}: No data")
                            fail_count += 1
                            continue
                        
                        last_price = float(hist['Close'].iloc[-1])
                        volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist else None
                    else:
                        last_price = info.get('regularMarketPrice') or info.get('currentPrice')
                        volume = info.get('volume')
                    
                    if not last_price:
                        logger.warning(f"    {ticker}: No price data")
                        fail_count += 1
                        continue
                    
                    # Insert to daily_prices
                    db.execute(text("""
                        INSERT INTO daily_prices (ticker, date, close, volume, open, high, low)
                        VALUES (:ticker, :date, :close, :volume, :close, :close, :close)
                        ON CONFLICT (ticker, date) DO UPDATE
                        SET close = :close, volume = :volume, updated_at = NOW()
                    """), {
                        "ticker": ticker,
                        "date": datetime.now().date(),
                        "close": last_price,
                        "volume": volume
                    })
                    
                    success_count += 1
                    logger.info(f"    ✅ {ticker}: {last_price:.2f} TL")
                    
                except Exception as e:
                    logger.error(f"    ❌ {ticker}: {str(e)[:50]}")
                    fail_count += 1
                
                time.sleep(0.1)  # Small delay to avoid rate limiting
            
            db.commit()
            logger.info(f"  Batch committed. Success: {success_count}, Failed: {fail_count}")
            time.sleep(1)  # Delay between batches
        
        logger.info(f"\n✅ Done!")
        logger.info(f"  Success: {success_count}/{len(ticker_list)} ({100*success_count/len(ticker_list):.1f}%)")
        logger.info(f"  Failed: {fail_count}/{len(ticker_list)}")

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("FAST LATEST PRICE FETCH")
    logger.info("="*70)
    start = datetime.now()
    fetch_latest_prices()
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"\n⏱️  Completed in {duration/60:.1f} minutes")
    logger.info("="*70)
