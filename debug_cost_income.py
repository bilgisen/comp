"""
Debug Cost/Income Ratio Calculation
"""
import sys
from sqlalchemy import select, and_
from core.database import SessionLocal
from models.financial import FinancialStatementRaw
from services.item_code_mapper import ItemCodeMapper


def debug_cost_income():
    """Debug cost/income ratio calculation"""
    print("="*70)
    print("DEBUG: Cost/Income Ratio Calculation")
    print("="*70)
    
    db = SessionLocal()
    mapper = ItemCodeMapper(db)
    
    ticker = "GARAN"
    
    # Get all 2025 data
    stmt = select(FinancialStatementRaw).where(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.year == 2025,
            FinancialStatementRaw.financial_group == "UFRS_K"
        )
    ).order_by(FinancialStatementRaw.period)
    
    statements = db.execute(stmt).scalars().all()
    
    # Group by period
    periods = {}
    for stmt in statements:
        if stmt.period not in periods:
            periods[stmt.period] = {}
        
        semantic = mapper.get_semantic_name(stmt.item_code, "UFRS_K")
        if semantic:
            periods[stmt.period][semantic] = stmt.value_try
    
    print(f"\nGARAN 2025 Periods Available: {list(periods.keys())}")
    print("="*70)
    
    # Check operating_expenses and total_operating_income in each period
    for period in sorted(periods.keys()):
        data = periods[period]
        op_exp = data.get("operating_expenses")
        tot_op_inc = data.get("total_operating_income")
        
        print(f"\n2025 Q{period//3}:")
        print(f"  Operating Expenses:      {op_exp:>20,.2f}" if op_exp else "  Operating Expenses:      NOT FOUND")
        print(f"  Total Operating Income:  {tot_op_inc:>20,.2f}" if tot_op_inc else "  Total Operating Income:  NOT FOUND")
        
        if op_exp and tot_op_inc:
            ratio = op_exp / tot_op_inc
            print(f"  Cost/Income Ratio:       {ratio:>20.6f} ({ratio*100:.4f}%)")
    
    # Now check how TTM would calculate
    print("\n" + "="*70)
    print("TTM CALCULATION (Banking uses annual data):")
    print("="*70)
    
    # Banking uses annual (period=12) directly as TTM
    if 12 in periods:
        annual_data = periods[12]
        op_exp_annual = annual_data.get("operating_expenses")
        tot_op_inc_annual = annual_data.get("total_operating_income")
        
        print(f"\nAnnual 2025Q4 (period=12):")
        print(f"  Operating Expenses:      {op_exp_annual:>20,.2f}" if op_exp_annual else "  NOT FOUND")
        print(f"  Total Operating Income:  {tot_op_inc_annual:>20,.2f}" if tot_op_inc_annual else "  NOT FOUND")
        
        if op_exp_annual and tot_op_inc_annual:
            ratio = op_exp_annual / tot_op_inc_annual
            print(f"  Cost/Income Ratio:       {ratio:>20.6f} ({ratio*100:.4f}%)")
            print(f"\n  ✅ This matches the test expectation!")
    
    # Check if there's confusion with cumulative vs quarterly
    print("\n" + "="*70)
    print("ANALYSIS:")
    print("="*70)
    print("Banking sector uses annual (cumulative) data directly for TTM.")
    print("If system calculated 2.94%, it might be using a different field")
    print("or there's an issue with TTM mapping for banking ratios.")
    
    db.close()


if __name__ == "__main__":
    debug_cost_income()
