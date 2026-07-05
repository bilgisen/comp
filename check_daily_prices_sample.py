"""Check daily_prices table structure and sample data"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Get sample data
    samples = db.execute(text("""
        SELECT ticker, date, close, volume
        FROM daily_prices
        ORDER BY date DESC, ticker
        LIMIT 20
    """)).fetchall()
    
    print("\n📊 Sample Daily Prices (Latest):\n")
    print(f"{'Ticker':<10} {'Date':<12} {'Close':<12} {'Volume':<15}")
    print("-" * 55)
    
    for row in samples:
        close_str = f"{row.close:,.2f}" if row.close else "N/A"
        vol_str = f"{row.volume:,}" if row.volume else "N/A"
        print(f"{row.ticker:<10} {str(row.date):<12} {close_str:<12} {vol_str:<15}")
    
    # Check how many unique tickers
    ticker_count = db.execute(text("""
        SELECT COUNT(DISTINCT ticker) FROM daily_prices
    """)).scalar()
    
    # Check date range
    date_range = db.execute(text("""
        SELECT MIN(date) as min_date, MAX(date) as max_date
        FROM daily_prices
    """)).first()
    
    # Check how many holdings have price data
    holding_prices = db.execute(text("""
        SELECT COUNT(DISTINCT dp.ticker)
        FROM daily_prices dp
        JOIN companies c ON dp.ticker = c.ticker
        WHERE c.industry = 'Holdingler'
    """)).scalar()
    
    print(f"\n📈 Summary:")
    print(f"  Total Tickers: {ticker_count}")
    print(f"  Date Range: {date_range.min_date} to {date_range.max_date}")
    print(f"  Holdings with Price: {holding_prices}/38")
