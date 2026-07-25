from typing import Optional, List
from db.client import D1Client


class SWOTBuilder:
    def __init__(self, db: D1Client):
        self.db = db

    async def build(self, ticker: str, ratios: dict, benchmarks: Optional[dict], trends: Optional[dict], sector: Optional[str] = None) -> dict:
        rc_data = ratios.get("ratios", {})
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []

        for code, entry in rc_data.items():
            value = entry.get("value")
            if value is None:
                continue
            name = entry.get("name", code)
            ctx = entry.get("sector_context")

            if ctx:
                med = ctx.get("median")
                pct = ctx.get("percentile")
                hib = entry.get("higher_is_better", True)
                if med and med != 0:
                    vs_median = (value - med) / abs(med)
                    if (vs_median > 0.3 and hib) or (vs_median < -0.3 and not hib):
                        item = f"{name} %{abs(vs_median)*100:.0f} sektör ortalamasının üzerinde ({value:.2f})"
                        strengths.append({"item": item, "category": entry.get("category"), "impact": self._impact_score(abs(vs_median)), "data": {"ratio": code, "value": value, "sector_median": med, "percentile": pct}})
                    elif (vs_median < -0.3 and hib) or (vs_median > 0.3 and not hib):
                        item = f"{name} %{abs(vs_median)*100:.0f} sektör ortalamasının altında ({value:.2f})"
                        weaknesses.append({"item": item, "category": entry.get("category"), "impact": self._impact_score(abs(vs_median)), "data": {"ratio": code, "value": value, "sector_median": med, "percentile": pct}})

            abs_score = entry.get("absolute_score")
            if abs_score is not None:
                if abs_score >= 75 and entry.get("category") in ("profitability", "liquidity"):
                    if not any(s["data"].get("ratio") == code for s in strengths):
                        strengths.append({"item": f"{name} mutlak skoru yüksek ({abs_score}/100)", "category": entry.get("category"), "impact": 3, "data": {"ratio": code, "absolute_score": abs_score}})
                elif abs_score <= 25 and entry.get("category") in ("profitability", "liquidity", "leverage"):
                    if not any(w["data"].get("ratio") == code for w in weaknesses):
                        weaknesses.append({"item": f"{name} mutlak skoru düşük ({abs_score}/100)", "category": entry.get("category"), "impact": 3, "data": {"ratio": code, "absolute_score": abs_score}})

        trend_data = trends.get("trends", {}) if trends else {}
        for code, td in trend_data.items():
            meta = {"pe": "F/K", "roe": "ROE", "net_margin": "Net Kâr Marjı", "debt_equity": "Borç/Özkaynak", "current_ratio": "Cari Oran"}.get(code, code)
            direction = td.get("direction")
            momentum = td.get("momentum")
            yoy = td.get("yoy_change")
            if direction == "rising" and yoy and yoy > 0.2:
                opportunities.append({"item": f"{meta} yükseliş trendinde (yıllık %{yoy*100:.0f} artış)", "category": "trend", "impact": 4, "data": {"ratio": code, "yoy_change": yoy, "direction": direction}})
            elif direction == "falling" and yoy and yoy < -0.2:
                threats.append({"item": f"{meta} düşüş trendinde (yıllık %{abs(yoy)*100:.0f} azalış)", "category": "trend", "impact": 4, "data": {"ratio": code, "yoy_change": yoy, "direction": direction}})

        peer_rank = None
        if sector:
            sr = await self.db.query(
                "SELECT cs.ticker, cs.composite_score FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE c.sector_main = ? AND cs.period_key = 'TTM' AND cs.composite_score IS NOT NULL ORDER BY cs.composite_score DESC",
                [sector]
            )
            tickers = [row["ticker"] for row in sr.results]
            scores_list = [row["composite_score"] for row in sr.results]
            if ticker in tickers:
                rank = tickers.index(ticker) + 1
                total = len(tickers)
                peer_rank = {"rank": rank, "total": total, "percentile": round((1 - rank / total) * 100, 1) if total > 0 else None}

        if not strengths:
            strengths.append({"item": "Sektördeki konumunu koruyor", "category": "general", "impact": 1, "data": None})
        if not weaknesses:
            weaknesses.append({"item": "Belirgin zayıf yön tespit edilemedi", "category": "general", "impact": 1, "data": None})
        if not opportunities:
            opportunities.append({"item": "Sektör dinamikleri değerlendirilmeli", "category": "general", "impact": 1, "data": None})
        if not threats:
            threats.append({"item": "Piyasa koşullarına dikkat edilmeli", "category": "general", "impact": 1, "data": None})

        return {
            "strengths": sorted(strengths, key=lambda x: x["impact"], reverse=True)[:5],
            "weaknesses": sorted(weaknesses, key=lambda x: x["impact"], reverse=True)[:5],
            "opportunities": sorted(opportunities, key=lambda x: x["impact"], reverse=True)[:5],
            "threats": sorted(threats, key=lambda x: x["impact"], reverse=True)[:5],
            "peer_rank": peer_rank,
        }

    def _impact_score(self, vs_median_pct: float) -> int:
        if vs_median_pct > 1.0:
            return 5
        if vs_median_pct > 0.5:
            return 4
        if vs_median_pct > 0.3:
            return 3
        return 2
