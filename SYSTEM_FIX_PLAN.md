# System Stabilization Plan - Comp API

## Current State (2026-07-05)

### ✅ GOOD
- **Financial Statements**: 94.9% coverage (579/610 companies) - 332,838 records
- **Scores**: 93.6% coverage (571/610 companies)  
- **Ratios**: 69.5% coverage (424/610 companies)
- Data freshness: All updated today

### ❌ CRITICAL ISSUES
1. **Price Data**: Only 2.5% coverage (15/610 companies)
2. **P/E Ratios**: 0% coverage (0/610 companies)
3. **daily_prices source**: Only 26/610 companies (4.3%)

### ⚠️ WARNINGS
- 31 companies missing financial statements (mostly UFRS_K aracı kurumlar)
- 186 companies missing ratios
- 39 companies missing scores
- Price data 2 days old

---

## Fix Priority

### 🔴 PRIORITY 1: Price Data (CRITICAL)
**Problem**: Only 26/610 companies in `daily_prices` table (finveri source)

**Root Cause**: finveri only fetches a limited set of tickers (probably BIST30 or similar)

**Solution Options**:
1. **Option A**: Expand finveri to fetch ALL 610 tickers daily
2. **Option B**: Add İş Yatırım price API as secondary source
3. **Option C**: Use yfinance for Turkish stocks (.IS suffix)

**Recommended**: Option A + Option C (finveri primary, yfinance fallback)

**Actions**:
- [ ] Check finveri ticker list configuration
- [ ] Add all 610 active tickers to finveri fetch list
- [ ] Create daily price sync job
- [ ] Populate company_metrics from daily_prices (already have script)

---

### 🟡 PRIORITY 2: Missing Ratios (186 companies)
**Problem**: 186/610 companies have financial statements but no ratios

**Root Cause Analysis Needed**:
- Do they have financial statements but ratio calculation failed?
- Are they different financial groups with missing calculation logic?

**Actions**:
- [ ] List which 186 companies are missing ratios
- [ ] Check their financial_group distribution
- [ ] Run ratio calculation script for them
- [ ] Fix any financial_group-specific issues

---

### 🟡 PRIORITY 3: Missing Scores (39 companies)
**Problem**: 39/610 companies have no scores

**Actions**:
- [ ] Identify which 39 companies
- [ ] Check if they have ratios
- [ ] Run score calculation for them

---

### 🟢 PRIORITY 4: Missing Financial Statements (31 companies)
**Problem**: 31/610 companies (mostly UFRS_K brokers) have no financial data

**Analysis**: These are small brokers, may not report or use different formats

**Actions**:
- [ ] Check if they actually report (İş Yatırım API)
- [ ] If yes, fetch their data
- [ ] If no, mark as `is_active = FALSE` or add note

---

## Implementation Scripts

### Script 1: Expand Price Coverage
```bash
# File: expand_price_coverage.py
# 1. Get all active tickers from companies table
# 2. Add to finveri fetch configuration
# 3. Backfill daily_prices for last 30 days
# 4. Run populate_company_metrics.py
```

### Script 2: Calculate Missing Ratios
```bash
# File: calculate_missing_ratios.py
# 1. Find companies with statements but no ratios
# 2. Group by financial_group
# 3. Run ratio calculation for each group
# 4. Log any errors
```

### Script 3: Calculate Missing Scores
```bash
# File: calculate_missing_scores.py
# 1. Find companies with ratios but no scores
# 2. Run score calculation
# 3. Verify all have scores
```

### Script 4: Daily Maintenance Job
```bash
# File: daily_maintenance.py
# 1. Fetch latest prices from finveri
# 2. Update company_metrics
# 3. Recalculate ratios for new periods
# 4. Recalculate scores
# 5. Update sector benchmarks
# 6. Log summary
```

---

## Expected Timeline

- **Day 1** (Today): Fix price data (Priority 1)
  - Run audit ✅
  - Identify root cause ✅
  - Create fix scripts
  - Deploy price coverage fix

- **Day 2**: Fix missing ratios & scores (Priority 2-3)
  - Calculate missing ratios
  - Calculate missing scores
  - Verify coverage

- **Day 3**: Set up automation
  - Create daily maintenance job
  - Test end-to-end
  - Deploy to production

---

## Success Metrics

### Target Coverage (Within 3 days)
- Financial Statements: 95%+ (maintain)
- Ratios: 90%+ (up from 69.5%)
- Scores: 95%+ (maintain)
- **Prices: 90%+** (up from 2.5%) ← CRITICAL
- **P/E Ratios: 70%+** (up from 0%) ← CRITICAL

### Monitoring
- Daily health check script
- Alert if coverage drops below thresholds
- Weekly data quality report

---

## Next Immediate Actions

1. ✅ Run system_health_audit.py
2. Check finveri ticker configuration
3. Create expand_price_coverage.py
4. Test with 10 tickers first
5. Roll out to all 610 tickers

