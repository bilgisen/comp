from typing import Optional, List
from db.client import D1Client
from models.financial import FinancialModel
from models.company import CompanyModel
from models.metrics import MetricsModel
from services.ai.context_builder import AIContextBuilder
from services.ai.sector_context_builder import SectorContextBuilder
from services.ai.compare_builder import CompareBuilder
from kv.cache import KVCache

async def get_ai_context(ticker: str, ctx_type: str, period_key: Optional[str], force_str: str, db: D1Client, env) -> dict:
    force = force_str == "true"
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    cache_key = f"ai_context_v2:{ticker.upper()}:{ctx_type}:{period_key or 'latest'}"
    if not force:
        cached = await cache.get(cache_key)
        if cached:
            return cached
    builder = AIContextBuilder(db, cache)
    query_type = "detailed" if ctx_type == "comprehensive" else "general"
    result = await builder.build_context(ticker, query_type, period_key)
    if isinstance(result, tuple):
        return result
    ttl = getattr(settings, 'CACHE_TTL_AI_CONTEXT', 1800)
    await cache.set(cache_key, result, ttl)
    return result

async def get_temel_analiz(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    builder = AIContextBuilder(db)
    result = await builder.build_analysis(ticker, period_key)
    if isinstance(result, tuple):
        return result
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    ttl = getattr(settings, 'CACHE_TTL_AI_CONTEXT', 1800)
    await cache.set(f"analysis_v2:{ticker.upper()}:{period_key or 'latest'}", result, ttl)
    return result

async def get_swot(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    builder = AIContextBuilder(db)
    result = await builder.build_swot(ticker, period_key)
    if isinstance(result, tuple):
        return result
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    ttl = getattr(settings, 'CACHE_TTL_AI_CONTEXT', 1800)
    await cache.set(f"swot_v2:{ticker.upper()}:{period_key or 'latest'}", result, ttl)
    return result

async def get_fundamental_report(ticker: str, period_key: Optional[str], db: D1Client, env) -> dict:
    builder = AIContextBuilder(db)
    result = await builder.build_fundamental_report(ticker, period_key)
    if isinstance(result, tuple):
        return result
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    ttl = getattr(settings, 'CACHE_TTL_AI_CONTEXT', 1800)
    await cache.set(f"report_v2:{ticker.upper()}:{period_key or 'latest'}", result, ttl)
    return result

async def get_sector_context(sector_name: str, period_key: Optional[str], db: D1Client, env) -> dict:
    builder = SectorContextBuilder(db)
    result = await builder.build(sector_name, period_key or "TTM")
    if isinstance(result, tuple):
        return result
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    ttl = getattr(settings, 'CACHE_TTL_AI_CONTEXT', 1800)
    await cache.set(f"sector_context:{sector_name}:{period_key or 'TTM'}", result, ttl)
    return result

async def get_compare_context(data: dict, db: D1Client, env) -> dict:
    tickers = data.get("tickers", [])
    period_key = data.get("period_key", "TTM")
    builder = CompareBuilder(db)
    result = await builder.build(tickers, period_key)
    if isinstance(result, tuple):
        return result
    cache = KVCache(env.TEMEL_CACHE)
    from config import settings
    ttl = getattr(settings, 'CACHE_TTL_AI_CONTEXT', 1800)
    await cache.set(f"compare_context:{'-'.join(sorted(tickers))}:{period_key}", result, ttl)
    return result
