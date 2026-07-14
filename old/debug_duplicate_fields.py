"""
Debug Duplicate Operating Expenses
"""
import sys
from sqlalchemy import select, and_
from core.database import SessionLocal
from models.financial import FinancialStatementRaw
from services.item_code_mapper import ItemCodeMapper


def debug_duplicates():
    """Find duplicate semantic mappings"""
    print("="*70)
    print("DEBUG: Duplicate Operating Expenses")
    print("="*70)
    
    db = SessionLocal()
    mapper = ItemCodeMapper(db)
    
    ticker = "GARAN"
    year = 2025
    period = 12
    
    # Get all statements for this period
    stmt = select(FinancialStatementRaw).where(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.year == year,
            FinancialStatementRaw.period == period,
            FinancialStatementRaw.financial_group == "UFRS_K"
        )
    )
    
    statements = db.execute(stmt).scalars().all()
    
    # Group by semantic name
    semantic_groups = {}
    for s in statements:
        semantic = mapper.get_semantic_name(s.item_code, "UFRS_K")
        if semantic:
            if semantic not in semantic_groups:
                semantic_groups[semantic] = []
            semantic_groups[semantic].append({
                "item_code": s.item_code,
                "value": s.value_try,
                "desc": s.item_desc_tr
            })
    
    # Find duplicates
    print(f"\nGARAN {year}Q{period//3} - Checking for duplicate mappings:")
    print("-" * 70)
    
    for semantic in ["operating_expenses", "total_operating_income", "net_interest_income"]:
        if semantic in semantic_groups:
            items = semantic_groups[semantic]
            print(f"\n{semantic}:")
            if len(items) > 1:
                print(f"  ⚠️  {len(items)} items map to this semantic name!")
                for item in items:
                    print(f"    {item['item_code']:10s}: {item['value']:>20,.2f} - {item['desc'][:60]}")
            else:
                print(f"  ✅ Single mapping")
                for item in items:
                    print(f"    {item['item_code']:10s}: {item['value']:>20,.2f}")
    
    # Check the hardcoded mapping
    print("\n" + "="*70)
    print("CHECKING HARDCODED UFRS_K_MAPPINGS:")
    print("="*70)
    
    # Access class variable directly
    mappings = mapper.UFRS_K_MAPPINGS
    
    # Find all item_codes that map to operating_expenses
    op_exp_codes = [code for code, semantic in mappings.items() if semantic == "operating_expenses"]
    print(f"\nItem codes mapping to 'operating_expenses': {op_exp_codes}")
    
    tot_op_inc_codes = [code for code, semantic in mappings.items() if semantic == "total_operating_income"]
    print(f"Item codes mapping to 'total_operating_income': {tot_op_inc_codes}")
    
    db.close()


if __name__ == "__main__":
    debug_duplicates()
