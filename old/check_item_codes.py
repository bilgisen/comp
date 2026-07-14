"""Check actual item codes in database"""
from core.database import SessionLocal
from models.financial import FinancialStatementRaw
from sqlalchemy import text

with SessionLocal() as db:
    # A1YEN için tüm item code'ları al
    items = db.execute(text('''
        SELECT DISTINCT item_code, item_desc_tr, COUNT(*) as cnt
        FROM financial_statements_raw
        WHERE ticker = 'A1YEN'
        GROUP BY item_code, item_desc_tr
        ORDER BY item_code
    ''')).fetchall()
    
    print('A1YEN ITEM CODES:')
    print('='*80)
    for item in items:
        desc = item[1][:50] if item[1] else "N/A"
        print(f"{item[0]:<10} {desc:<50} ({item[2]} rows)")
