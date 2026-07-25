from typing import Optional, List
from db.client import D1Client

KEY_RATIOS = ["pe", "pb", "roe", "net_margin", "current_ratio", "debt_equity", "ev_ebitda", "roa"]

RATIO_NAMES_COMPARE = {
    "pe": "F/K", "pb": "PD/DD", "roe": "ROE", "net_margin": "Net Kâr Marjı",
    "current_ratio": "Cari Oran", "debt_equity": "Borç/Özkaynak",
    "ev_ebitda": "FD/FAVÖK", "roa": "ROA",
}

RATIO_CATEGORIES_COMPARE = {
    "pe": "degerleme", "pb": "degerleme", "ev_ebitda": "degerleme",
    "roe": "karlilik", "net_margin": "karlilik", "roa": "karlilik",
    "current_ratio": "finansal", "debt_equity": "finansal",
}

HIGHER_IS_BETTER = {
    "pe": False, "pb": False, "ev_ebitda": False,
    "roe": True, "net_margin": True, "roa": True,
    "current_ratio": True, "debt_equity": False,
}


class CompareBuilder:
    def __init__(self, db: D1Client):
        self.db = db

    async def build(self, tickers: List[str], period_key: str = "TTM") -> dict:
        tickers = [t.upper().strip() for t in tickers if t.strip()]
        if len(tickers) < 2:
            return {"error": "At least 2 tickers required"}, 400
        if len(tickers) > 5:
            return {"error": "Max 5 tickers allowed"}, 400

        companies = []
        sectors = set()
        for t in tickers:
            company = await self._get_company(t)
            if not company:
                return {"error": f"Company '{t}' not found"}, 404
            companies.append(company)
            if company.get("sector_main"):
                sectors.add(company["sector_main"])

        sector_warning = None
        if len(sectors) > 1:
            sector_warning = "Şirketler farklı sektörlerden. Karşılaştırma anlamlı olmayabilir."

        scores = {}
        ratios = {}
        for ticker in tickers:
            sc = await self._get_score(ticker, period_key)
            scores[ticker] = sc
            rt = await self._get_ratios(ticker, period_key)
            ratios[ticker] = rt

        comparison = self._build_comparison(tickers, ratios, scores)
        chart_data = self._build_chart_data(tickers, scores, ratios)

        return {
            "tickers": tickers,
            "companies": {c["ticker"]: c for c in companies},
            "period": period_key,
            "sector_warning": sector_warning,
            "sectors": list(sectors),
            "scores": scores,
            "ratios": ratios,
            "comparison": comparison,
            "visualization_data": chart_data,
        }

    async def _get_company(self, ticker: str) -> Optional[dict]:
        r = await self.db.query(
            "SELECT ticker, name, sector_main, market_cap FROM companies WHERE ticker = ? AND is_active = 1",
            [ticker]
        )
        if not r.first:
            return None
        return {
            "ticker": r.first["ticker"],
            "name": r.first["name"],
            "sector": r.first["sector_main"],
            "market_cap": r.first.get("market_cap"),
        }

    async def _get_score(self, ticker: str, period_key: str) -> dict:
        r = await self.db.query(
            "SELECT * FROM company_scores WHERE ticker = ? AND period_key = ? AND score_version = 'v1' ORDER BY computed_at DESC LIMIT 1",
            [ticker, period_key]
        )
        if not r.first:
            return {"composite_score": None, "absolute_score": None, "absolute_label": None}
        row = r.first
        return {
            "composite_score": row.get("composite_score"),
            "reliability": row.get("reliability"),
            "pillars": {
                "finansal_saglik": row.get("pillar_finansal_saglik"),
                "karlilik_buyume": row.get("pillar_karlilik_buyume"),
                "degerleme": row.get("pillar_degerleme"),
            },
            "absolute_score": row.get("absolute_score"),
            "absolute_label": row.get("absolute_label"),
            "data_completeness": row.get("data_completeness"),
            "benchmark_source": row.get("benchmark_source"),
            "n_peers": row.get("n_peers"),
        }

    async def _get_ratios(self, ticker: str, period_key: str) -> dict:
        if not period_key:
            period_key = "TTM"
        placeholders = ",".join("?" for _ in KEY_RATIOS)
        r = await self.db.query(
            f"SELECT ratio_code, ratio_value FROM company_ratios WHERE ticker = ? AND period_key = ? AND ratio_code IN ({placeholders}) AND ratio_value IS NOT NULL",
            [ticker, period_key] + KEY_RATIOS
        )
        result = {}
        for row in r.results:
            result[row["ratio_code"]] = {
                "value": row["ratio_value"],
                "name": RATIO_NAMES_COMPARE.get(row["ratio_code"], row["ratio_code"]),
                "category": RATIO_CATEGORIES_COMPARE.get(row["ratio_code"], "other"),
            }
        return result

    def _build_comparison(self, tickers: list, ratios: dict, scores: dict) -> dict:
        comparison = {}
        for rc in KEY_RATIOS:
            values = {}
            for t in tickers:
                if rc in ratios.get(t, {}):
                    values[t] = ratios[t][rc]["value"]
            if not values:
                continue

            sorted_vals = sorted(values.items(), key=lambda x: x[1])
            best = sorted_vals[-1][0] if HIGHER_IS_BETTER.get(rc, True) else sorted_vals[0][0]
            worst = sorted_vals[0][0] if HIGHER_IS_BETTER.get(rc, True) else sorted_vals[-1][0]

            vals_only = [v for _, v in sorted_vals]
            median = sorted(vals_only)[len(vals_only) // 2] if vals_only else None

            comparison[rc] = {
                "values": {t: values[t] for t in tickers if t in values},
                "ranking": [t for t, _ in (sorted_vals if HIGHER_IS_BETTER.get(rc, True) else reversed(sorted_vals))],
                "median": median,
                "best": best,
                "worst": worst,
                "name": RATIO_NAMES_COMPARE.get(rc, rc),
                "category": RATIO_CATEGORIES_COMPARE.get(rc, "other"),
            }

        return comparison

    def _build_chart_data(self, tickers: list, scores: dict, ratios: dict) -> dict:
        radar_categories = ["finansal_saglik", "karlilik_buyume", "degerleme"]
        radar_series = []
        for t in tickers:
            sc = scores.get(t, {})
            pillars = sc.get("pillars", {})
            radar_series.append({
                "name": t,
                "data": [pillars.get(cat) for cat in radar_categories],
            })

        bar_categories = [rc for rc in KEY_RATIOS if any(rc in ratios.get(t, {}) for t in tickers)]
        bar_series = []
        for t in tickers:
            bar_series.append({
                "name": t,
                "data": [ratios.get(t, {}).get(rc, {}).get("value") for rc in bar_categories],
            })

        return {
            "radar_chart": {
                "categories": radar_categories,
                "categories_tr": ["Finansal Sağlık", "Kârlılık & Büyüme", "Değerleme"],
                "series": radar_series,
            },
            "bar_chart": {
                "categories": bar_categories,
                "categories_tr": [RATIO_NAMES_COMPARE.get(rc, rc) for rc in bar_categories],
                "series": bar_series,
            },
            "score_summary": {
                ticker: {
                    "composite_score": scores.get(ticker, {}).get("composite_score"),
                    "absolute_score": scores.get(ticker, {}).get("absolute_score"),
                    "absolute_label": scores.get(ticker, {}).get("absolute_label"),
                }
                for ticker in tickers
            },
        }
