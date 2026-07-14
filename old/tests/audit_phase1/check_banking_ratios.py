"""
Banking Ratio Coverage Analysis
Checks which banking-specific ratios are configured vs actually calculated
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import select, and_, func
from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from calculate_ratios_sync import SyncRatioCalculator

print("="*70)
print("BANKING RATIO COVERAGE ANALYSIS")
print("="*70)

db = SessionLocal()

# Get banking companies
banking_companies = db.execute(
    select(Company.ticker, Company.name).where(
        and_(
            Company.is_active == True,
            Company.financial_group.in_(["UFRS_K", "UFRS_F", "UFRS_S"])
        )
    ).limit(10)
).all()

print(f"\nBanking Companies (Sample 10): {len(banking_companies)}")
for ticker, name in banking_companies:
    print(f"  • {ticker} - {name}")

# Check configured banking ratios
calculator = SyncRatioCalculator
banking_ratios_config = calculator.BANKING_RATIOS

print(f"\n{'='*70}")
print(f"CONFIGURED BANKING RATIOS: {len(banking_ratios_config)}")
print(f"{'='*70}")
for ratio_code in sorted(banking_ratios_config.keys()):
    print(f"  • {ratio_code}")

# Check actually calculated ratios for sample companies
print(f"\n{'='*70}")
print("CALCULATED RATIOS PER COMPANY")
print(f"{'='*70}")

for ticker, name in banking_companies[:5]:  # Top 5
    stmt = select(
        CompanyRatio.ratio_code
    ).where(
        and_(
            CompanyRatio.ticker == ticker,
            CompanyRatio.period_key.like('2026%')
        )
    ).distinct()
    
    result = db.execute(stmt)
    calculated_ratios = [row[0] for row in result.all()]
    
    print(f"\n{ticker} - {len(calculated_ratios)} ratios:")
    for ratio in sorted(calculated_ratios):
        in_banking_config = "✓" if ratio in banking_ratios_config else "✗"
        print(f"  {in_banking_config} {ratio}")

# Gap analysis
print(f"\n{'='*70}")
print("GAP ANALYSIS")
print(f"{'='*70}")

# Get all distinct ratio codes calculated for banking sector
all_calculated = db.execute(
    select(func.distinct(CompanyRatio.ratio_code)).join(
        Company,
        Company.ticker == CompanyRatio.ticker
    ).where(
        Company.financial_group.in_(["UFRS_K", "UFRS_F", "UFRS_S"])
    )
).scalars().all()

print(f"\nTotal Distinct Ratios Calculated for Banking: {len(all_calculated)}")

# Configured but not calculated
configured_not_calculated = set(banking_ratios_config.keys()) - set(all_calculated)
if configured_not_calculated:
    print(f"\n⚠️  CONFIGURED BUT NOT CALCULATED ({len(configured_not_calculated)}):")
    for ratio in sorted(configured_not_calculated):
        print(f"  • {ratio}")
else:
    print(f"\n✅ All configured ratios are being calculated")

# Calculated but not in banking config (using default ratios)
calculated_not_configured = set(all_calculated) - set(banking_ratios_config.keys())
if calculated_not_configured:
    print(f"\nℹ️  CALCULATED (from DEFAULT_RATIOS) ({len(calculated_not_configured)}):")
    for ratio in sorted(calculated_not_configured):
        print(f"  • {ratio}")

# Expected banking ratios (industry standard)
EXPECTED_BANKING_RATIOS = {
    "net_interest_margin",
    "loan_to_deposit",
    "npl_ratio",
    "capital_adequacy",
    "cost_income_ratio",
    "roe",
    "roa",
    "nim",  # Net Interest Margin
    "tier1_ratio",
    "leverage_ratio"
}

missing_expected = EXPECTED_BANKING_RATIOS - set(all_calculated)
if missing_expected:
    print(f"\n⚠️  MISSING EXPECTED BANKING RATIOS ({len(missing_expected)}):")
    for ratio in sorted(missing_expected):
        print(f"  • {ratio}")

print(f"\n{'='*70}")
print("RECOMMENDATION")
print(f"{'='*70}")
print("""
Based on this analysis:

1. If configured ratios are not calculated:
   - Check data availability (required fields missing?)
   - Check formula logic (division by zero, NULL handling)
   
2. If expected ratios are missing:
   - Add to BANKING_RATIOS configuration
   - Ensure item code mappings exist for required fields
   
3. Review sector-specific ratio application:
   - Verify SECTOR_RATIOS mapping
   - Ensure banking companies use BANKING_RATIOS
""")

db.close()
