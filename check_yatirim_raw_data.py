"""Check raw financial data for yatırım ortaklıkları"""
import asyncio
from sqlalchemy import text
from core.database import get_async_db

async def check_raw_data():
    async for db in get_async_db():
        # Check if they have ANY financial statements
        query = text("""
            SELECT ticker, period_key, financial_group, COUNT(*) as item_count
            FROM financial_statements_raw
            WHERE ticker IN (
                SELECT ticker FROM companies WHERE industry = 'Yatırım Ortaklıkları' LIMIT 5
            )
            GROUP BY ticker, period_key, financial_group
            ORDER BY period_key DESC, ticker
            LIMIT 20
        """)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        print("\n=== Raw Financial Statements for Yatırım Ortaklıkları ===")
        if rows:
            for row in rows:
                print(f"{row.ticker:8} {row.period_key} {row.financial_group:20} Items: {row.item_count}")
        else:
            print("❌ NO FINANCIAL DATA FOUND!")
        
        # Check bootstrap status
        query2 = text("""
            SELECT ticker, name, is_active, industry, sector_main
            FROM companies
            WHERE industry = 'Yatırım Ortaklıkları'
            LIMIT 10
        """)
        
        result2 = await db.execute(query2)
        rows2 = result2.fetchall()
        
        print("\n=== Yatırım Ortaklıkları Company Status ===")
        for row in rows2:
            print(f"{row.ticker:8} {row.name:35} Active: {row.is_active} Sector: {row.sector_main or 'NULL'}")
        
        break

if __name__ == "__main__":
    asyncio.run(check_raw_data())
