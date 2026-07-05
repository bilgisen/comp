"""Check yatırım ortaklıkları scores"""
import asyncio
from sqlalchemy import text
from core.database import get_async_db

async def check_scores():
    async for db in get_async_db():
        # Check if yatırım ortaklıkları have scores
        query = text("""
            SELECT 
                c.ticker, 
                c.name,
                c.industry,
                cs.score_genel,
                cs.score_sektor,
                cs.period_key
            FROM companies c
            LEFT JOIN company_scores cs ON c.ticker = cs.ticker 
                AND cs.period_key = (SELECT MAX(period_key) FROM company_scores WHERE is_stale = FALSE)
            WHERE c.industry = 'Yatırım Ortaklıkları'
            ORDER BY cs.score_genel DESC NULLS LAST
            LIMIT 10
        """)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        print("\n=== Yatırım Ortaklıkları Scores ===")
        for row in rows:
            print(f"{row.ticker:8} {row.name:30} Score: {row.score_genel or 'NULL':>6} Period: {row.period_key or 'NULL'}")
        
        # Check if they have financial data
        query2 = text("""
            SELECT ticker, period_key, COUNT(*) as ratio_count
            FROM company_ratios
            WHERE ticker IN (
                SELECT ticker FROM companies WHERE industry = 'Yatırım Ortaklıkları' LIMIT 5
            )
            GROUP BY ticker, period_key
            ORDER BY period_key DESC
            LIMIT 10
        """)
        
        result2 = await db.execute(query2)
        rows2 = result2.fetchall()
        
        print("\n=== Yatırım Ortaklıkları Financial Data ===")
        for row in rows2:
            print(f"{row.ticker:8} {row.period_key} Ratios: {row.ratio_count}")
        
        break

if __name__ == "__main__":
    asyncio.run(check_scores())
