"""
Test Banking Ratio Fix - Verify net_interest_margin and cost_income_ratio
Tests the recently modified banking ratio calculations
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from decimal import Decimal
from sqlalchemy import select, and_
from core.database import SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw, CompanyRatio
from services.item_code_mapper import ItemCodeMapper


def test_banking_field_availability():
    """Test if required fields for banking ratios are available in data"""
    print("\n" + "="*70)
    print("TEST 1: Banking Field Availability Check")
    print("="*70)
    
    db = SessionLocal()
    
    # Select GARAN as reference banking company
    ticker = "GARAN"
    
    # Get item codes for GARAN
    stmt = select(
        FinancialStatementRaw.item_code,
        FinancialStatementRaw.item_desc_tr,
        FinancialStatementRaw.value_try
    ).where(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.year == 2025,
            FinancialStatementRaw.period == 12
        )
    )
    
    result = db.execute(stmt).all()
    
    # Check for required item codes
    mapper = ItemCodeMapper(db)
    
    required_fields = {
        "net_interest_income": "3C",
        "operating_expenses": "3CG", 
        "total_operating_income": "3CE",
        "total_assets": "1Z"
    }
    
    print(f"\nChecking GARAN (2025Q4) for required fields:")
    print("-" * 70)
    
    found_fields = {}
    for row in result:
        semantic = mapper.get_semantic_name(row.item_code, "UFRS_K")
        if semantic in required_fields.keys():
            found_fields[semantic] = {
                "item_code": row.item_code,
                "value": row.value_try,
                "name": row.item_desc_tr
            }
    
    for field_name, item_code in required_fields.items():
        if field_name in found_fields:
            print(f"✅ {field_name:30s} | {found_fields[field_name]['item_code']:6s} | {found_fields[field_name]['value']:>15,.2f}")
        else:
            print(f"❌ {field_name:30s} | {item_code:6s} | NOT FOUND")
    
    db.close()
    
    # Summary
    print("\n" + "-" * 70)
    print(f"Found: {len(found_fields)}/{len(required_fields)} required fields")
    
    return len(found_fields) == len(required_fields)


def test_banking_ratio_calculation():
    """Test if banking ratios are being calculated correctly"""
    print("\n" + "="*70)
    print("TEST 2: Banking Ratio Calculation Check")
    print("="*70)
    
    db = SessionLocal()
    
    # Select banking companies
    banking_companies = ["GARAN", "AKBNK", "YKBNK"]
    
    for ticker in banking_companies:
        print(f"\n{ticker}:")
        print("-" * 70)
        
        # Get latest ratios
        stmt = select(CompanyRatio).where(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.period_key == "2026Q1"
            )
        )
        
        ratios = db.execute(stmt).scalars().all()
        
        banking_ratios = [
            "net_interest_margin",
            "loan_to_deposit", 
            "npl_ratio",
            "cost_income_ratio",
            "roe",
            "roa"
        ]
        
        found_ratios = {}
        for ratio in ratios:
            if ratio.ratio_code in banking_ratios:
                found_ratios[ratio.ratio_code] = ratio.ratio_value
        
        for ratio_code in banking_ratios:
            if ratio_code in found_ratios:
                value = found_ratios[ratio_code]
                if value is not None:
                    print(f"  ✅ {ratio_code:25s}: {float(value):>10.4f}")
                else:
                    print(f"  ⚠️  {ratio_code:25s}: NULL")
            else:
                print(f"  ❌ {ratio_code:25s}: NOT CALCULATED")
        
        # Summary
        calculated = len([v for v in found_ratios.values() if v is not None])
        print(f"\n  Summary: {calculated}/{len(banking_ratios)} ratios calculated")
    
    db.close()


def test_net_interest_margin_formula():
    """Test net_interest_margin calculation manually"""
    print("\n" + "="*70)
    print("TEST 3: Net Interest Margin Formula Verification")
    print("="*70)
    
    db = SessionLocal()
    mapper = ItemCodeMapper(db)
    
    ticker = "GARAN"
    
    # Get 2025 annual data for TTM
    stmt = select(FinancialStatementRaw).where(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.year == 2025,
            FinancialStatementRaw.period == 12,
            FinancialStatementRaw.financial_group == "UFRS_K"
        )
    )
    
    statements = db.execute(stmt).scalars().all()
    
    # Extract values
    net_interest_income = None
    total_assets = None
    
    for stmt in statements:
        semantic = mapper.get_semantic_name(stmt.item_code, "UFRS_K")
        if semantic == "net_interest_income":
            net_interest_income = stmt.value_try
        elif semantic == "total_assets":
            total_assets = stmt.value_try
    
    print(f"\nGARAN 2025Q4 Data:")
    print("-" * 70)
    print(f"Net Interest Income (3C): {net_interest_income:>20,.2f} TRY" if net_interest_income else "❌ Not found")
    print(f"Total Assets (1Z):        {total_assets:>20,.2f} TRY" if total_assets else "❌ Not found")
    
    if net_interest_income and total_assets:
        # Calculate NIM (as decimal, not percentage)
        nim = net_interest_income / total_assets
        
        print(f"\nCalculated NIM: {nim:.6f} ({nim*100:.4f}%)")
        print(f"Formula: Net Interest Income / Total Assets")
        print(f"Note: Using total_assets as approximation for interest_earning_assets")
        
        # Get system calculated value
        ratio_stmt = select(CompanyRatio).where(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.period_key == "2026Q1",
                CompanyRatio.ratio_code == "net_interest_margin"
            )
        )
        
        system_ratio = db.execute(ratio_stmt).scalar_one_or_none()
        
        if system_ratio and system_ratio.ratio_value:
            system_value = float(system_ratio.ratio_value)
            print(f"\nSystem Calculated NIM: {system_value:.6f} ({system_value*100:.4f}%)")
            
            # Compare
            diff = abs(float(nim) - system_value)
            diff_pct = (diff / float(nim) * 100) if nim != 0 else 0
            
            print(f"Difference: {diff:.6f} ({diff_pct:.2f}%)")
            
            if diff_pct < 5:
                print("✅ PASS - Within 5% tolerance")
                return True
            else:
                print("⚠️  WARNING - Difference > 5%")
                return False
        else:
            print("\n❌ System value not found - Ratio not calculated")
            return False
    else:
        print("\n❌ Required fields not found")
        return False
    
    db.close()


def test_cost_income_ratio_formula():
    """Test cost_income_ratio calculation manually"""
    print("\n" + "="*70)
    print("TEST 4: Cost/Income Ratio Formula Verification")
    print("="*70)
    
    db = SessionLocal()
    mapper = ItemCodeMapper(db)
    
    ticker = "GARAN"
    
    # Get 2025 annual data for TTM
    stmt = select(FinancialStatementRaw).where(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.year == 2025,
            FinancialStatementRaw.period == 12,
            FinancialStatementRaw.financial_group == "UFRS_K"
        )
    )
    
    statements = db.execute(stmt).scalars().all()
    
    # Extract values
    operating_expenses = None
    total_operating_income = None
    
    for stmt in statements:
        semantic = mapper.get_semantic_name(stmt.item_code, "UFRS_K")
        if semantic == "operating_expenses":
            operating_expenses = stmt.value_try
        elif semantic == "total_operating_income":
            total_operating_income = stmt.value_try
    
    print(f"\nGARAN 2025Q4 Data:")
    print("-" * 70)
    print(f"Operating Expenses (3CG):      {operating_expenses:>20,.2f} TRY" if operating_expenses else "❌ Not found")
    print(f"Total Operating Income (3CE):  {total_operating_income:>20,.2f} TRY" if total_operating_income else "❌ Not found")
    
    if operating_expenses and total_operating_income:
        # Calculate Cost/Income Ratio (as decimal, not percentage)
        cost_income = abs(operating_expenses) / total_operating_income
        
        print(f"\nCalculated Cost/Income Ratio: {cost_income:.6f} ({cost_income*100:.4f}%)")
        print(f"Formula: Operating Expenses / Total Operating Income")
        
        # Get system calculated value
        ratio_stmt = select(CompanyRatio).where(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.period_key == "2026Q1",
                CompanyRatio.ratio_code == "cost_income_ratio"
            )
        )
        
        system_ratio = db.execute(ratio_stmt).scalar_one_or_none()
        
        if system_ratio and system_ratio.ratio_value:
            system_value = float(system_ratio.ratio_value)
            print(f"\nSystem Calculated: {system_value:.6f} ({system_value*100:.4f}%)")
            
            # Compare
            diff = abs(float(cost_income) - system_value)
            diff_pct = (diff / float(cost_income) * 100) if cost_income != 0 else 0
            
            print(f"Difference: {diff:.6f} ({diff_pct:.2f}%)")
            
            if diff_pct < 5:
                print("✅ PASS - Within 5% tolerance")
                return True
            else:
                print("⚠️  WARNING - Difference > 5%")
                return False
        else:
            print("\n❌ System value not found - Ratio not calculated")
            return False
    else:
        print("\n❌ Required fields not found")
        return False
    
    db.close()


def main():
    """Run all banking ratio tests"""
    print("\n" + "="*70)
    print("BANKING RATIO FIX - TEST SUITE")
    print("="*70)
    print("\nTesting recently modified banking ratio calculations:")
    print("1. Field availability check")
    print("2. Banking ratio calculation check")
    print("3. Net Interest Margin formula verification")
    print("4. Cost/Income Ratio formula verification")
    
    results = {
        "field_availability": test_banking_field_availability(),
        "nim_formula": test_net_interest_margin_formula(),
        "cost_income_formula": test_cost_income_ratio_formula()
    }
    
    test_banking_ratio_calculation()
    
    # Final Summary
    print("\n" + "="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30s}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print("\n" + "-" * 70)
    print(f"Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✅ All banking ratio tests PASSED!")
        print("\nNext Steps:")
        print("1. Banking ratios are working correctly")
        print("2. Wait 15-30 minutes for API rate limit reset")
        print("3. Run TTM backfill: python scripts/backfill_historical_data.py")
    else:
        print("\n⚠️  Some tests failed - review results above")


if __name__ == "__main__":
    main()
