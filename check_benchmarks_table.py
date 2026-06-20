import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://avnadmin:H3m7baA6K5Ix1NoLWGsM@postgresql-77b1bcb9-o033531ff.database.cloud.ovh.net:20184/compengine"

async def check_benchmarks():
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT id, sector_main, ratio_code, period_key, n_peers, reliability, is_stale FROM sector_benchmarks WHERE sector_main = 'Ulaştırma & Lojistik';"))
        records = res.fetchall()
        print("Benchmarks in database:")
        for r in records:
            print(f"  - ID: {r[0]}, Sector: {r[1]}, Ratio: {r[2]}, Period: {r[3]}, N: {r[4]}, Reliability: {r[5]}, Stale: {r[6]}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_benchmarks())
