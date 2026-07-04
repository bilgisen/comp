"""Check if banking-specific fields are mapped"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.database import SessionLocal
from services.item_code_mapper import ItemCodeMapper
from sqlalchemy import select, and_
from models.financial import FinancialStatementRaw

db = SessionLocal()
mapper = ItemCodeMapper(db)

# Fields needed for missing ratios
needed_fields = {
    "net_interest_margin": [
        "net_interest_income",      # Mapped from '3C'
        "total_assets"              # We use total_assets_avg as approximation
    ],
    "capital_adequacy": [
        "tier1_capital",            # NOT AVAILABLE (requires regulatory data)
        "risk_weighted_assets"      # NOT AVAILABLE (requires regulatory data)
    ],
    "cost_income_ratio": [
        "operating_expenses",       # Mapped from '3CG'
        "total_operating_income"    # Mapped from '3CE'
    ]
}

print("="*70)
print("BANKING FIELD MAPPING CHECK")
print("="*70)

for ratio, fields in needed_fields.items():
    print(f"\n{ratio.upper()}:")
    for field in fields:
        # Check if semantic name can be found
        result = mapper.get_semantic_name(field, "UFRS_K")
        status = "✅ MAPPED" if result else "❌ NOT MAPPED"
        print(f"  {field}: {status}")

# Check actual item codes from GARAN
print(f"\n{'='*70}")
print("GARAN AVAILABLE ITEM CODES (Sample)")
print(f"{'='*70}")

stmt = select(
    FinancialStatementRaw.item_code,
    FinancialStatementRaw.item_desc_tr
).where(
    and_(
        FinancialStatementRaw.ticker == "GARAN",
        FinancialStatementRaw.period_key == "2026Q1"
    )
).limit(20)

result = db.execute(stmt)
for item_code, desc in result.all():
    semantic = mapper.get_semantic_name(item_code, "UFRS_K")
    print(f"{item_code:20} -> {semantic or 'NOT MAPPED':30} | {desc[:40] if desc else 'N/A'}")

db.close()
