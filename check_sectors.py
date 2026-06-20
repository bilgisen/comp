import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://avnadmin:H3m7baA6K5Ix1NoLWGsM@postgresql-77b1bcb9-o033531ff.database.cloud.ovh.net:20184/compengine"

async def check_ratio_values():
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT ticker, ratio_code, ratio_value FROM company_ratios WHERE ticker IN ('THYAO', 'PGSUS', 'CLEBI') AND ratio_code = 'current_ratio';"))
        records = res.fetchall()
        print("Ratio values for current_ratio:")
        for r in records:
            print(f"  - {r[0]}: {r[1]} = {float(r[2]) if r[2] is not None else 'None'}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_ratio_values())
