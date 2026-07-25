from typing import Optional, List
from db.client import D1Client
from datetime import datetime

TREND_RATIOS = ["pe", "pb", "roe", "net_margin", "debt_equity", "current_ratio", "ev_ebitda", "roa", "gross_margin", "profit_growth"]


class TrendBuilder:
    def __init__(self, db: D1Client):
        self.db = db

    async def build(self, ticker: str, max_periods: int = 8, sector: Optional[str] = None) -> dict:
        periods_r = await self.db.query(
            "SELECT DISTINCT period_key FROM company_ratios WHERE ticker = ? AND period_key != 'TTM' ORDER BY period_key DESC LIMIT ?",
            [ticker.upper(), max_periods]
        )
        periods = [r["period_key"] for r in periods_r.results if r["period_key"]]

        if not periods:
            r = await self.db.query(
                "SELECT DISTINCT period_key FROM company_ratios WHERE ticker = ? ORDER BY period_key DESC LIMIT 1",
                [ticker.upper()]
            )
            if r.first:
                periods = [r.first["period_key"]]

        trends = {}
        for rc in TREND_RATIOS:
            values = []
            for pk in periods:
                vr = await self.db.query(
                    "SELECT ratio_value FROM company_ratios WHERE ticker = ? AND period_key = ? AND ratio_code = ? AND ratio_value IS NOT NULL LIMIT 1",
                    [ticker.upper(), pk, rc]
                )
                values.append({"period": pk, "value": vr.first["ratio_value"] if vr.first else None})

            actual_values = [v["value"] for v in values if v["value"] is not None]
            if len(actual_values) < 2:
                continue

            direction = self._classify_direction(actual_values)
            momentum = self._classify_momentum(actual_values)
            qoq_change = self._calc_change(actual_values[-1], actual_values[-2]) if len(actual_values) >= 2 else None
            yoy_change = self._calc_change(actual_values[-1], actual_values[-4]) if len(actual_values) >= 4 else None
            cagr = self._calc_cagr(actual_values) if len(actual_values) >= 4 else None

            trends[rc] = {
                "values": values,
                "direction": direction,
                "momentum": momentum,
                "qoq_change": qoq_change,
                "yoy_change": yoy_change,
                "cagr": cagr,
                "volatility": self._calc_volatility(actual_values),
                "n_periods": len(actual_values),
                "missing_periods": max_periods - len(actual_values),
            }

        sector_trends = {}
        if sector and trends:
            for rc, data in trends.items():
                if data.get("yoy_change") is not None:
                    sr = await self.db.query(
                        "SELECT median_ew FROM sector_benchmarks WHERE sector_name = ? AND benchmark_type = 'sector' AND ratio_code = ? AND period_key IN (SELECT DISTINCT period_key FROM company_ratios ORDER BY period_key DESC LIMIT 4) ORDER BY period_key DESC LIMIT 1",
                        [sector, rc]
                    )
                    if sr.first:
                        sector_trends[rc] = {"sector_median": sr.first["median_ew"]}

        return {
            "periods": periods,
            "n_periods": len(periods),
            "trends": trends,
            "sector_comparison": sector_trends if sector_trends else None,
        }

    def _classify_direction(self, values: list) -> str:
        if len(values) < 3:
            return "stable"
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        change = (avg_second - avg_first) / abs(avg_first) if avg_first != 0 else 0
        if change > 0.1:
            return "rising"
        if change < -0.1:
            return "falling"
        return "stable"

    def _classify_momentum(self, values: list) -> str:
        if len(values) < 4:
            return "stable"
        recent = values[-2:]
        older = values[-4:-2]
        if len(recent) >= 2 and len(older) >= 2:
            recent_slope = (recent[-1] - recent[0]) / max(abs(recent[0]), 0.001)
            older_slope = (older[-1] - older[0]) / max(abs(older[0]), 0.001)
            if abs(recent_slope) > abs(older_slope) * 1.2:
                return "accelerating" if recent_slope > 0 else "decelerating"
        return "stable"

    def _calc_change(self, current, previous):
        if current is None or previous is None or previous == 0:
            return None
        return (current - previous) / abs(previous)

    def _calc_cagr(self, values: list) -> Optional[float]:
        if len(values) < 4:
            return None
        first, last = values[0], values[-1]
        if first is None or last is None or first == 0:
            return None
        n_periods = len(values) - 1
        return (last / first) ** (1.0 / n_periods) - 1

    def _calc_volatility(self, values: list) -> Optional[float]:
        if len(values) < 3:
            return None
        mean = sum(values) / len(values)
        if mean == 0:
            return None
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return (variance ** 0.5) / mean
