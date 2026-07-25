from typing import Optional


class RiskBuilder:
    def build(self, ratios: dict, trends: Optional[dict], sector: Optional[str] = None) -> dict:
        rc_data = ratios.get("ratios", {})
        risk_scores = {}

        liquidity_score = self._assess_liquidity(rc_data)
        leverage_score = self._assess_leverage(rc_data)
        profitability_score = self._assess_profitability(rc_data)
        valuation_score = self._assess_valuation(rc_data)

        indicators = {}
        if liquidity_score is not None:
            indicators["liquidity_risk"] = liquidity_score
        if leverage_score is not None:
            indicators["leverage_risk"] = leverage_score
        if profitability_score is not None:
            indicators["profitability_risk"] = profitability_score
        if valuation_score is not None:
            indicators["valuation_risk"] = valuation_score

        scores = [v["score"] for v in indicators.values() if v is not None]
        composite = sum(scores) / len(scores) if scores else 50
        level = self._risk_level(composite)

        risk_trends = {}
        if trends:
            td = trends.get("trends", {})
            for key, trend_key in [("leverage_risk", "debt_equity"), ("profitability_risk", "roe"), ("liquidity_risk", "current_ratio")]:
                if trend_key in td:
                    risk_trends[key] = td[trend_key].get("direction", "stable")

        mitigations = []
        if liquidity_score and liquidity_score["score"] <= 30:
            mitigations.append("Güçlü likidite pozisyonu finansal riski dengeliyor")
        if leverage_score and leverage_score["score"] <= 30:
            mitigations.append("Düşük borçluluk oranı finansal esneklik sağlıyor")
        if profitability_score and profitability_score["score"] <= 20:
            mitigations.append("Güçlü kârlılık metrikleri risk primini düşürüyor")

        return {
            "composite_risk_score": round(composite, 1),
            "risk_level": level,
            "indicators": indicators,
            "risk_trends": risk_trends if risk_trends else None,
            "mitigation_factors": mitigations if mitigations else None,
        }

    def _assess_liquidity(self, ratios: dict) -> Optional[dict]:
        cr = ratios.get("current_ratio", {}).get("value")
        if cr is None:
            return None
        raw_score = max(0, min(100, (1.0 - cr / 3.0) * 100)) if cr > 0 else 100
        factors = [{"factor": "current_ratio", "value": cr, "threshold": 1.0, "status": "healthy" if cr >= 1.5 else "acceptable" if cr >= 1.0 else "warning" if cr >= 0.5 else "critical"}]
        return {"score": round(raw_score, 1), "level": self._risk_level(raw_score), "factors": factors}

    def _assess_leverage(self, ratios: dict) -> Optional[dict]:
        de = ratios.get("debt_equity", {}).get("value")
        dr = ratios.get("debt_ratio", {}).get("value")
        factors = []
        scores = []
        if de is not None:
            raw = max(0, min(100, (de / 3.0) * 100))
            scores.append(raw)
            factors.append({"factor": "debt_equity", "value": de, "threshold": 1.0, "status": "healthy" if de < 0.5 else "acceptable" if de < 1.5 else "warning" if de < 3.0 else "critical"})
        if dr is not None:
            raw = max(0, min(100, dr * 100))
            scores.append(raw)
            factors.append({"factor": "debt_ratio", "value": dr, "threshold": 0.5, "status": "healthy" if dr < 0.3 else "acceptable" if dr < 0.5 else "warning" if dr < 0.7 else "critical"})
        if not scores:
            return None
        composite = sum(scores) / len(scores)
        return {"score": round(composite, 1), "level": self._risk_level(composite), "factors": factors}

    def _assess_profitability(self, ratios: dict) -> Optional[dict]:
        roe = ratios.get("roe", {}).get("value")
        nm = ratios.get("net_margin", {}).get("value")
        factors = []
        scores = []
        if roe is not None:
            raw = max(0, min(100, (1.0 - min(roe, 0.5) / 0.5) * 100))
            scores.append(raw)
            factors.append({"factor": "roe", "value": roe, "threshold": 0.15, "status": "healthy" if roe >= 0.15 else "acceptable" if roe >= 0.10 else "warning"})
        if nm is not None:
            raw = max(0, min(100, (1.0 - min(nm, 0.3) / 0.3) * 100))
            scores.append(raw)
            factors.append({"factor": "net_margin", "value": nm, "threshold": 0.10, "status": "healthy" if nm >= 0.10 else "acceptable" if nm >= 0.05 else "warning"})
        if not scores:
            return None
        composite = sum(scores) / len(scores)
        return {"score": round(composite, 1), "level": self._risk_level(composite), "factors": factors}

    def _assess_valuation(self, ratios: dict) -> Optional[dict]:
        pe = ratios.get("pe", {}).get("value")
        if pe is None:
            return None
        raw = max(0, min(100, (min(pe, 30) / 30) * 100))
        factors = [{"factor": "pe_ratio", "value": pe, "threshold": 15, "status": "healthy" if pe < 10 else "acceptable" if pe < 15 else "warning" if pe < 25 else "critical"}]
        return {"score": round(raw, 1), "level": self._risk_level(raw), "factors": factors}

    def _risk_level(self, score: float) -> str:
        if score <= 20:
            return "low"
        if score <= 40:
            return "moderate"
        if score <= 60:
            return "high"
        return "critical"
