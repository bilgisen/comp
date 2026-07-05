"""Debug insurance company data structure"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Get detailed data for ANSGR and ANHYT
    for ticker in ['ANSGR', 'ANHYT']:
        print(f"\n{'='*60}")
        print(f"🔍 {ticker} - Detailed Analysis")
        print('='*60)
        
        # Get all periods with ratios
        ratio_periods = db.execute(text("""
            SELECT DISTINCT period_key, COUNT(*) as ratio_count
            FROM company_ratios
            WHERE ticker = :ticker
            GROUP BY period_key
            ORDER BY period_key DESC
        """), {"ticker": ticker}).fetchall()
        
        print(f"\n📊 Ratio Periods:")
        for period, count in ratio_periods:
            print(f"  {period}: {count} ratios")
        
        # Get all periods with scores
        score_periods = db.execute(text("""
            SELECT period_key, score_genel
            FROM company_scores
            WHERE ticker = :ticker
            ORDER BY period_key DESC
        """), {"ticker": ticker}).fetchall()
        
        print(f"\n💯 Score Periods:")
        if score_periods:
            for period, score in score_periods:
                score_str = f"{score:.2f}" if score is not None else "NULL"
                print(f"  {period}: {score_str}")
        else:
            print("  No scores found")
        
        # Get ratios for latest period
        if ratio_periods:
            latest_period = ratio_periods[0][0]
            ratios = db.execute(text("""
                SELECT ratio_code, ratio_value
                FROM company_ratios
                WHERE ticker = :ticker AND period_key = :period_key
            """), {"ticker": ticker, "period_key": latest_period}).fetchall()
            
            print(f"\n📈 Ratios for {latest_period}:")
            for code, value in ratios:
                print(f"  {code}: {value:.6f}")
            
            # Calculate what the score should be
            ratio_dict = {r[0]: r[1] for r in ratios}
            roe = ratio_dict.get('roe', 0) or 0
            roa = ratio_dict.get('roa', 0) or 0
            score = min(max((roe * 300 + roa * 700), 0), 100)
            
            print(f"\n🎯 Calculated Score: {score:.2f} (ROE={roe:.4f}, ROA={roa:.4f})")
