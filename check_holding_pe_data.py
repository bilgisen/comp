"""Check why holdings have no P/E ratio data"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Get holding companies
    holdings = db.execute(text("""
        SELECT c.ticker, c.name, cm.last_price, cm.market_cap, cm.pe_ratio
        FROM companies c
        LEFT JOIN company_metrics cm ON c.ticker = cm.ticker
        WHERE c.industry = 'Holdingler'
        ORDER BY cm.market_cap DESC NULLS LAST
        LIMIT 10
    """)).fetchall()
    
    print("\n📊 Holding Şirketleri - Fiyat ve EPS Durumu:\n")
    print(f"{'Ticker':<8} {'Name':<25} {'Price':<12} {'P/E (DB)':<12} {'Market Cap':<15}")
    print("-" * 80)
    
    for ticker, name, price, mcap, pe_db in holdings:
        price_str = f"{price:,.2f}" if price else "YOK"
        mcap_str = f"{mcap:,.0f}" if mcap else "YOK"
        pe_db_str = f"{pe_db:.2f}" if pe_db else "YOK"
        print(f"{ticker:<8} {name:<25} {price_str:<12} {pe_db_str:<12} {mcap_str:<15}")
        
        # Check if EPS exists
        eps = db.execute(text("""
            SELECT ratio_value 
            FROM company_ratios 
            WHERE ticker = :ticker AND ratio_code = 'eps'
            ORDER BY period_key DESC
            LIMIT 1
        """), {"ticker": ticker}).scalar()
        
        if eps:
            print(f"         → EPS: {eps:.4f}, P/E: {price/eps:.2f}" if price and eps != 0 else f"         → EPS: {eps:.4f}, P/E: N/A")
        else:
            print(f"         → EPS: YOK")
    
    # Check total holdings with price
    total = db.execute(text("""
        SELECT COUNT(*) FROM companies WHERE industry = 'Holdingler'
    """)).scalar()
    
    with_price = db.execute(text("""
        SELECT COUNT(DISTINCT c.ticker)
        FROM companies c
        JOIN company_metrics cm ON c.ticker = cm.ticker
        WHERE c.industry = 'Holdingler' AND cm.last_price IS NOT NULL
    """)).scalar()
    
    with_pe = db.execute(text("""
        SELECT COUNT(DISTINCT c.ticker)
        FROM companies c
        JOIN company_metrics cm ON c.ticker = cm.ticker
        WHERE c.industry = 'Holdingler' AND cm.pe_ratio IS NOT NULL
    """)).scalar()
    
    with_eps = db.execute(text("""
        SELECT COUNT(DISTINCT cr.ticker)
        FROM company_ratios cr
        JOIN companies c ON cr.ticker = c.ticker
        WHERE c.industry = 'Holdingler' AND cr.ratio_code = 'eps'
    """)).scalar()
    
    print(f"\n📈 Summary:")
    print(f"  Total Holdings: {total}")
    print(f"  With Price: {with_price}")
    print(f"  With P/E (in company_metrics): {with_pe}")
    print(f"  With EPS (in company_ratios): {with_eps}")
