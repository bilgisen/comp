"""Check yatırım ortaklıkları financial_group"""
import asyncio
from sqlalchemy import text
from core.database import get_async_db

async def check_financial_group():
    async for db in get_async_db():
        query = text("""
            SELECT ticker, name, industry, financial_group
            FROM companies
            WHERE industry = 'Yatırım Ortaklıkları'
            ORDER BY ticker
            LIMIT 20
        """)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        print("\n=== Yatırım Ortaklıkları Financial Groups ===")
        financial_groups = set()
        for row in rows:
            print(f"{row.ticker:8} {row.name:35} FG: {row.financial_group}")
            financial_groups.add(row.financial_group)
        
        print(f"\n📊 Unique Financial Groups: {financial_groups}")
        
        # Check if any financial data exists for these financial groups
        for fg in financial_groups:
            query2 = text("""
                SELECT COUNT(DISTINCT ticker) as company_count,
                       COUNT(*) as statement_count
                FROM financial_statements_raw
                WHERE financial_group = :fg
            """)
            result2 = await db.execute(query2, {"fg": fg})
            row2 = result2.fetchone()
            print(f"  {fg}: {row2.company_count} companies, {row2.statement_count} statements")
        
        break

if __name__ == "__main__":
    asyncio.run(check_financial_group())
