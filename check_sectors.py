import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://avnadmin:H3m7baA6K5Ix1NoLWGsM@postgresql-77b1bcb9-o033531ff.database.cloud.ovh.net:20184/compengine"

async def test_peer_query():
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.connect() as conn:
        query = text("""
            SELECT 
                cr.ticker,
                cr.ratio_value,
                c.market_cap,
                (
                    SELECT COUNT(*) 
                    FROM company_ratios cr2 
                    WHERE cr2.ticker = cr.ticker 
                      AND cr2.ratio_code = :ratio_code
                ) as available_periods
            FROM company_ratios cr
            JOIN companies c ON cr.ticker = c.ticker
            WHERE c.sector_main = :sector_main
              AND cr.ratio_code = :ratio_code  
              AND cr.period_key = :period_key
              AND c.is_active = true
        """)
        
        result = await conn.execute(query, {
            "sector_main": "Ulaştırma & Lojistik",
            "ratio_code": "current_ratio",
            "period_key": "2026Q1"
        })
        rows = result.fetchall()
        print(f"Peer query rows (count={len(rows)}):")
        for row in rows:
            print(f"  - Ticker: {row[0]}, Value: {float(row[1]) if row[1] is not None else 'None'}, Cap: {float(row[2]) if row[2] else 0}, Periods: {row[3]}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_peer_query())
