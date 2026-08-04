# Temel Analiz — Comprehensive Improvement Plan

## Phase 0: Investigation (BLOCKER for ranking viz)

### 0.1 Fix `sector_position` vs `peer_rank` inconsistency
- **Problem:** `sector_position` (from context-builder.js) and `peer_rank` (from swot-builder.js) both compute same thing: percentile rank within sector by `composite_score`. But they take different approaches (`(below+1)/n` vs `(1 - rank/n)`). Verify both produce same result.
- **Likely root cause:** SAYAS 14/15 = 6.7% vs 2/15 = 86.7% — one is rank (14th out of 15), the other is percentile. The frontend may be displaying `ranks.sector.percentile` from score-worker (`6.7%`) vs `peer_rank.percentile` from swot (`86.7%`). Score worker `_calc_rank` uses `(below + 0.5*equal)/n * 100` — if SAYAS has composite_score near bottom, this gives low percentile. SWOT `peer_rank` does `(1 - rank/n) * 100` where rank = idx+1 — same math, should match.
- **Action:** Add debug logging to both paths, run for SAYAS, compare raw values. Fix whichever is wrong.

### 0.2 Ticker casing normalization
- **Problem:** `SAYAS` vs `sayas` leads to cache misses. Already handled in Hono route params (`ticker.toUpperCase()`), but verify score-worker also normalizes.

## Phase 1: API Consolidation (Hono + Workers)

### 1.1 New unified endpoint: `GET /comp/fundamentals/{ticker}?scope=public|member|abone`
- Merges data from:
  - `/score/{ticker}` → composite_score, pillars, absolute, ranks
  - `/companies/{ticker}/profile` → company info
  - `/companies/{ticker}/ratios` → ratios with sector context
  - `/companies/{ticker}/trends` → trend data
  - AI context (native DB) → key_insights, risk_assessment, relational_signals
- **Response shape:**
  ```json
  {
    "ticker": "SAYAS",
    "company_name": "...",
    "sector": "...",
    "composite_score": 42.5,
    "pillars": { "finansal_saglik": {...}, "karlilik_buyume": {...}, "degerleme": {...} },
    "absolute": { "score": 35, "label": "ZAYIF" },
    "ranks": { "sector": { "percentile": 6.7, "n_peers": 15 } },
    "ratios": { /* RATIO_META entries with sector_context */ },
    "trends": { /* TREND_RATIOS with values, direction, momentum */ },
    "key_insights": [ /* top-5 sorted by importance */ ],
    "risk_assessment": { /* composite + indicators */ },
    "relational_signals": [ /* Phase 3 */ ],
    "sections": {
      "locked": { "ai_report": true, "ratio_values": false /* for public */ },
      "available": ["score", "pillars", "ranks", "overview"]
    }
  }
  ```
- **Scope gating:**
  - `public`: score visible, ratio values → blurred/0, no AI report, no relational signals
  - `member`: score + ratio values + trends visible + key_insights ("Öne Çıkanlar"). AI report locked.
  - `abone`: everything unlocked, including AI report and relational signals
- **Cache**: 1h TTL, keyed by `fundamentals:{ticker}:{scope}`

### 1.2 Deprecate old endpoints (keep for backward compat, remove from frontend hooks)
- Keep `/score/{ticker}`, `/companies/{ticker}/ratios`, `/companies/{ticker}/trends` etc. but the frontend should use only the new endpoint.

### 1.3 Remove `/ai/swot/{ticker}` endpoint
- SWOT frame is killed. `buildSWOTOnly` deleted.
- `key_insights` from insight-builder.js is recycled for member tier as "Öne Çıkanlar".

## Phase 2: Kill SWOT — Recycle as "Öne Çıkanlar"

### 2.1 Delete swot-builder.js
- `buildSWOT()` function removed
- Filter out template filler items: `"Sektör dinamikleri değerlendirilmeli"`, `"Piyasa koşullarına dikkat edilmeli"`, etc.

### 2.2 Upgrade insight-builder.js
- Rename to "Öne Çıkanlar" (featured insights)
- Sorted by importance, top-5
- Categories: `strength` (green), `weakness` (red), `positive_trend` (blue), `negative_trend` (orange), `data_quality` (gray)

### 2.3 Frontend: replace SWOT card grid with Öne Çıkanlar list
- Simple flat list with colored category badges, not a 2x2 grid
- Member tier: shows this
- Subscriber tier: also shows the AI report below

## Phase 3: Relational Classification Layer (Pre-LLM)

