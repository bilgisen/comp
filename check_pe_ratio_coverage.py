"""Check P/E ratio coverage across all sectors"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Check P/E coverage by industry
    results = db.execute(text("""
        SELECT 
            c.industry,
            COUNT(DISTINCT c.ticker) as total_companies,
            COUNT(DISTINCT CASE WHEN cm.last_price IS NOT NULL THEN c.ticker END) as with_price,
            COUNT(DISTINCT CASE WHEN cm.pe_ratio IS NOT NULL THEN c.ticker END) as with_pe,
            COUNT(DISTINCT CASE WHEN cr.ratio_code = 'eps' THEN c.ticker END) as with_eps
        FROM companies c
        LEFT JOIN company_metrics cm ON c.ticker = cm.ticker
        LEFT JOIN company_ratios cr ON c.ticker = cr.ticker AND cr.ratio_code = 'eps'
        WHERE c.is_active = TRUE AND c.industry IS NOT NULL
        GROUP BY c.industry
        ORDER BY total_companies DESC
    """)).fetchall()
    
    print("\n📊 P/E Ratio Coverage by Industry:\n")
    print(f"{'Industry':<30} {'Total':<8} {'Price':<8} {'P/E':<8} {'EPS':<8} {'Coverage':<12}")
    print("-" * 85)
    
    total_all = 0
    total_with_price = 0
    total_with_pe = 0
    total_with_eps = 0
    
    for row in results:
        industry = row.industry[:28] if row.industry else "Unknown"
        total = row.total_companies
        with_price = row.with_price
        with_pe = row.with_pe
        with_eps = row.with_eps
        
        coverage = f"{with_pe}/{total}" if total > 0 else "0/0"
        
        total_all += total
        total_with_price += with_price
        total_with_pe += with_pe
        total_with_eps += with_eps
        
        # Highlight industries with 0 P/E
        marker = "⚠️ " if with_pe == 0 else "   "
        
        print(f"{marker}{industry:<30} {total:<8} {with_price:<8} {with_pe:<8} {with_eps:<8} {coverage:<12}")
    
    print("-" * 85)
    print(f"{'TOTAL':<30} {total_all:<8} {total_with_price:<8} {total_with_pe:<8} {total_with_eps:<8}")
    
    print(f"\n📈 Summary:")
    print(f"  Total Companies: {total_all}")
    print(f"  With Price: {total_with_price} ({100*total_with_price/total_all:.1f}%)")
    print(f"  With P/E: {total_with_pe} ({100*total_with_pe/total_all:.1f}%)")
    print(f"  With EPS: {total_with_eps} ({100*total_with_eps/total_all:.1f}%)")
    
    if total_with_price == 0:
        print(f"\n⚠️  CRITICAL: NO companies have price data!")
        print(f"   company_metrics table appears to be empty or not populated.")
    elif total_with_pe == 0:
        print(f"\n⚠️  WARNING: Companies have price but NO P/E ratios!")
        print(f"   P/E calculation may not be working.")
