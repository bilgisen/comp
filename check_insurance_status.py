import asyncpg
import asyncio

async def check():
    conn = await asyncpg.connect(
        host='aws-0-eu-central-1.pooler.supabase.com',
        port=6543,
        user='postgres.mrvgzgsbfvmzbllddstw',
        password='12102003Hasan.',
        database='postgres'
    )
    
    # Get insurance companies
    companies = await conn.fetch("""
        SELECT symbol, name 
        FROM companies 
        WHERE industry_slug = 'sigortacilik'
        ORDER BY symbol
    """)
    
    print('\nSigorta Şirketleri - Ratio ve Score Durumu:\n')
    for comp in companies:
        ratio_count = await conn.fetchval("""
            SELECT COUNT(*) FROM company_ratios 
            WHERE symbol = $1
        """, comp['symbol'])
        
        score = await conn.fetchval("""
            SELECT score FROM company_scores 
            WHERE symbol = $1
        """, comp['symbol'])
        
        print(f'{comp["symbol"]:6} {comp["name"]:30} Ratios: {ratio_count:2}  Score: {score if score else "YOK"}')
    
    await conn.close()

asyncio.run(check())
