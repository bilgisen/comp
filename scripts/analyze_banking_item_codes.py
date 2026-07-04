"""
Analyze Banking Item Codes to Create Mappings
Extracts all item codes from major banks to identify banking-specific codes
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, and_, func
from core.database import SessionLocal
from models.financial import FinancialStatementRaw

db = SessionLocal()

# Major banks
MAJOR_BANKS = ['GARAN', 'AKBNK', 'YKBNK', 'ISCTR', 'HALKB']

print("="*80)
print("BANKING ITEM CODE ANALYSIS")
print("="*80)

# Get all distinct item codes from major banks
all_codes = {}

for ticker in MAJOR_BANKS:
    stmt = select(
        FinancialStatementRaw.item_code,
        FinancialStatementRaw.item_desc_tr,
        FinancialStatementRaw.item_desc_en
    ).where(
        and_(
            FinancialStatementRaw.ticker == ticker,
            FinancialStatementRaw.period_key == '2026Q1',
            FinancialStatementRaw.financial_group == 'UFRS_K'
        )
    ).distinct()
    
    result = db.execute(stmt)
    codes = {row[0]: (row[1], row[2]) for row in result.all()}
    
    print(f"\n{ticker}: {len(codes)} unique codes")
    all_codes[ticker] = codes

# Find common codes across all banks
all_code_sets = [set(codes.keys()) for codes in all_codes.values()]
common_codes = set.intersection(*all_code_sets) if all_code_sets else set()

print(f"\n{'='*80}")
print(f"COMMON CODES ACROSS ALL BANKS: {len(common_codes)}")
print(f"{'='*80}")

# Categorize by keywords
banking_keywords = {
    "interest": ["FAİZ", "INTEREST", "NİM"],
    "loans": ["KREDİ", "LOAN", "ALACAK"],
    "deposits": ["MEVDUAT", "DEPOSIT"],
    "capital": ["SERMAYE", "CAPITAL", "ÖZKAYNAKLAR", "EQUITY"],
    "npl": ["TAKİP", "NPL", "NON-PERFORMING"],
    "assets": ["AKTİF", "ASSET", "VARLIK"],
    "risk": ["RİSK", "RISK"],
}

categorized = {key: [] for key in banking_keywords.keys()}
categorized["other"] = []

for code in sorted(common_codes):
    desc_tr, desc_en = all_codes[MAJOR_BANKS[0]][code]
    desc = (desc_tr or "") + " " + (desc_en or "")
    desc_upper = desc.upper()
    
    matched = False
    for category, keywords in banking_keywords.items():
        if any(kw in desc_upper for kw in keywords):
            categorized[category].append((code, desc_tr, desc_en))
            matched = True
            break
    
    if not matched:
        categorized["other"].append((code, desc_tr, desc_en))

# Print categorized codes
for category, codes in categorized.items():
    if codes and category != "other":
        print(f"\n{'='*80}")
        print(f"{category.upper()} RELATED ({len(codes)} codes)")
        print(f"{'='*80}")
        for code, desc_tr, desc_en in codes[:10]:  # Show first 10
            print(f"{code:15} | {desc_tr[:50] if desc_tr else 'N/A'}")

# Generate mapping suggestions
print(f"\n{'='*80}")
print("SUGGESTED MAPPINGS FOR MISSING BANKING RATIOS")
print(f"{'='*80}")

suggestions = {
    "net_interest_income": {
        "keywords": ["NET FAİZ GELİRİ", "NET INTEREST INCOME"],
        "candidates": []
    },
    "interest_earning_assets": {
        "keywords": ["FAİZ GETİRİLİ AKTİFLER", "EARNING ASSETS", "TOPLAM AKTİFLER"],
        "candidates": []
    },
    "tier1_capital": {
        "keywords": ["ANA SERMAYE", "TIER 1", "ÖZKAYNAK"],
        "candidates": []
    },
    "risk_weighted_assets": {
        "keywords": ["RİSK AĞIRLIKLI", "RISK WEIGHTED"],
        "candidates": []
    },
    "operating_expenses": {
        "keywords": ["FAALİYET GİDERİ", "OPERATING EXPENSE"],
        "candidates": []
    },
    "total_operating_income": {
        "keywords": ["FAALİYET GELİRİ", "OPERATING INCOME", "NET FAALİYET"],
        "candidates": []
    }
}

# Find candidates
for semantic, info in suggestions.items():
    for code in common_codes:
        desc_tr, desc_en = all_codes[MAJOR_BANKS[0]][code]
        desc = (desc_tr or "") + " " + (desc_en or "")
        desc_upper = desc.upper()
        
        if any(kw in desc_upper for kw in info["keywords"]):
            suggestions[semantic]["candidates"].append((code, desc_tr))

print("\nFor net_interest_margin:")
for semantic in ["net_interest_income", "interest_earning_assets"]:
    candidates = suggestions[semantic]["candidates"]
    if candidates:
        print(f"\n  {semantic}:")
        for code, desc in candidates[:3]:
            print(f"    {code}: {desc[:60] if desc else 'N/A'}")
    else:
        print(f"\n  {semantic}: ⚠️  No candidates found")

print("\nFor capital_adequacy:")
for semantic in ["tier1_capital", "risk_weighted_assets"]:
    candidates = suggestions[semantic]["candidates"]
    if candidates:
        print(f"\n  {semantic}:")
        for code, desc in candidates[:3]:
            print(f"    {code}: {desc[:60] if desc else 'N/A'}")
    else:
        print(f"\n  {semantic}: ⚠️  No candidates found")

print("\nFor cost_income_ratio:")
for semantic in ["operating_expenses", "total_operating_income"]:
    candidates = suggestions[semantic]["candidates"]
    if candidates:
        print(f"\n  {semantic}:")
        for code, desc in candidates[:3]:
            print(f"    {code}: {desc[:60] if desc else 'N/A'}")
    else:
        print(f"\n  {semantic}: ⚠️  No candidates found")

db.close()

print(f"\n{'='*80}")
print("Next steps:")
print("1. Review suggested mappings above")
print("2. Add mappings to services/item_code_mapper.py")
print("3. Test with: python tests/audit_phase1/check_banking_fields.py")
print("="*80)
