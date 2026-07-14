# System Stabilization Plan - Comprehensive Fix

**Date**: 2026-07-05
**Status**: IN PROGRESS
**Priority**: CRITICAL

---

## Current System State

### Coverage Analysis
- ✅ **Financial Statements**: 579/610 (94.9%) - GOOD
- ⚠️ **Ratios**: 441/610 (72.3%) - NEEDS IMPROVEMENT
  - Missing: 139 companies (mostly XI_29 financial group)
  - Missing: THYAO and other critical companies
- ✅ **Scores**: 571/610 (93.6%) - GOOD  
- ❌ **Prices**: 15/610 (2.5%) - CRITICAL ISSUE
- ❌ **P/E Ratios**: 0/610 (0.0%) - CRITICAL ISSUE
- ❌ **EPS**: 0/610 (0.0%) - MISSING ENTIRELY

### Health Score: 65.8% ❌ URGENT FIXES NEEDED

---

## Root Cause Analysis

### Issue 1: EPS Not Calculated
**Problem**: EPS (Earnings Per Share) ratio is NOT defined in `RatioCalculator`
**Impact**: 
- P/E ratios cannot be calculated (0% coverage)
- API returns empty F/K values for ALL companies
- Valuation metrics completely missing

**Root Cause**: `services/ratio_calculator.py` does not have EPS ratio definition
**Solution**: Add EPS calculation to ratio definitions

### Issue 2: Price Data Coverage (2.5%)
**Problem**: Only 26 tickers in `daily_prices` table (mostly indices/forex)
**Impact**: 
- Only 15 companies have price data
- Market cap calculations missing
- P/E, P/B, EV/EBITDA ratios cannot be calculated for 595/610 companies

**Root Causes**:
1. finveri's `tickers.json` only had 19 hardcoded tickers
2. finveri not restarted after tickers.json update
3. No automated price fetching from external APIs

**Solutions** (in order of preference):
1. ✅ Updated `finveri/data/tickers.json` with all 614 tickers
2. ⏳ Restart finveri to load new ticker list
3. ⏳ Run historical price sync in finveri
4. ⏳ Alternative: Direct fetch from İş Yatırım API (currently failing - needs fix)

### Issue 3: Missing Ratios for 139 Companies
**Problem**: Companies have financial statements but no ratios
**Breakdown**:
- XI_29 financial group: 139 companies
- UFRS_K financial group: 1 company (THYAO)

**Root Cause**: Ratio calculation not run for these companies
**Solution**: Bulk calculate ratios for all companies with financial statements

---

## Implementation Plan

### Phase 1: Add EPS Calculation ⏳
**File**: `services/ratio_calculator.py`
**Action**: Add EPS ratio to DEFAULT_RATIOS

```python
"eps": RatioConfig(
    code="eps",
    formula=lambda d: d.get("net_income_ttm") / d.get("shares_outstanding") 
        if d.get("net_income_ttm") is not None 
        and d.get("shares_outstanding") is not None 
        and d.get("shares_outstanding") != 0 
        else None,
    type="ttm",
    description="Pay Başına Kazanç = Net Kâr (TTM) / Hisse Senedi Sayısı",
    category="valuation"
),
```

**Issue**: Need to verify if `shares_outstanding` data exists in financial_statements_raw
**Fallback**: Calculate from market_cap / price if shares_outstanding missing

### Phase 2: Fix Price Data Coverage ⏳
**Target**: 90%+ price coverage (550+ companies)

**Option A: finveri (Preferred)**
1. Restart finveri process (loads new tickers.json with 614 tickers)
2. Trigger historical sync: `POST /admin/sync-all-history`
3. Wait for sync completion (~30-60 min for 610 tickers)
4. Run `populate_company_metrics.py` to sync to company_metrics

**Option B: Direct API Fetch (Backup)**
1. Fix `fetch_prices_from_isyatirim.py` (currently fails)
2. Test with single ticker to understand response format
3. Update parsing logic
4. Batch fetch all 610 tickers

**Option C: yfinance (Alternative)**
1. Install: `pip install yfinance`
2. Use existing `fetch_latest_prices_fast.py`
3. Fetch with `.IS` suffix for BIST tickers

### Phase 3: Calculate Missing Ratios ⏳
**Target**: 95%+ ratio coverage (580+ companies)

**Actions**:
1. Run ratio calculation for XI_29 companies (139 missing)
2. Run ratio calculation for THYAO (UFRS_K, single outlier)
3. Verify EPS is now calculated for all companies with statements

**Script**: Create `calculate_missing_ratios_bulk.py`

### Phase 4: Sync and Verify ⏳
1. Run `populate_company_metrics.py` to sync prices
2. Calculate P/E ratios (now possible with EPS + prices)
3. Run `stabilize_system.py` to verify
4. Target health score: 95%+

---

## Action Items (Prioritized)

### Immediate (Now)
1. ✅ Add unique constraint to company_metrics.ticker
2. ⏳ Check if shares_outstanding data exists in financial_statements_raw
3. ⏳ Add EPS ratio definition to ratio_calculator.py
4. ⏳ Create bulk ratio calculation script

### Short Term (Next Hour)
5. ⏳ Restart finveri with new tickers.json
6. ⏳ Run finveri historical sync OR fix İş Yatırım fetch
7. ⏳ Bulk calculate missing ratios (139 companies)
8. ⏳ Populate company_metrics with prices

### Verification (After Fixes)
9. ⏳ Run stabilize_system.py - expect 95%+ health score
10. ⏳ Test API endpoint - verify F/K appears for holdings
11. ⏳ Spot check: https://jetborsa.com/sektorler/holdingler

---

## Expected Results

### Before
- Financial Statements: 94.9%
- Ratios: 72.3%
- Scores: 93.6%
- Prices: 2.5% ❌
- P/E: 0.0% ❌
- EPS: 0.0% ❌
- Health: 65.8% ❌

### After (Target)
- Financial Statements: 95%+ ✅
- Ratios: 95%+ ✅
- Scores: 95%+ ✅
- Prices: 90%+ ✅
- P/E: 85%+ ✅
- EPS: 90%+ ✅
- Health: 95%+ ✅

---

## Risk Mitigation

1. **EPS Calculation Risk**: If shares_outstanding missing, use market_cap/price as fallback
2. **Price Fetch Risk**: If finveri sync fails, use direct API or yfinance
3. **Ratio Calculation Risk**: If bulk fails, process in smaller batches by financial_group
4. **Performance Risk**: Price sync for 610 tickers may take 30-60 minutes

---

## Next Steps

User needs to:
1. Decide on price data approach (finveri restart vs direct fetch)
2. Confirm if we should add EPS now or wait for price data first
3. Set expectations on timeline (immediate fix vs gradual rollout)

Agent will:
1. Implement EPS ratio definition
2. Create bulk ratio calculation script
3. Fix and run chosen price data approach
4. Verify system health reaches 95%+