### 3.1 New module: `hono/src/lib/fa/relational-rules.js`
- No LLM involved — pure boolean logic
- Input: `ratios` object (all RATIO_META keys with values + sector_context)
- Output: `RelationalSignal[]`

### 3.2 Pattern library (10 rules minimum)
```js
// Pattern signature
{ pattern_id: "cheap_slow_growth",
  category: "confirming" | "conflicting" | "warning" | "opportunity",
  ratios_involved: ["pe", "profit_growth"],
  polarity: "confirming", // or "conflicting"
  narrative_hint: "Düşük F/K düşük büyüme ile tutarlı",
  severity: 1-5,
  ratio_details: { pe: { value, percentile }, profit_growth: { value, percentile } }
}
```

Rules to implement:
1. **cheap_slow_growth** (confirming): `pe < p25 && profit_growth < p25`
2. **expensive_fast_growth** (confirming): `pe > p75 && profit_growth > p75`
3. **value_trap** (warning): `pe < p25 && (roe < p25 || net_margin < p25)`
4. **high_roe_low_growth** (conflicting): `roe > p75 && profit_growth < p25`
5. **overvalued_weak_profits** (warning): `pe > p75 && roe < p25`
6. **strong_liquidity_high_debt** (conflicting): `current_ratio > p75 && debt_equity > p75`
7. **low_margin_high_turnover** (confirming): `net_margin < p25 && asset_turnover > p75`
8. **candidate_distress** (warning): `current_ratio < p25 && debt_equity > p75 && interest_coverage < p25`
9. **quality_at_reasonable_price** (opportunity): `roe > p75 && pe < p50 && debt_equity < p50`
10. **momentum_acceleration** (opportunity): `net_margin direction=rising && roe direction=rising && profit_growth > p50`
11. **margin_erosion** (warning): `gross_margin direction=falling && net_margin direction=falling`
12. **balance_sheet_strengthening** (opportunity): `debt_equity direction=falling && current_ratio direction=rising`

### 3.3 Integration
- `relational-rules.js` called from context-builder.js after ratios are built
- `RelationalSignal[]` added to context → fundamental report → subscriber report
- Signals rendered as expandable accordion cards in the AI report

## Phase 4: Subscriber AI Report — 5-Section Narrative

### 4.1 New endpoint: `POST /api/v2/ai-report/{ticker}`
- Already exists as `reportRoute` in main.js (section-level v2)
- Extend to include:
  - `relational_signals` as structured input
  - Per-section ratio references

### 4.2 Report structure (5 sections)
```json
"sections": [
  { "id": "sentez", "title": "Genel Değerlendirme",
    "content": "SAYAS ... [inline_ratio:pe] ... [inline_ratio:roe] ...",
    "signals_used": ["value_trap", "candidate_distress"],
    "visual_hint": "score_gauge" },
  { "id": "degerleme", "title": "Değerleme Analizi",
    "content": "...",
    "ratios_referenced": ["pe", "pb", "ev_ebitda"],
    "visual_hint": "comparison_table" },
  { "id": "karlilik", "title": "Kârlılık Kalitesi",
    "content": "...",
    "ratios_referenced": ["roe", "net_margin", "gross_margin"],
    "visual_hint": "trend_chart" },
  { "id": "saglamlik", "title": "Finansal Sağlamlık",
    "content": "...",
    "ratios_referenced": ["current_ratio", "debt_equity", "interest_coverage"],
    "visual_hint": "gauge" },
  { "id": "izlenecekler", "title": "İzlenmesi Gerekenler",
    "content": "...",
    "signals_used": ["momentum_acceleration", "margin_erosion"],
    "visual_hint": "checklist" }
]
```

### 4.3 Inline ratio badges
- In content paragraphs: `[inline_ratio:pe]` → rendered as `<sup><a href="#" class="ratio-badge" data-ratio="pe">F/K: 5.2x</a></sup>`
- Hover/click shows tooltip with sector percentile

### 4.4 Chatbot bridge
- Footer of report: "Bu analiz hakkında sorularınız mı var? [AI Asistanına Sor]"
- Pre-fills chatbot context with `{ ticker, report_id, section_id }`

## Phase 5: Frontend Redesign

### 5.1 New single hook: `useCompFundamentals(ticker, scope)`
- Calls `GET /api/v1/comp/fundamentals/{ticker}?scope=abone`
- Replaces: `useCompScore`, `useCompProfile`, `useCompRatios`, `useCompTrends`, `useCompAnalysis`, `useCompSwot`, `useCompFundamentalReport`
- Returns typed `FundamentalsResponse`

