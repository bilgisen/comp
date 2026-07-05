"""Check bank scores and ratios"""
import asyncio
from sqlalchemy import text
from core.database import get_async_db

async def check_banks():
    async for db in get_async_db():
        # Check banks
        query = text("""
            SELECT 
                c.ticker,
                c.name,
                c.financial_group,
                COUNT(DISTINCT fsr.period_key) as periods_count,
                COUNT(DISTINCT cr.ratio_code) as ratios_count,
                cs.score_genel
            FROM companies c
            LEFT JOIN financial_statements_raw fsr ON c.ticker = fsr.ticker
            LEFT JOIN company_ratios cr ON c.ticker = cr.ticker
            LEFT JOIN company_scores cs ON c.ticker = cs.ticker 
                AND cs.period_key = (SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE)
            WHERE c.industry = 'Bankacılık'
            GROUP BY c.ticker, c.name, c.financial_group, cs.score_genel
            ORDER BY c.name
            LIMIT 15
        """)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        print("\n=== Bankacılık Sektörü Durum ===")
        print(f"{'Ticker':<10} {'Name':<25} {'FG':<10} {'Periods':<8} {'Ratios':<8} {'Score':<8}")
        print("="*85)
        for row in rows:
            score = f"{row.score_genel:.1f}" if row.score_genel else "NULL"
            print(f"{row.ticker:<10} {row.name:<25} {row.financial_group:<10} {row.periods_count:<8} {row.ratios_count:<8} {score:<8}")
        
        break

if __name__ == "__main__":
    asyncio.run(check_banks())
