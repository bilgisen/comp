"""Test API endpoint locally"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Test the same query API uses
    result = db.execute(text("""
        SELECT 
            c.ticker,
            c.name as company_name,
            c.industry,
            c.market_cap,
            c.city,
            cs.score_genel as score,
            cm.last_price,
            cm.pe_ratio
        FROM companies c
        LEFT JOIN company_scores cs ON c.ticker = cs.ticker 
            AND cs.period_key = (SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE)
        LEFT JOIN company_metrics cm ON c.ticker = cm.ticker
        WHERE c.is_active = TRUE
          AND c.industry = 'Holdingler'
          AND c.ticker IN ('SAHOL', 'KCHOL')
        ORDER BY cs.score_genel DESC NULLS LAST
    """)).fetchall()
    
    print("\n📊 Holdings with Price Data:\n")
    print(f"{'Ticker':<8} {'Name':<20} {'Price':<10} {'P/E':<10} {'Score':<10}")
    print("-" * 65)
    
    for row in result:
        price_str = f"{row.last_price:.2f}" if row.last_price else "N/A"
        pe_str = f"{row.pe_ratio:.2f}" if row.pe_ratio else "N/A"
        score_str = f"{row.score:.2f}" if row.score else "N/A"
        
        print(f"{row.ticker:<8} {row.company_name:<20} {price_str:<10} {pe_str:<10} {score_str:<10}")