### 5.2 Layout sections (top→bottom):

**A. Score Radar (replaces old score + pillar bar chart)**
- RadialBarChart (recharts) showing composite score as arc
- 3 small radial gauges for pillar scores
- Sector percentile badge
- Absolute score with label

**B. Ratio at a Glance (replaces old bar chart)**
- Grid of ratio cards, each showing:
  - Ratio name + value
  - Inline bar comparing to sector median (0-100% fill)
  - Color: green if outperforming sector median, red if under

**C. Öne Çıkanlar (member+)**
- Flat list of insight items with colored category badges
- Links to relevant section of AI report (subscriber) or upgrade CTA (member)

**D. Risk Radar (subscriber)**
- Risk gauge (recharts PieChart with gauge-like arc)
- Risk indicators table (liquidity, leverage, profitability, valuation)
- Risk trend signals

**E. AI Raporu (subscriber only)**
- 5-section accordion/expandable cards
- Each section: title + content paragraph + inline ratio badges
- Bottom: chatbot "Sor" button
- Non-subscriber: blurred preview + "Abone Ol" CTA

**F. Trend Placeholder**
- If trends have ≥4 periods: LineChart (same as current)
- If <4 periods: "Trend verisi yetersiz — en az 4 dönem gerekiyor" message
- Show available data as simple table instead

### 5.3 Content Gating in Frontend
- `scope` parameter controls what API returns
- No client-side hiding of ratio values — server returns blurred/zeroed data for public
- CSS blur effect (`blur-sm`) for locked sections with overlay CTA

## Phase 6: Chart Recommendations

| Section | Chart Type | Library | Notes |
|---------|-----------|---------|-------|
| Composite Score | RadialBarChart (single arc) | recharts | 0-100 arc, color gradient |
| Pillar Scores | 3x RadialBarChart (small) | recharts | Green/blue/amber |
| Ratio vs Sector | Inline horizontal bar | Pure CSS | Each ratio row, 0-100% fill |
| Risk | Semi-circle gauge | recharts PieChart | 180° arc, red-yellow-green |
| Trend (≥4 periods) | LineChart | recharts | Same as current, multi-series |
| Trend (<4 periods) | Data table | HTML table | Period columns, ratio rows |

## Implementation Order

```
Phase 0 ──→ Verify & fix ranking inconsistency (1-2h)
    │
    ▼
Phase 1 ──→ Build unified fundamentals endpoint (4-6h)
    │
    ▼
Phase 3 ──→ Relational rules engine (2-3h) — can build in parallel with Phase 1
    │
    ▼
Phase 2 ──→ Kill SWOT, upgrade insights (1-2h)
    │
    ▼
Phase 4 ──→ AI report 5-section narrative (4-6h)
    │
    ▼
Phase 5 ──→ Frontend redesign (6-8h)
    │
    ▼
Phase 6 ──→ Polish charts, responsive (2-3h)
```

## Files to Create/Modify

### New files:
- `hono/src/lib/fa/relational-rules.js` — rule engine
- `tanstack/src/components/company/ScoreRadar.tsx` — radial gauge + pillar gauges
- `tanstack/src/components/company/RatioGrid.tsx` — ratio cards with inline bars
- `tanstack/src/components/company/AiReport.tsx` — 5-section subscriber report
- `tanstack/src/components/company/RiskRadar.tsx` — risk gauge section
- `tanstack/src/components/company/OneCikanlar.tsx` — featured insights list

### Modified files:
- `hono/src/routes/comp.js` — add `/fundamentals/{ticker}` endpoint
- `hono/src/lib/fa/context-builder.js` — add relational signals, remove SWOT, upgrade insights
- `hono/src/lib/fa/insight-builder.js` — add categories, remove duplicates
- `hono/src/lib/fa/swot-builder.js` — DELETE
- `tanstack/src/lib/useCompData.ts` — add `useCompFundamentals` hook, deprecate old hooks
- `tanstack/src/routes/hisse.$ticker.temel-analiz.tsx` — full rewrite
- `tanstack/src/components/company/FaReport.tsx` — replace with AiReport.tsx

### Deleted files:
- `hono/src/lib/fa/swot-builder.js`

## Verification

After each phase:
1. `wrangler dev` for Hono — confirm endpoint returns expected shape
2. Check frontend renders without errors for public/member/abone
3. Verify no regression on `/sektorler`, `/hisse/$ticker` pages
4. Test with SAYAS, AKBNK, THYAO (different sectors, score ranges)
