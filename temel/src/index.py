from workers import WorkerEntrypoint, Response

from config import init_settings
from db.client import D1Client
from routers import health
from routers.companies import (
    list_companies, get_company_profile, get_statements, get_ratios,
    get_trends, get_sectors, search_companies, get_financial_summary, calculate_ratios
)
from routers.analysis import (
    get_ai_context, get_temel_analiz, get_swot, get_fundamental_report
)


def parse_params(request):
    url = request.url
    qs = url.split("?", 1)[1] if "?" in url else ""
    params = {}
    if qs:
        for pair in qs.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k] = v
    return params


def get_path(request):
    url = request.url.split("?")[0]
    parts = url.split("/")
    return "/" + "/".join(parts[3:]).rstrip("/")


def parts_from_path(path):
    return [p for p in path.split("/") if p]


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        init_settings(self.env)
        db = D1Client(self.env.TEMEL_DB)
        method = request.method.upper()

        if method == "OPTIONS":
            return Response.new("", status=204)

        path = get_path(request)
        parts = parts_from_path(path)
        params = parse_params(request)

        def qp(key, default=None):
            return params.get(key, default)

        if path == "/health":
            return Response.json(health.health_handler())
        if path == "/":
            return Response.json(health.root_handler())

        if len(parts) >= 3 and parts[0] == "api" and parts[1] == "v1":
            resource = parts[2]
            if resource == "sectors" and len(parts) == 3:
                data, status = await get_sectors(db)
                return Response.json(data, status=status)
            if resource == "companies":
                if len(parts) == 3:
                    return Response.json(await list_companies(qp("page", "1"), qp("limit", "50"), qp("sector"), db))
                if len(parts) == 4 and parts[3] == "search":
                    res = await search_companies(qp("q", ""), db)
                    if isinstance(res, tuple):
                        return Response.json(res[0], status=res[1])
                    return Response.json(res)
                if len(parts) >= 4:
                    ticker = parts[3].upper()
                    sub = parts[4] if len(parts) > 4 else ""
                    if sub == "profile":
                        data, status = await get_company_profile(ticker, db)
                    elif sub == "statements":
                        data, status = await get_statements(ticker, qp("period"), db)
                    elif sub == "ratios":
                        data, status = await get_ratios(ticker, qp("period"), qp("ratios"), db)
                    elif sub == "trends":
                        data, status = await get_trends(ticker, qp("periods", "8"), qp("ratios"), db)
                    elif sub == "summary":
                        data, status = await get_financial_summary(ticker, qp("period"), db)
                    elif sub == "calculate":
                        data, status = await calculate_ratios(ticker, qp("period"), db, self.env)
                    elif sub == "":
                        data, status = await get_company_profile(ticker, db)
                    else:
                        return Response.json({"error": f"Unknown endpoint: {sub}"}, status=404)
                    return Response.json(data, status=status)
            if resource == "ai" and len(parts) >= 5:
                ai_type = parts[3]
                ticker = parts[4].upper()
                ai_map = {
                    "context": lambda: get_ai_context(ticker, qp("type", "basic"), qp("period"), qp("force", "false"), db, self.env),
                    "analysis": lambda: get_temel_analiz(ticker, qp("period"), db, self.env),
                    "swot": lambda: get_swot(ticker, qp("period"), db, self.env),
                    "fundamental-report": lambda: get_fundamental_report(ticker, qp("period"), db, self.env),
                }
                if ai_type in ai_map:
                    result = await ai_map[ai_type]()
                    data, status = result if isinstance(result, tuple) else (result, 200)
                    return Response.json(data, status=status)
                return Response.json({"error": f"Unknown AI type: {ai_type}"}, status=404)

        return Response.json({"error": "Not found"}, status=404)
