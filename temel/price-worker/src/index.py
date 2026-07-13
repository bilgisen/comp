import json
from workers import WorkerEntrypoint, Response


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        from js import Date, fetch as js_fetch

        t0 = Date.now()

        try:
            # Try HisseTekil with browser-like headers
            url = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse=ASELS"
            r1 = await js_fetch(url, {"method": "GET", "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Accept": "application/json,text/plain,*/*", "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"}})
            t1 = Date.now()
            if r1.status != 200:
                return Response.json({"status": r1.status, "body": "non-200", "elapsed_ms": round(t1 - t0)})
            b1 = await r1.text()
            return Response.json({"status": r1.status, "body": b1[:500], "elapsed_ms": round(t1 - t0)})
        except Exception as e:
            return Response.json({
                "error": str(e),
                "type": type(e).__name__,
                "elapsed": round(Date.now() - t0),
            }, status=500)
