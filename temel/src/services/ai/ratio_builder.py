from typing import Optional, List
from db.client import D1Client

RATIO_META = {
    "pe": {"name": "F/K Oranı", "category": "valuation", "higher_is_better": False},
    "pb": {"name": "PD/DD Oranı", "category": "valuation", "higher_is_better": False},
    "ev_ebitda": {"name": "FD/FAVÖK", "category": "valuation", "higher_is_better": False},
    "ev_sales": {"name": "FD/Satışlar", "category": "valuation", "higher_is_better": False},
    "roe": {"name": "Özkaynak Kârlılığı (ROE)", "category": "profitability", "higher_is_better": True},
    "roa": {"name": "Aktif Kârlılığı (ROA)", "category": "profitability", "higher_is_better": True},
    "net_margin": {"name": "Net Kâr Marjı", "category": "profitability", "higher_is_better": True},
    "gross_margin": {"name": "Brüt Kâr Marjı", "category": "profitability", "higher_is_better": True},
    "operating_margin": {"name": "Faaliyet Kâr Marjı", "category": "profitability", "higher_is_better": True},
    "ebitda_margin": {"name": "FAVÖK Marjı", "category": "profitability", "higher_is_better": True},
    "profit_growth": {"name": "Kâr Büyümesi", "category": "profitability", "higher_is_better": True},
    "current_ratio": {"name": "Cari Oran", "category": "liquidity", "higher_is_better": True},
    "acid_test_ratio": {"name": "Asit Test Oranı", "category": "liquidity", "higher_is_better": True},
    "cash_ratio": {"name": "Nakit Oranı", "category": "liquidity", "higher_is_better": True},
    "debt_equity": {"name": "Borç/Özkaynak", "category": "leverage", "higher_is_better": False},
    "debt_ratio": {"name": "Borçlanma Oranı", "category": "leverage", "higher_is_better": False},
    "interest_coverage": {"name": "Faiz Karşılama Oranı", "category": "leverage", "higher_is_better": True},
    "asset_turnover": {"name": "Aktif Devir Hızı", "category": "efficiency", "higher_is_better": True},
    "inventory_turnover": {"name": "Stok Devir Hızı", "category": "efficiency", "higher_is_better": True},
    "net_interest_margin": {"name": "Net Faiz Marjı", "category": "banking", "higher_is_better": True},
    "loan_to_deposit": {"name": "Kredi/Mevduat", "category": "banking", "higher_is_better": False},
    "npl_ratio": {"name": "Takipteki Kredi Oranı", "category": "asset_quality", "higher_is_better": False},
    "cost_income_ratio": {"name": "Maliyet/Gelir", "category": "efficiency", "higher_is_better": False},
    "nav_discount": {"name": "NAD İskontosu", "category": "valuation", "higher_is_better": False},
    "rental_yield": {"name": "Kira Getirisi", "category": "profitability", "higher_is_better": True},
    "loss_ratio": {"name": "Hasar Oranı", "category": "insurance", "higher_is_better": False},
    "expense_ratio": {"name": "Gider Oranı", "category": "efficiency", "higher_is_better": False},
    "combined_ratio": {"name": "Birleşik Oran", "category": "insurance", "higher_is_better": False},
    "eps": {"name": "Hisse Başına Kâr", "category": "profitability", "higher_is_better": True},
    "book_per_share": {"name": "Defter Değeri", "category": "valuation", "higher_is_better": True},
}

INTERPRETATIONS = {
    "pe": lambda v, m: f"Düşük F/K ({(v):.1f}x), sektör medyanı {m:.1f}x" if v < m else f"F/K oranı {(v):.1f}x, sektör medyanına yakın" if v < m * 1.5 else f"Yüksek F/K ({(v):.1f}x) - değerleme riski olabilir",
    "pb": lambda v, m: f"PD/DD {(v):.2f}x - sektör medyanı {m:.2f}x" if v < m else f"PD/DD {(v):.2f}x, sektör medyanı {m:.2f}x",
    "roe": lambda v, m: f"ROE %{v*100:.1f} - sektör medyanı %{m*100:.1f} üzerinde, güçlü kârlılık" if v > m else f"ROE %{v*100:.1f} - sektör medyanı %{m*100:.1f}",
    "net_margin": lambda v, m: f"Net kâr marjı %{v*100:.1f}, sektör medyanı %{m*100:.1f}" if v > m else f"Net kâr marjı %{v*100:.1f}, sektör medyanı %{m*100:.1f} altında",
    "current_ratio": lambda v, m: f"Cari oran {v:.2f} - likidite güçlü" if v > 1.5 else f"Cari oran {v:.2f} - likidite orta" if v > 1.0 else f"Cari oran {v:.2f} - likidite zayıf",
    "debt_equity": lambda v, m: f"Borç/özkaynak {v:.2f} - sektör medyanı {m:.2f}" if v < m else f"Borç/özkaynak {v:.2f} - sektör medyanı {m:.2f}'ın üzerinde",
}

