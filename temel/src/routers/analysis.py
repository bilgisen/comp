from typing import Optional
from db.client import D1Client
from models.financial import FinancialModel
from models.company import CompanyModel
from models.metrics import MetricsModel
from services.ai_context import AIContextBuilder
from services.ratio_calculator import RatioCalculator
from kv.cache import KVCache
from routers.mappings import RATIO_NAMES

async def get_ai_context(ticker: str, ctx_type: str, period_key: Optional[str], force_str: str, db: D1Client, env) -> dict:
    force = force_str == "true"
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    if not force:
        cache_key = f"ai_context:{ticker.upper()}:{ctx_type}:{period_key or 'latest'}"
        cached = await cache.get(cache_key)
        if cached:
            return cached
    builder = AIContextBuilder(db, cache)
    if ctx_type == "comprehensive":
        context = await builder.build_comprehensive_context(ticker, period_key)
    else:
        context = await builder.build_basic_context(ticker, period_key)
    if "error" in context:
        return context, 404
    ttl = settings.CACHE_TTL_AI_CONTEXT if hasattr(settings, 'CACHE_TTL_AI_CONTEXT') else 1800
    cache_key = f"ai_context:{ticker.upper()}:{ctx_type}:{period_key or 'latest'}"
    await cache.set(cache_key, context, ttl)
    return context

async def get_temel_analiz(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not company:
        return {"error": "Company not found"}, 404
    financial_model = FinancialModel(db)
    if not period_key:
        period_key = await financial_model.get_latest_period(ticker)
    ratios = await financial_model.get_ratios(ticker, period_key)
    metrics = await MetricsModel(db).get_by_ticker(ticker)
    ratio_dict = {r["ratio_code"]: r["ratio_value"] for r in ratios if r["ratio_value"] is not None}
    score = _calculate_score(ratio_dict)
    return {
        "ticker": ticker.upper(),
        "company_name": company["name"],
        "sector": company["sector_main"],
        "period": period_key,
        "score": score,
        "key_metrics": {
            code: {"name": RATIO_NAMES.get(code, code), "value": ratio_dict.get(code)}
            for code in ["roe", "current_ratio", "debt_ratio", "net_margin", "pe_ratio"]
            if code in ratio_dict
        },
        "data_quality": "verified"
    }

def _calculate_score(ratio_dict: dict) -> dict:
    score = {"genel": 50, "karlilik": 50, "finansal": 50, "verimlilik": 50, "degerleme": 50}
    if ratio_dict.get("roe") is not None:
        roe = ratio_dict["roe"]
        score["karlilik"] = min(100, max(0, int((roe + 0.5) * 100)))
    if ratio_dict.get("current_ratio") is not None:
        cr = ratio_dict["current_ratio"]
        score["finansal"] = min(100, max(0, int(min(cr, 3) / 3 * 100)))
    if ratio_dict.get("debt_ratio") is not None:
        dr = ratio_dict["debt_ratio"]
        score["finansal"] = (score["finansal"] + min(100, max(0, int((1 - dr) * 100)))) // 2
    if ratio_dict.get("net_margin") is not None:
        nm = ratio_dict["net_margin"]
        score["karlilik"] = (score["karlilik"] + min(100, max(0, int((nm + 0.3) * 200)))) // 2
    if ratio_dict.get("pe_ratio") is not None:
        pe = ratio_dict["pe_ratio"]
        score["degerleme"] = min(100, max(0, int((1 - min(pe, 30) / 30) * 100)))
    score["genel"] = (score["karlilik"] + score["finansal"] + score["verimlilik"] + score["degerleme"]) // 4
    return score

async def get_swot(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not company:
        return {"error": "Company not found"}, 404
    financial_model = FinancialModel(db)
    if not period_key:
        period_key = await financial_model.get_latest_period(ticker)
    ratios = await financial_model.get_ratios(ticker, period_key)
    strengths, weaknesses, opportunities, threats = [], [], [], []
    ratio_lookup = {r["ratio_code"]: r["ratio_value"] for r in ratios if r["ratio_value"] is not None}
    if ratio_lookup.get("roe") is not None:
        if ratio_lookup["roe"] > 0.15:
            strengths.append(f"Güçlü özkaynak kârlılığı (%{ratio_lookup['roe']*100:.1f})")
        elif ratio_lookup["roe"] < 0.05:
            weaknesses.append(f"Düşük özkaynak kârlılığı (%{ratio_lookup['roe']*100:.1f})")
    if ratio_lookup.get("current_ratio") is not None:
        if ratio_lookup["current_ratio"] > 1.5:
            strengths.append(f"Güçlü likidite (cari oran: {ratio_lookup['current_ratio']:.2f})")
        elif ratio_lookup["current_ratio"] < 1.0:
            weaknesses.append(f"Zayıf likidite (cari oran: {ratio_lookup['current_ratio']:.2f})")
    if ratio_lookup.get("debt_ratio") is not None:
        if ratio_lookup["debt_ratio"] < 0.5:
            strengths.append(f"Düşük borçluluk (borçlanma oranı: {ratio_lookup['debt_ratio']:.2f})")
        elif ratio_lookup["debt_ratio"] > 0.8:
            weaknesses.append(f"Yüksek borçluluk (borçlanma oranı: {ratio_lookup['debt_ratio']:.2f})")
    if ratio_lookup.get("net_margin") is not None and ratio_lookup["net_margin"] > 0.1:
        opportunities.append("Kârlılık artış potansiyeli mevcut")
    if ratio_lookup.get("pe_ratio") is not None and ratio_lookup["pe_ratio"] > 25:
        threats.append("Yüksek F/K oranı - değerleme riski")
    if not strengths:
        strengths.append("Sektördeki konumunu koruyor")
    if not weaknesses:
        weaknesses.append("Belirgin zayıf yön tespit edilemedi")
    if not opportunities:
        opportunities.append("Sektör dinamikleri değerlendirilmeli")
    if not threats:
        threats.append("Piyasa koşullarına dikkat edilmeli")
    return {
        "ticker": ticker.upper(), "period": period_key,
        "strengths": strengths[:5], "weaknesses": weaknesses[:5],
        "opportunities": opportunities[:5], "threats": threats[:5]
    }

async def get_fundamental_report(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not company:
        return {"error": "Company not found"}, 404
    financial_model = FinancialModel(db)
    if not period_key:
        period_key = await financial_model.get_latest_period(ticker)
    ratios = await financial_model.get_ratios(ticker, period_key)
    metrics = await MetricsModel(db).get_by_ticker(ticker)
    ratio_dict = {r["ratio_code"]: r["ratio_value"] for r in ratios if r["ratio_value"] is not None}
    score = _calculate_score(ratio_dict)
    return {
        "ticker": ticker.upper(), "company_name": company["name"],
        "sector": company["sector_main"], "period_key": period_key,
        "executive_summary": f"{company['name']} için temel analiz puanı {score['genel']}/100.",
        "financial_health": {
            "overall": "iyi" if score["genel"] > 60 else ("orta" if score["genel"] > 40 else "zayıf"),
            "score": score
        },
        "ratios": ratio_dict,
        "disclaimer": "Bu analiz otomatik veri analizine dayanmaktadır ve yatırım tavsiyesi değildir."
    }
