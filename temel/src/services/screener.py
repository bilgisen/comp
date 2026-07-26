from typing import Optional
from db.client import D1Client


RATIO_ALIASES = {
    "pe": "pe", "fk": "pe", "f/k": "pe",
    "pb": "pb", "pddd": "pb", "pd/dd": "pb",
    "ev_ebitda": "ev_ebitda", "fdfavok": "ev_ebitda", "fd/favök": "ev_ebitda",
    "ev_sales": "ev_sales", "fdsatis": "ev_sales", "fd/satış": "ev_sales",
    "roe": "roe", "roa": "roa",
    "net_margin": "net_margin", "net_kar": "net_margin",
    "debt_equity": "debt_equity", "borc_ozkaynak": "debt_equity",
    "current_ratio": "current_ratio", "cari_oran": "current_ratio",
    "eps": "eps", "hbk": "eps",
    "profit_growth": "profit_growth", "kar_buyume": "profit_growth",
}

RATIO_FILTER_PREFIXES = [f"{code}_min" for code in RATIO_ALIASES] + [f"{code}_max" for code in RATIO_ALIASES]


class ScreenerService:
    def __init__(self, db: D1Client):
        self.db = db

    async def filter(self, params: dict) -> dict:
        sector = params.get("sector", "")
        group = params.get("group", "")
        q = params.get("q", "")
        score_min = self._float_or_none(params.get("score_min"))
        score_max = self._float_or_none(params.get("score_max"))
        sort_by = params.get("sort_by", "composite_score")
        sort_dir = params.get("sort_dir", "desc")

        where_clauses = ["c.is_active = 1"]
        where_params = []

        if sector:
            where_clauses.append("c.sector_main = ?")
            where_params.append(sector)
        if group:
            where_clauses.append("c.financial_group = ?")
            where_params.append(group)
        if q:
            where_clauses.append("(c.ticker LIKE ? OR c.name LIKE ?)")
            like = f"%{q.upper()}%"
            where_params.extend([like, like])

        where_sql = " AND ".join(where_clauses)

        companies = await self.db.query(
            f"SELECT ticker, name, sector_main, financial_group, market_cap FROM companies {where_sql} ORDER BY market_cap DESC",
            where_params
        )
        tickers = [r["ticker"] for r in companies.results]
        if not tickers:
            return {"total": 0, "results": []}

        scores_raw = await self.db.query(
            "SELECT ticker, composite_score, pillar_finansal_saglik, pillar_karlilik_buyume, pillar_degerleme, absolute_score "
            "FROM company_scores WHERE ticker IN (" + ",".join(["?"] * len(tickers)) + ") AND period_key = 'TTM' AND score_version = 'v1'",
            tickers
        )
        score_map = {r["ticker"]: r for r in scores_raw.results}

        ratios_raw = await self.db.query(
            "SELECT ticker, ratio_code, ratio_value FROM company_ratios "
            "WHERE ticker IN (" + ",".join(["?"] * len(tickers)) + ") AND period_key = 'TTM'",
            tickers
        )
        ratio_map: dict[str, dict[str, float | None]] = {}
        for r in ratios_raw.results:
            t = r["ticker"]
            if t not in ratio_map:
                ratio_map[t] = {}
            ratio_map[t][r["ratio_code"]] = r["ratio_value"]

        ratio_filters = []
        for key, val in params.items():
            prefix = "_min" if key.endswith("_min") else "_max" if key.endswith("_max") else None
            if prefix is None:
                continue
            code = key[:-len(prefix)]
            canonical = RATIO_ALIASES.get(code)
            if canonical and val:
                ratio_filters.append((canonical, prefix, self._float_or_none(val)))

        def passes_ratio_filters(ticker_ratios: dict) -> bool:
            for code, op, threshold in ratio_filters:
                v = ticker_ratios.get(code)
                if v is None:
                    return False
                if op == "_min" and v < threshold:
                    return False
                if op == "_max" and v > threshold:
                    return False
            return True

        results = []
        for c in companies.results:
            ticker = c["ticker"]
            sc = score_map.get(ticker, {})
            composite = sc.get("composite_score")

            if score_min is not None and (composite is None or composite < score_min):
                continue
            if score_max is not None and (composite is None or composite > score_max):
                continue

            ticker_ratios = ratio_map.get(ticker, {})

            if ratio_filters and not passes_ratio_filters(ticker_ratios):
                continue

            results.append({
                "ticker": ticker,
                "name": c.get("name"),
                "sector": c.get("sector_main"),
                "market_cap": c.get("market_cap"),
                "composite_score": composite,
                "pillar_finansal_saglik": sc.get("pillar_finansal_saglik"),
                "pillar_karlilik_buyume": sc.get("pillar_karlilik_buyume"),
                "pillar_degerleme": sc.get("pillar_degerleme"),
                "absolute_score": sc.get("absolute_score"),
                "ratios": ticker_ratios,
            })

        reverse = sort_dir.lower() != "asc"
        results.sort(key=lambda r: r.get(sort_by) if r.get(sort_by) is not None else 0, reverse=reverse)

        return {
            "total": len(results),
            "results": results,
        }

    @staticmethod
    def _float_or_none(val) -> Optional[float]:
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
