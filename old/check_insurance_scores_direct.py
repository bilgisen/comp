"""Check insurance company scores directly from database"""
from sqlalchemy import text
from core.database import SessionLocal

with SessionLocal() as db:
    # Get insurance companies with scores
    results = db.execute(text("""
        SELECT c.ticker, c.name, cs.score_genel, cs.period_key,
               (SELECT COUNT(*) FROM company_ratios WHERE ticker = c.ticker) as ratio_count
        FROM companies c
        LEFT JOIN company_scores cs ON c.ticker = cs.ticker
        WHERE c.industry = 'Sigortacılık' AND c.is_active = TRUE
        ORDER BY cs.score_genel DESC NULLS LAST, c.ticker
    """)).fetchall()
    
    print("\n📊 Sigortacılık Şirketleri - Score Durumu:\n")
    print(f"{'Ticker':<8} {'Name':<30} {'Score':<10} {'Period':<12} {'Ratios':<8}")
    print("-" * 75)
    
    for ticker, name, score, period, ratio_count in results:
        score_str = f"{score:.1f}" if score else "YOK"
        period_str = period if period else "-"
        print(f"{ticker:<8} {name:<30} {score_str:<10} {period_str:<12} {ratio_count:<8}")
    
    # Count scored vs total
    scored = sum(1 for r in results if r[2] is not None)
    total = len(results)
    print(f"\n✅ {scored}/{total} sigorta şirketi score'a sahip")