SCORE_THRESHOLDS = {
    "current_ratio": [(0.5, 0), (0.8, 25), (1.2, 50), (1.8, 75), (float("inf"), 100)],
    "cash_ratio": [(0.05, 0), (0.15, 25), (0.30, 50), (0.50, 75), (float("inf"), 100)],
    "debt_equity": [(0.0, 100), (1.0, 75), (2.5, 50), (4.0, 25), (float("inf"), 0)],
    "interest_coverage": [(0.0, 0), (1.0, 25), (3.0, 50), (6.0, 75), (float("inf"), 100)],
    "roe": [(0.0, 0), (0.05, 25), (0.10, 50), (0.18, 75), (float("inf"), 100)],
    "roa": [(-0.05, 0), (0.0, 25), (0.05, 50), (0.10, 75), (float("inf"), 100)],
    "net_margin": [(-0.10, 0), (0.0, 25), (0.05, 50), (0.12, 75), (float("inf"), 100)],
    "pe": [(0.0, 100), (8.0, 75), (15.0, 50), (25.0, 25), (float("inf"), 0)],
    "pb": [(0.0, 100), (1.0, 75), (3.0, 50), (7.0, 25), (float("inf"), 0)],
}


class RatioBuilder:
    def __init__(self, db: D1Client):
        self.db = db

    async def build(self, ticker: str, period_key: str = "TTM", sector: Optional[str] = None) -> dict:
        r = await self.db.query(
            "SELECT ratio_code, ratio_value FROM company_ratios WHERE ticker = ? AND period_key = ? AND ratio_value IS NOT NULL ORDER BY ratio_code",
            [ticker.upper(), period_key]
        )
        raw = {row["ratio_code"]: row["ratio_value"] for row in r.results}

        sector_benchmarks = {}
        if sector:
            sb = await self.db.query(
                "SELECT ratio_code, median_ew, p25, p75, n_peers, reliability FROM sector_benchmarks WHERE sector_name = ? AND benchmark_type = 'sector' AND period_key = ?",
                [sector, period_key]
            )
            for row in sb.results:
                sector_benchmarks[row["ratio_code"]] = row

        ratios = {}
        for code, value in raw.items():
            meta = RATIO_META.get(code)
            if not meta:
                continue
            entry = {
                "value": value,
                "name": meta["name"],
                "category": meta["category"],
                "higher_is_better": meta["higher_is_better"],
            }
            bench = sector_benchmarks.get(code)
            if bench and bench.get("median_ew") is not None:
                med = bench["median_ew"]
                entry["sector_context"] = {
                    "median": med,
                    "p25": bench.get("p25"),
                    "p75": bench.get("p75"),
                    "percentile": self._estimate_percentile(value, med, bench.get("p25"), bench.get("p75")),
                    "position": "above_median" if value > med else "below_median",
                }
                interp_fn = INTERPRETATIONS.get(code)
                if interp_fn:
                    entry["interpretation"] = interp_fn(value, med)
            if code in SCORE_THRESHOLDS:
                entry["absolute_score"] = self._absolute_ratio_score(value, SCORE_THRESHOLDS[code])
            ratios[code] = entry

        completeness = len(ratios) / len(RATIO_META) if RATIO_META else 0
        missing = [c for c in RATIO_META if c not in raw]

        return {
            "period": period_key,
            "ratios": ratios,
            "missing_ratios": missing,
            "data_completeness": round(completeness, 2),
            "total_present": len(ratios),
            "total_possible": len(RATIO_META),
        }

    def _estimate_percentile(self, value, median, p25, p75):
        if p25 is None or p75 is None or median is None:
            return None
        if p75 == p25:
            return 50
        if value >= median:
            return min(99, int(50 + (value - median) / (p75 - median) * 25))
        return max(1, int(50 - (median - value) / (median - p25) * 25))

    def _absolute_ratio_score(self, value, thresholds):
        if value is None:
            return None
        for max_val, score in thresholds:
            if value <= max_val:
                return score
        return 50.0
