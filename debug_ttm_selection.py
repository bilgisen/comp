"""
Debug TTM Period Selection for Banking
"""
import sys
import asyncio
from sqlalchemy import and_, desc
from core.database import SessionLocal
from models.financial import FinancialStatementRaw
from services.item_code_mapper import ItemCodeMapper


async def debug_ttm_selection():
    """Debug which period is used for banking TTM"""
    print("="*70)
    print("DEBUG: TTM Period Selection for Banking")
    print("="*70)
    
    db = SessionLocal()
    mapper = ItemCodeMapper(db)
    
    ticker = "GARAN"
    period_key = "2026Q1"
    financial_group = "UFRS_K"
    
    # Simulate the code from ratio_calculator
    statements = db.query(FinancialStatementRaw).filter(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.financial_group == financial_group
        )
    ).order_by(desc(FinancialStatementRaw.year), desc(FinancialStatementRaw.period)).all()
    
    print(f"\nAll statements for {ticker} (ordered by year DESC, period DESC):")
    print("-" * 70)
    
    periods_seen = set()
    for stmt in statements[:20]:  # First 20
        key = (stmt.year, stmt.period)
        if key not in periods_seen:
            print(f"  {stmt.year}Q{stmt.period//3} (period={stmt.period})")
            periods_seen.add(key)
    
    # Check annual statements
    annual_statements = [s for s in statements if s.period == 12]
    
    print(f"\n\nAnnual statements (period=12) found: {len(annual_statements)} records")
    print("-" * 70)
    
    if annual_statements:
        latest_annual = annual_statements[0]
        print(f"Latest annual: {latest_annual.year}Q4 (period={latest_annual.period})")
        print(f"Period key: {latest_annual.period_key}")
        
        # Get values for this year
        year_statements = [s for s in annual_statements if s.year == latest_annual.year]
        print(f"\nStatements for year {latest_annual.year}: {len(year_statements)} records")
        
        # Check specific fields
        for stmt in year_statements:
            semantic = mapper.get_semantic_name(stmt.item_code, financial_group)
            if semantic in ["operating_expenses", "total_operating_income"]:
                print(f"  {semantic:30s}: {stmt.value_try:>20,.2f}")
    
    # Now check what period_key we're calculating for
    print(f"\n\nTarget calculation:")
    print("-" * 70)
    print(f"  Requested period_key: {period_key}")
    print(f"  Using annual data from: {latest_annual.year}Q4")
    print(f"\n  ⚠️  PROBLEM: period_key='2026Q1' should use 2025Q4 data")
    print(f"      But if we're in 2026Q1, we might not have 2026Q4 yet!")
    print(f"      So using latest available annual (2025Q4) is CORRECT")
    
    db.close()


if __name__ == "__main__":
    asyncio.run(debug_ttm_selection())
