# Insurance Sector Score Fix Summary

## Problem

Insurance companies ANSGR and ANHYT had ratios in the database but scores were showing as 0.00 or NULL.

## Root Cause

The `calculate_all_ufrs_k_scores.py` script was using **wrong item codes** for calculating net income for insurance companies:

- **Wrong**: Used `3ZA` or `3Z` for net income
- **Correct**: Should use `3NJD` (Dönem Net Kar veya Zararı) for insurance companies

Insurance companies use **different financial statement structure** than banks:
- Banks/Other UFRS_K: Net income is in `3ZA` or `3Z`
- Insurance companies: Net income is in `3NJD`

## Solution

Created `fix_insurance_ratios.py` script that:
1. Correctly reads net income from `3NJD` for insurance companies
2. Recalculates ROE and ROA ratios for all periods
3. Updates scores based on corrected ratios

## Results

### Before Fix
- ANSGR: ROE=0, ROA=0, Score=0.00
- ANHYT: ROE=0, ROA=0, Score=0.00

### After Fix
- **ANSGR** (Anadolu Sigorta):
  - ROE: 9.82%, ROA: 2.45%
  - **Score: 46.59**

- **ANHYT** (Anadolu Hayat Emeklilik):
  - ROE: 14.22%, ROA: 0.34%
  - **Score: 45.06**

### Final Insurance Sector Status (6 companies total)

✅ **4 companies with scores:**
1. AGESA (Agesa Hayat ve Emeklilik): 100.0
2. TURSG (Türkiye Sigorta): 60.19
3. ANSGR (Anadolu Sigorta): 46.59 ← Fixed
4. ANHYT (Anadolu Hayat Emeklilik): 45.06 ← Fixed

❌ **2 companies without scores (no financial data):**
5. AKGRT (Aksigorta): No UFRS_K financial statements in database
6. RAYSG (Ray Sigorta): No UFRS_K financial statements in database

## API Verification

✅ Tested: `https://comp-ef958063.fastapicloud.dev/api/v1/sectors/industries/sigortacilik`
✅ All 4 scored companies showing correctly in API response
✅ Page live at: https://jetborsa.com/sektorler/sigortacilik

## Files Created

1. `fix_insurance_ratios.py` - Corrects ratios and scores for insurance companies
2. `check_insurance_status.py` - Checks ratio and score status
3. `check_insurance_financial_items.py` - Inspects financial statement structure
4. `debug_insurance_data.py` - Debugging tool for detailed analysis
5. `calculate_missing_insurance_scores.py` - Finds companies with ratios but no scores

## Next Steps (If Needed)

For AKGRT and RAYSG:
1. Check if they report under UFRS_K financial group
2. If yes, fetch their financial statements from İş Yatırım API
3. Run `fix_insurance_ratios.py` to calculate scores

## Date
2026-01-07
