from typing import Optional
from datetime import datetime, timezone

from db.client import D1Client
from kv.cache import KVCache
from services.ai.profile_builder import ProfileBuilder
from services.ai.ratio_builder import RatioBuilder
from services.ai.trend_builder import TrendBuilder
from services.ai.insight_builder import InsightBuilder
from services.ai.risk_builder import RiskBuilder
from services.ai.swot_builder import SWOTBuilder
from services.ai.sector_context_builder import SectorContextBuilder
from services.ai.compare_builder import CompareBuilder


class AIContextBuilder:
    def __init__(self, db: D1Client, cache: Optional[KVCache] = None):
        self.db = db
        self.cache = cache
        self.profile_builder = ProfileBuilder(db)
        self.ratio_builder = RatioBuilder(db)
        self.trend_builder = TrendBuilder(db)
        self.insight_builder = InsightBuilder()
        self.risk_builder = RiskBuilder()
        self.swot_builder = SWOTBuilder(db)
        self.sector_builder = SectorContextBuilder(db)
        self.compare_builder = CompareBuilder(db)

    async def build_context(self, ticker: str, query_type: str = "general", period_key: Optional[str] = None) -> dict:
        ticker = ticker.upper()
        profile = await self.profile_builder.build(ticker)
        if not profile:
            return {"error": f"Company {ticker} not found"}, 404

        if not period_key:
            pr = await self.db.query(
                "SELECT period_key FROM company_ratios WHERE ticker = ? ORDER BY computed_at DESC LIMIT 1",
                [ticker]
            )
            period_key = pr.first["period_key"] if pr.first else "TTM"

        ratios = await self.ratio_builder.build(ticker, period_key, profile.get("sector"))
        trends = await self.trend_builder.build(ticker, 8, profile.get("sector")) if query_type == "detailed" else None
        insights = self.insight_builder.build(ratios, None, {"trends": trends["trends"]} if trends else None, profile.get("sector"))
        risk = self.risk_builder.build(ratios, {"trends": trends["trends"]} if trends else None, profile.get("sector"))

        sector_position = None
        own_score = None
        if profile.get("sector"):
            sr = await self.db.query(
                "SELECT cs.composite_score FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE c.sector_main = ? AND cs.period_key = 'TTM' AND cs.composite_score IS NOT NULL ORDER BY cs.composite_score DESC",
                [profile["sector"]]
            )
            scores = [row["composite_score"] for row in sr.results]
            if scores:
                own_r = await self.db.query(
                    "SELECT composite_score FROM company_scores WHERE ticker = ? AND period_key = 'TTM' AND composite_score IS NOT NULL LIMIT 1",
                    [ticker]
                )
                own_score = own_r.first["composite_score"] if own_r.first else None
                if own_score is not None:
                    below = sum(1 for s in scores if s < own_score)
                    rank = below + 1
                    sector_position = {
                        "benchmark_source": "sector",
                        "benchmark_name": profile["sector"],
                        "n_peers": len(scores),
                        "sector_rank": rank,
                        "sector_percentile": round((1 - rank / len(scores)) * 100, 1),
                    }

        financial_health = None
        if own_score is not None:
            abs_r = await self.db.query(
                "SELECT absolute_score, absolute_label FROM company_scores WHERE ticker = ? AND period_key = 'TTM' LIMIT 1",
                [ticker]
            )
            abs_data = abs_r.first if abs_r.first else {}
            financial_health = {
                "composite_score": own_score,
                "absolute_score": abs_data.get("absolute_score"),
                "absolute_label": abs_data.get("absolute_label"),
            }

        return {
            "ticker": ticker,
            "context_type": query_type,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "profile": profile,
            "financial_health": financial_health,
            "sector_position": sector_position,
            "ratios": ratios,
            "trends": trends,
            "key_insights": insights,
            "risk_assessment": risk,
            "metadata": {
                "period": period_key,
                "data_completeness": ratios.get("data_completeness"),
                "missing_ratios": ratios.get("missing_ratios", []),
                "language": "tr",
                "version": "2.0",
            },
        }

    async def build_swot(self, ticker: str, period_key: Optional[str] = None) -> dict:
        ticker = ticker.upper()
        profile = await self.profile_builder.build(ticker)
        if not profile:
            return {"error": f"Company {ticker} not found"}, 404
        if not period_key:
            pr = await self.db.query(
                "SELECT period_key FROM company_ratios WHERE ticker = ? ORDER BY computed_at DESC LIMIT 1", [ticker]
            )
            period_key = pr.first["period_key"] if pr.first else "TTM"

        ratios = await self.ratio_builder.build(ticker, period_key, profile.get("sector"))
        trends = await self.trend_builder.build(ticker, 8, profile.get("sector"))
        swot = await self.swot_builder.build(ticker, ratios, None, {"trends": trends["trends"]}, profile.get("sector"))
        swot["ticker"] = ticker
        swot["period"] = period_key
        return swot

    async def build_analysis(self, ticker: str, period_key: Optional[str] = None) -> dict:
        context = await self.build_context(ticker, "detailed", period_key)
        if isinstance(context, tuple):
            return context
        swot = await self.build_swot(ticker, period_key)
        profile = context.get("profile", {})
        health = context.get("financial_health", {})
        sector_pos = context.get("sector_position", {})

        exec_summary = f"{profile.get('name', ticker)} için temel analiz."
        if health:
            exec_summary += f" Skor: {health.get('composite_score', 'N/A')}/100, {health.get('absolute_label', 'N/A')}."
        if sector_pos:
            exec_summary += f" Sektör sıralaması: {sector_pos.get('sector_rank', '?')}/{sector_pos.get('n_peers', '?')}."

        return {
            "ticker": ticker,
            "period": context.get("metadata", {}).get("period"),
            "executive_summary": exec_summary,
            "financial_health": health,
            "sector_position": sector_pos,
            "key_insights": context.get("key_insights", []),
            "risk_assessment": context.get("risk_assessment"),
            "swot": {k: swot.get(k) for k in ["strengths", "weaknesses", "opportunities", "threats"]},
            "peer_rank": swot.get("peer_rank"),
        }

    async def build_fundamental_report(self, ticker: str, period_key: Optional[str] = None) -> dict:
        context = await self.build_context(ticker, "detailed", period_key)
        if isinstance(context, tuple):
            return context
        swot = await self.build_swot(ticker, period_key)

        return {
            "ticker": ticker,
            "report_type": "fundamental",
            "generated_at": context.get("generated_at"),
            "profile": context.get("profile"),
            "financial_health": context.get("financial_health"),
            "sector_position": context.get("sector_position"),
            "ratios": context.get("ratios"),
            "trends": context.get("trends"),
            "key_insights": context.get("key_insights"),
            "risk_assessment": context.get("risk_assessment"),
            "swot": {k: swot.get(k) for k in ["strengths", "weaknesses", "opportunities", "threats", "peer_rank"]},
            "data_quality": {
                "completeness": context.get("metadata", {}).get("data_completeness"),
                "missing_data": context.get("metadata", {}).get("missing_ratios", []),
                "version": "2.0",
            },
            "sections": [
                {"id": "executive_summary", "title": "Yönetici Özeti", "visualization_type": None},
                {"id": "financial_health", "title": "Finansal Sağlık", "visualization_type": "score_card"},
                {"id": "ratios", "title": "Finansal Rasyolar", "visualization_type": "table"},
                {"id": "trends", "title": "Trend Analizi", "visualization_type": "line_chart"},
                {"id": "swot", "title": "SWOT Analizi", "visualization_type": "grid"},
                {"id": "risk", "title": "Risk Değerlendirmesi", "visualization_type": "gauge"},
            ],
        }
