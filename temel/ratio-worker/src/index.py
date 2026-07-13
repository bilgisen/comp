import json
from datetime import datetime, timezone
from workers import WorkerEntrypoint, Response


def safe_div(a, b):
    if b is None or a is None:
        return None
    try:
        return a / b if b != 0 else None
    except (ZeroDivisionError, TypeError):
        return None


SECTOR_RATIOS = {
    "industrial": ["pe","pb","ev_ebitda","ev_sales","roe","roa","net_margin","gross_margin","eps","book_per_share","profit_growth","current_ratio","cash_ratio","debt_equity","inventory_turnover","interest_coverage","forward_pe","forward_ev_ebitda","forward_pb"],
    "financial": ["pe","pb","roe","roa","net_margin","eps","book_per_share","profit_growth","forward_pe","forward_pb"],
    "holding": ["pe","pb","ev_ebitda","ev_sales","roe","roa","net_margin","eps","book_per_share","profit_growth","debt_equity","forward_pe","forward_ev_ebitda","forward_pb"],
    "reit": ["pe","pb","roe","net_margin","eps","book_per_share","profit_growth","forward_pe","forward_pb"],
    "insurance": ["pe","pb","roe","roa","net_margin","eps","book_per_share","profit_growth","forward_pe","forward_pb"],
    "brokerage": ["pe","pb","roe","roa","net_margin","eps","book_per_share","profit_growth"],
    "banking": ["pe","pb","roe","roa","net_margin","eps","book_per_share","profit_growth","forward_pe","forward_pb"],
}


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        try:
            db = self.env.TEMEL_DB
            cache = self.env.TEMEL_CACHE
            url = request.url
            if "/compute" in url and request.method.upper() in ("POST", "GET"):
                return await self.compute_ratios(db, cache, url)
            if "/validate" in url:
                return await self.validate_ratios(db)
            if "/ticker/" in url:
                ticker = url.split("/ticker/")[-1].split("?")[0].split("/")[0].upper().strip()
                return await self.get_ticker_ratios(db, ticker)
            return Response.json({
                "endpoints": {
                    "POST/GET /compute": "Run ratio computation for 15 companies (cursor-based)",
                    "POST/GET /validate": "Compare computed vs isyatirim_ratios reference",
                    "GET /ticker/{TICKER}": "Get all data for a ticker",
                }
            })
        except Exception as e:
            return Response.json({"error": str(e), "type": type(e).__name__}, status=500)

    async def scheduled(self, event):
        db = self.env.TEMEL_DB
        cache = self.env.TEMEL_CACHE
        await cache.delete("ratio:cursor")
        while True:
            r = await self.compute_ratios(db, cache, "http://cron/compute")
            body = json.loads(await r.text())
            if body.get("cursor", 0) == 0:
                break

    async def get_ticker_ratios(self, db, ticker):
        d1 = await db.prepare("SELECT ratio_code, ratio_value, is_ttm, computed_at FROM company_ratios WHERE ticker = ? ORDER BY ratio_code").bind(ticker).all()
        d1p = await db.prepare("SELECT * FROM company_sector_profiles WHERE ticker = ?").bind(ticker).all()
        d1m = await db.prepare("SELECT * FROM company_metrics WHERE ticker = ?").bind(ticker).all()
        d1s = await db.prepare("SELECT * FROM company_financial_summary WHERE ticker = ? ORDER BY period_key DESC").bind(ticker).all()
        d1r = await db.prepare("SELECT * FROM isyatirim_ratios WHERE ticker = ?").bind(ticker).all()
        return Response.json({
            "ticker": ticker,
            "profile": dict(d1p.results[0]) if d1p.results else {},
            "metrics": dict(d1m.results[0]) if d1m.results else {},
            "summary": [dict(r) for r in d1s.results],
            "reference": dict(d1r.results[0]) if d1r.results else {},
            "computed": [dict(r) for r in d1.results],
        })

    async def validate_ratios(self, db):
        d1 = await db.prepare("""
            SELECT cr.ticker, cr.ratio_code, cr.ratio_value,
                   ir.pe_ratio, ir.pb_ratio, ir.ev_ebitda, ir.ev_sales
            FROM company_ratios cr
            LEFT JOIN isyatirim_ratios ir ON cr.ticker = ir.ticker
            ORDER BY cr.ticker
        """).all()
        rows = [dict(r) for r in d1.results]
        ref_map = {"pe": "pe_ratio", "pb": "pb_ratio", "ev_ebitda": "ev_ebitda", "ev_sales": "ev_sales"}
        deviations = []
        for row in rows:
            ref_key = ref_map.get(row.get("ratio_code", ""))
            ref_val = row.get(ref_key) if ref_key else None
            comp_val = row.get("ratio_value")
            if comp_val and ref_val and ref_val > 0:
                dev = (comp_val - ref_val) / ref_val * 100
                deviations.append({"ticker": row["ticker"], "ratio": row["ratio_code"], "computed": round(comp_val, 2), "reference": ref_val, "deviation_pct": round(dev, 1)})
        flagged = [d for d in deviations if abs(d["deviation_pct"]) > 20]
        return Response.json({"total_validated": len(deviations), "flagged": len(flagged), "deviations": deviations[:100], "flagged_rows": flagged[:50]})

    async def compute_ratios(self, db, cache, url):
        ticker_filter = None
        if "ticker=" in url:
            ticker_filter = url.split("ticker=")[-1].split("&")[0].upper().strip()

        d1p = await db.prepare("SELECT * FROM company_sector_profiles").all()
        profiles = {dict(r)["ticker"]: dict(r) for r in d1p.results}

        all_tickers = sorted(profiles.keys())
        if ticker_filter and ticker_filter in all_tickers:
            all_tickers = [ticker_filter]

        cursor_val = await cache.get("ratio:cursor")
        start = int(cursor_val) if cursor_val is not None else 0
        if start >= len(all_tickers):
            start = 0

        d1m = await db.prepare("SELECT * FROM company_metrics").all()
        metrics_map = {dict(r)["ticker"]: dict(r) for r in d1m.results}

        d1r = await db.prepare("SELECT * FROM isyatirim_ratios").all()
        ref_map = {dict(r)["ticker"]: dict(r) for r in d1r.results}

        d1s = await db.prepare("SELECT * FROM company_financial_summary ORDER BY ticker, period_key DESC").all()
        summaries = {}
        for r in d1s.results:
            row = dict(r)
            t = row["ticker"]
            if t not in summaries:
                summaries[t] = row

        d1r2 = await db.prepare("""
            SELECT ticker, period_key, item_code, value_try
            FROM financial_statements_raw
            WHERE item_code IN ('3Z','2O','3C','3CA','3DF','1BL','1AI','2A','1AA','1AF','1AC','2AA','2BA','3D','3HC')
            ORDER BY ticker, period_key DESC
        """).all()
        data_map = {}
        for r in d1r2.results:
            row = dict(r)
            t = row["ticker"]
            code = row.get("item_code", "")
            val = row.get("value_try")
            if val is not None:
                key = (t, code)
                if key not in data_map:
                    data_map[key] = []
                data_map[key].append(val)

        def ttm_sum(ticker, code):
            vals = data_map.get((ticker, code), [])
            if vals:
                return sum(vals[:4])
            return None

        def latest(ticker, code):
            vals = data_map.get((ticker, code), [])
            return vals[0] if vals else None

        now_iso = datetime.now(timezone.utc).isoformat()
        batch_size = 15
        end = min(start + batch_size, len(all_tickers))
        batch = all_tickers[start:end]
        results = []
        computed_count = 0

        for ticker in batch:
            try:
                profile = profiles.get(ticker, {})
                metrics = metrics_map.get(ticker, {})
                ref = ref_map.get(ticker, {})

                ni_ttm = ttm_sum(ticker, "3Z")
                if ni_ttm is None:
                    ni_ttm = summaries.get(ticker, {}).get("net_income")
                equity = latest(ticker, "2O")
                if equity is None:
                    equity = summaries.get(ticker, {}).get("equity")

                revenue = ttm_sum(ticker, "3C")
                cogs = ttm_sum(ticker, "3CA")
                ebit = ttm_sum(ticker, "3DF")
                gross_profit = ttm_sum(ticker, "3D")
                total_assets = latest(ticker, "1BL")
                current_assets = latest(ticker, "1AI")
                current_liabilities = latest(ticker, "2A")
                cash = latest(ticker, "1AA")
                inventory = latest(ticker, "1AF")
                receivables_st = latest(ticker, "1AC")
                debt_st = latest(ticker, "2AA")
                debt_lt = latest(ticker, "2BA")
                interest_exp = ttm_sum(ticker, "3HC")

                prev_vals = data_map.get((ticker, "3Z"), [])
                prev_ni = sum(prev_vals[1:5]) if len(prev_vals) > 1 else None

                total_debt = (debt_st or 0) + (debt_lt or 0) if (debt_st is not None or debt_lt is not None) else None
                total_debt = total_debt if (total_debt is not None and total_debt > 0) else None

                sg = profile.get("sector_group", "industrial")
                ratio_list = SECTOR_RATIOS.get(sg, SECTOR_RATIOS["industrial"])
                price = metrics.get("last_price")
                shares = metrics.get("shares_outstanding")

                eps = safe_div(ni_ttm, shares)
                bps = safe_div(equity, shares)

                vals = {
                    "eps": eps, "book_per_share": bps,
                    "pe": safe_div(price, eps),
                    "pb": safe_div(price, bps),
                    "roe": safe_div(ni_ttm, equity),
                    "profit_growth": safe_div(ni_ttm - prev_ni, abs(prev_ni)) if prev_ni and ni_ttm is not None else None,
                    "ev_ebitda": ref.get("ev_ebitda"),
                    "ev_sales": ref.get("ev_sales"),
                    "forward_pe": ref.get("forward_pe"),
                    "forward_ev_ebitda": ref.get("forward_ev_ebitda"),
                    "forward_pb": ref.get("forward_pb"),
                    "roa": safe_div(ni_ttm, total_assets),
                    "net_margin": safe_div(ni_ttm, revenue),
                    "gross_margin": safe_div(gross_profit, revenue),
                    "current_ratio": safe_div(current_assets, current_liabilities),
                    "cash_ratio": safe_div(cash, current_liabilities),
                    "debt_equity": safe_div(total_debt, equity),
                    "inventory_turnover": safe_div(abs(cogs) if cogs else None, inventory),
                    "interest_coverage": safe_div(ebit, abs(interest_exp) if interest_exp else None),
                }

                ref_pe = ref.get("pe_ratio")
                ref_pb = ref.get("pb_ratio")
                if vals["pe"] is None and ref_pe:
                    vals["pe"] = ref_pe
                if vals["pb"] is None and ref_pb:
                    vals["pb"] = ref_pb

                ratio_count = 0
                for code in ratio_list:
                    v = vals.get(code)
                    if v is not None:
                        await db.prepare("""
                            INSERT OR REPLACE INTO company_ratios
                            (ticker, period_key, ratio_code, ratio_value, is_ttm, calculation_method, data_quality_score, computed_at)
                            VALUES (?, 'TTM', ?, ?, 1, 'v2', 0.8, ?)
                        """).bind(ticker, code, v, now_iso).run()
                        ratio_count += 1

                computed_count += 1
                results.append({"ticker": ticker, "ratios": ratio_count})
            except Exception as e:
                results.append({"ticker": ticker, "error": str(e)[:100]})

        next_cursor = end
        if next_cursor >= len(all_tickers):
            await cache.delete("ratio:cursor")
        else:
            await cache.put("ratio:cursor", str(next_cursor))

        return Response.json({
            "computed": computed_count,
            "total": len(all_tickers),
            "cursor": next_cursor if next_cursor < len(all_tickers) else 0,
            "results": results,
        })
