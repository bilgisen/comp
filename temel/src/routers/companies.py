from typing import Optional
from datetime import datetime
from db.client import D1Client
from models.company import CompanyModel
from models.financial import FinancialModel
from models.metrics import MetricsModel
from services.ratio_calculator import RatioCalculator
from kv.cache import KVCache
from routers.mappings import map_financial_group, map_statement_type, RATIO_NAMES
from services.screener import ScreenerService


async def list_companies(page_str: str, limit_str: str, sector: Optional[str], db: D1Client) -> dict:
    page = int(page_str) if page_str else 1
    limit = int(limit_str) if limit_str else 50
    model = CompanyModel(db)
    return await model.get_all(page, min(limit, 100), sector)


async def get_company_profile(ticker: str, db: D1Client) -> dict:
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not company:
        return {"error": "Company not found"}, 404
    metrics_model = MetricsModel(db)
    metrics = await metrics_model.get_by_ticker(ticker)
    financial_model = FinancialModel(db)
    latest_period = await financial_model.get_latest_period(ticker)
    key_ratios = await financial_model.get_ratios(ticker, latest_period,
        ["current_ratio", "debt_to_equity", "roe", "net_margin", "pe_ratio"])
    fg = company.get("financial_group", "XI_29")
    return {
        "ticker": company["ticker"],
        "name": company["name"],
        "sector_main": company["sector_main"],
        "industry": company.get("industry"),
        "financial_group": fg,
        "financial_group_label": map_financial_group(fg),
        "market_data": {
            "last_price": metrics["last_price"] if metrics else None,
            "market_cap": metrics["market_cap"] if metrics else None,
            "free_float_pct": metrics["free_float_pct"] if metrics else None,
            "pe_ratio": metrics["pe_ratio"] if metrics else None,
            "pb_ratio": metrics["pb_ratio"] if metrics else None
        } if metrics else None,
        "key_ratios": {r["ratio_code"]: r["ratio_value"] for r in key_ratios},
        "latest_period": latest_period
    }, 200


async def get_statements(ticker: str, period_key: Optional[str], db: D1Client) -> dict:
    model = FinancialModel(db)
    company_model = CompanyModel(db)
    statements = await model.get_statements(ticker, period_key)
    if not statements:
        return {"error": "No statements found"}, 404

    company = await company_model.get_by_ticker(ticker)
    fg = company["financial_group"] if company else "XI_29"
    mappings = await model.get_item_code_mappings(fg)
    code_to_type = {m["item_code"]: m["statement_type"] for m in mappings if m.get("statement_type")}

    grouped = {}
    for s in statements:
        st = code_to_type.get(s["item_code"], "other")
        entry = dict(s)
        entry["financial_group_label"] = map_financial_group(s.get("financial_group", fg))
        entry["statement_type"] = st
        entry["statement_type_tr"] = map_statement_type(st)
        if st not in grouped:
            grouped[st] = {"label": map_statement_type(st), "items": []}
        grouped[st]["items"].append(entry)

    return {
        "ticker": ticker.upper(),
        "period_key": period_key or "all",
        "financial_group": fg,
        "financial_group_label": map_financial_group(fg),
        "total_items": len(statements),
        "grouped": grouped,
        "statements": statements
    }, 200


async def get_ratios(ticker: str, period_key: Optional[str], ratio_codes_str: Optional[str], db: D1Client) -> dict:
    ratio_codes = ratio_codes_str.split(",") if ratio_codes_str else None
    model = FinancialModel(db)
    if not period_key:
        period_key = await model.get_latest_period(ticker)
    ratios = await model.get_ratios(ticker, period_key, ratio_codes)
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not ratios:
        return {"error": "No ratios found"}, 404
    enriched = []
    for r in ratios:
        if r["ratio_value"] is not None:
            enriched.append({
                "code": r["ratio_code"],
                "value": r["ratio_value"],
                "name": RATIO_NAMES.get(r["ratio_code"], r["ratio_code"])
            })
    return {
        "ticker": ticker.upper(),
        "company_name": company["name"] if company else None,
        "sector": company["sector_main"] if company else None,
        "period": period_key,
        "total_ratios": len(enriched),
        "ratios": enriched,
        "ratio_map": {r["code"]: r["value"] for r in enriched}
    }, 200


async def get_trends(ticker: str, periods_str: str, ratio_codes_str: Optional[str], db: D1Client) -> dict:
    periods = int(periods_str) if periods_str else 8
    ratio_codes = ratio_codes_str.split(",") if ratio_codes_str else None
    model = FinancialModel(db)
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not company:
        return {"error": "Company not found"}, 404
    available = await model.get_distinct_periods(ticker)
    available = available[:periods]
    trend_data = {}
    for pk in available:
        ratios = await model.get_ratios(ticker, pk, ratio_codes)
        for r in ratios:
            code = r["ratio_code"]
            if code not in trend_data:
                trend_data[code] = {"name": RATIO_NAMES.get(code, code), "values": []}
            trend_data[code]["values"].append({
                "period": pk,
                "value": r["ratio_value"]
            })
    return {
        "ticker": ticker.upper(),
        "company_name": company["name"],
        "periods_analyzed": len(available),
        "trends": trend_data
    }, 200


async def get_sectors(db: D1Client) -> dict:
    model = CompanyModel(db)
    sectors = await model.get_sectors()
    return {"sectors": sectors, "total": len(sectors)}, 200


async def search_companies(q: str, db: D1Client) -> dict:
    if len(q) < 1:
        return {"error": "Query too short"}, 400
    model = CompanyModel(db)
    results = await model.search(q)
    return {"query": q, "results": results, "total": len(results)}, 200


async def get_financial_summary(ticker: str, period_key: Optional[str], db: D1Client) -> dict:
    model = FinancialModel(db)
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    records = await model.get_financial_summary(ticker, period_key)
    if not records:
        return {"error": "No summary data found"}, 404
    return {
        "ticker": ticker.upper(),
        "company_name": company["name"] if company else None,
        "total_periods": len(records),
        "records": records
    }, 200


async def calculate_ratios(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    company_model = CompanyModel(db)
    company = await company_model.get_by_ticker(ticker)
    if not company:
        return {"error": "Company not found"}, 404
    financial_model = FinancialModel(db)
    if not period_key:
        period_key = await financial_model.get_latest_period(ticker)
    statements = await financial_model.get_statements(ticker, period_key)
    metrics_model = MetricsModel(db)
    metrics = await metrics_model.get_by_ticker(ticker)
    calculator = RatioCalculator()
    results = calculator.calculate(
        ticker, statements, company["sector_main"],
        metrics["market_cap"] if metrics else None, period_key
    )
    saved = await financial_model.save_ratios([
        {"ticker": ticker, "period_key": period_key, "ratio_code": r.ratio_code,
         "ratio_value": r.value, "is_ttm": r.ratio_code in [k for k, v in RatioCalculator.DEFAULT_RATIOS.items() if v.type == "ttm"],
         "calculation_method": r.calculation_method, "data_quality_score": r.data_quality_score,
         "computed_at": datetime.utcnow().isoformat()}
        for r in results if r.success
    ])
    cache = KVCache(env.TEMEL_CACHE)
    await cache.delete_by_prefix(f"ratios:{ticker}:")
    return {
        "ticker": ticker.upper(), "period": period_key,
        "total": len(results), "successful": saved, "failed": len(results) - saved
    }, 200


async def screener_filter(params: dict, db: D1Client) -> dict:
    service = ScreenerService(db)
    return await service.filter(params), 200
