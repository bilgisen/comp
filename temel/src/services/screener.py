from typing import Optional
import re
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

    @staticmethod
    def _normalize(value: str) -> str:
        return (value or "").lower().replace("ı", "i").replace("ş", "s").replace("ğ", "g").replace("ü", "u").replace("ö", "o").replace("ç", "c")

    @staticmethod
    def _chunk_ids(ids: list, size: int = 90):
        for i in range(0, len(ids), size):
            yield ids[i:i + size]

    async def _query_in(self, sql_prefix: str, sql_suffix: str, ids: list, extra_params: Optional[list] = None) -> list:
        """Run an IN(...) query in chunks to stay under D1's 100 bound-parameter limit."""
        rows = []
        extra = extra_params or []
        for chunk in self._chunk_ids(ids):
            placeholders = ",".join(["?"] * len(chunk))
            r = await self.db.query(sql_prefix + placeholders + sql_suffix, list(chunk) + extra)
            rows.extend(r.results)
        return rows

    async def filter(self, params: dict) -> dict:
        sector = params.get("sector", "")
        group = params.get("group", "")
        q = params.get("q", "")
        score_min = self._float_or_none(params.get("score_min"))
        score_max = self._float_or_none(params.get("score_max"))
        sort_by = params.get("sort_by", "composite_score")
        sort_dir = params.get("sort_dir", "desc")
        if sort_by in RATIO_ALIASES:
            sort_by = RATIO_ALIASES[sort_by]
        elif sort_by.endswith("_min") or sort_by.endswith("_max"):
            base = sort_by[:-4]
            if base in RATIO_ALIASES:
                sort_by = RATIO_ALIASES[base]

        where_clauses = ["is_active = 1"]
        where_params = []

        if sector:
            s = sector.strip()
            cons = s.replace("&", "ve").replace(" ", "_")
            clauses = [
                "sector_main = ?",
                "sector_main IN (SELECT sector_raw FROM sector_consolidation WHERE sector_consolidated IN (?, ?) OR sector_raw IN (?, ?))",
            ]
            where_params.extend([s, s, cons, s, cons])
            norm = self._normalize(s)
            clauses.append(
                "LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(sector_main,'ı','i'),'ş','s'),'ğ','g'),'ü','u'),'ö','o')) = ?"
            )
            where_params.append(norm)
            words = [w for w in re.split(r"[&\s]+", s) if len(w) >= 3]
            if len(words) >= 2:
                like_conditions = " AND ".join(["sector_consolidated LIKE ?"] * len(words))
                clauses.append(f"sector_main IN (SELECT sector_raw FROM sector_consolidation WHERE {like_conditions})")
                where_params.extend([f"%{w}%" for w in words])
            where_clauses.append("(" + " OR ".join(clauses) + ")")
        if group:
            where_clauses.append("financial_group = ?")
            where_params.append(group)
        if q:
            where_clauses.append("(ticker LIKE ? OR name LIKE ?)")
            like = f"%{q.upper()}%"
            where_params.extend([like, like])

        where_sql = " AND ".join(where_clauses)

        companies = await self.db.query(
            f"SELECT ticker, name, sector_main, financial_group, market_cap FROM companies WHERE {where_sql} ORDER BY market_cap DESC",
            where_params
        )
        tickers = [r["ticker"] for r in companies.results]
        if not tickers:
            return {"total": 0, "results": []}

        scores_raw = await self._query_in(
            "SELECT id, ticker, composite_score, pillar_finansal_saglik, pillar_karlilik_buyume, pillar_degerleme, absolute_score "
            "FROM company_scores WHERE ticker IN (",
            ") AND period_key = 'TTM' AND score_version = 'v1'",
            tickers
        )
        score_map = {r["ticker"]: r for r in scores_raw}

        score_ids = [r["id"] for r in scores_raw if r.get("id")]
        ticker_by_score_id = {r["id"]: r["ticker"] for r in scores_raw if r.get("id")}
        details_map: dict[str, dict[str, dict]] = {}
        if score_ids:
            details_raw = await self._query_in(
                "SELECT score_id, ratio_code, ratio_value, peer_median, percentile, higher_is_better "
                "FROM company_score_details WHERE score_id IN (",
                ")",
                score_ids
            )
            for d in details_raw:
                ticker = ticker_by_score_id.get(d["score_id"])
                if not ticker:
                    continue
                details_map.setdefault(ticker, {})[d["ratio_code"]] = {
                    "value": d.get("ratio_value"),
                    "peer_median": d.get("peer_median"),
                    "percentile": d.get("percentile"),
                    "higher_is_better": d.get("higher_is_better"),
                }

        ratios_raw = await self._query_in(
            "SELECT ticker, ratio_code, ratio_value FROM company_ratios WHERE ticker IN (",
            ") AND period_key = 'TTM'",
            tickers
        )
        ratio_map: dict[str, dict[str, float | None]] = {}
        for r in ratios_raw:
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
            ticker_details = details_map.get(ticker, {})

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
                "percentiles": {code: d["percentile"] for code, d in ticker_details.items() if d.get("percentile") is not None},
                "peer_medians": {code: d["peer_median"] for code, d in ticker_details.items() if d.get("peer_median") is not None},
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
