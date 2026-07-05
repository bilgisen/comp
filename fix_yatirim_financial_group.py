"""Fix yatırım ortaklıkları financial_group from UFRS_K to XI_29"""
import asyncio
from sqlalchemy import text
from core.database import get_async_db

async def fix_financial_group():
    async for db in get_async_db():
        # Update yatırım ortaklıkları to XI_29
        query = text("""
            UPDATE companies
            SET financial_group = 'XI_29'
            WHERE industry = 'Yatırım Ortaklıkları'
            RETURNING ticker, name, financial_group
        """)
        
        result = await db.execute(query)
        await db.commit()
        
        rows = result.fetchall()
        
        print(f"\n✅ Updated {len(rows)} yatırım ortaklıkları to XI_29:")
        for row in rows:
            print(f"  {row.ticker:8} {row.name:35} -> {row.financial_group}")
        
        break

if __name__ == "__main__":
    asyncio.run(fix_financial_group())
