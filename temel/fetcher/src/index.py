import json
import hashlib
import time
from datetime import datetime, timezone
from workers import WorkerEntrypoint, Response


def is_in_kap_window(month):
    return month in [1, 2, 3, 4, 5, 7, 8, 10, 11]


def get_window_label(month):
    labels = {1: "Q4-Annual", 2: "Q4-Annual", 3: "Q4-Annual",
              4: "Q1", 5: "Q1", 7: "Q2", 8: "Q2",
              10: "Q3", 11: "Q3"}
    return labels.get(month, "Off-Window")


def get_periods_to_fetch(now=None):
    if now is None:
        now = datetime.now(timezone.utc)
    month = now.month
    year = now.year
    if month <= 5:
        current = (year - 1, 12)
    elif month <= 8:
        current = (year, 3)
    elif month <= 11:
        current = (year, 6)
    else:
        current = (year, 9)
    periods = []
    y, p = current
    qmap = {12: 9, 9: 6, 6: 3, 3: 12}
    for _ in range(4):
        periods.append((y, p))
        prev = qmap[p]
        if prev == 12:
            y -= 1
        p = prev
    return periods


def period_key_str(year, period):
    q = period // 3 if period != 12 else 4
    return f"{year}Q{q}"


def parse_items(items, ticker, financial_group, periods):
    parsed = []
    period_keys = {}
    for i, (y, p) in enumerate(periods):
        period_keys[str(i + 1)] = (period_key_str(y, p), y, p)
    for item in items:
        code = item.get("kod", item.get("itemCode", ""))
        desc_tr = item.get("aciklama1", item.get("itemDescTr", ""))
        desc_en = item.get("itemDescEng", "")
        for key, (pk, y, p) in period_keys.items():
            val_key = f"valueTutar{key}" if f"valueTutar{key}" in item else f"value{key}"
            val = item.get(val_key)
            if val is not None:
                try:
                    clean = str(val).strip().replace(".", "").replace(",", ".")
                    v = float(clean) if clean else None
                except ValueError:
                    v = None
                parsed.append({
                    "period_key": pk, "year": y, "period": p,
                    "financial_group": financial_group, "item_code": code,
                    "item_desc_tr": desc_tr, "item_desc_en": desc_en, "value_try": v
                })
    return parsed


class RateLimiter:
    def __init__(self, max_per_minute=20, delay=3.0):
        self.max_per_minute = max_per_minute
        self.delay = delay
        self.timestamps = []
        self.last_request = 0

    async def wait(self, priority=False):
        import asyncio
        now = time.time()
        cutoff = now - 60
        self.timestamps = [t for t in self.timestamps if t > cutoff]
        if not priority and len(self.timestamps) >= self.max_per_minute:
            sleep_time = 60 - (now - self.timestamps[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        elapsed = now - self.last_request
        actual_delay = self.delay * 0.5 if priority else self.delay
        if elapsed < actual_delay:
            await asyncio.sleep(actual_delay - elapsed)
        self.last_request = time.time()
        self.timestamps.append(time.time())


ratelimiter = RateLimiter()


async def fetch_mali_tablo(ticker, financial_group, settings, js_fetch, periods=None):
    if periods is None:
        periods = get_periods_to_fetch()
    pk = period_key_str(periods[0][0], periods[0][1])
    start = time.time()
    try:
        await ratelimiter.wait()
        base = settings["ISYATIRIM_BASE_URL"]
        url = base + "/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode=" + ticker.upper() + "&exchange=TRY&financialGroup=" + financial_group
        for i, (y, p) in enumerate(periods, 1):
            url = url + "&year" + str(i) + "=" + str(y) + "&period" + str(i) + "=" + str(p)
        resp = await js_fetch(url, {"method": "GET"})
        rtime = int((time.time() - start) * 1000)
        if resp.status != 200:
            return {"success": False, "ticker": ticker, "period_key": pk, "error": "HTTP", "response_time_ms": rtime, "http_status": resp.status}
        text = await resp.text()
        data = json.loads(text)
        if not data.get("ok", True):
            return {"success": False, "ticker": ticker, "period_key": pk, "error": data.get("message"), "response_time_ms": rtime, "http_status": 200}
        items = data.get("value", [])
        checksum = hashlib.md5(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()
        parsed = parse_items(items, ticker, financial_group, periods)
        return {"success": True, "ticker": ticker, "period_key": pk, "items": parsed, "checksum": checksum, "response_time_ms": rtime, "response_size": len(text), "http_status": 200}
    except Exception as e:
        return {"success": False, "ticker": ticker, "period_key": pk, "error": str(e), "response_time_ms": int((time.time() - start) * 1000), "http_status": 0}


async def fetch_short_table(ticker, settings, js_fetch):
    await ratelimiter.wait()
    periods = get_periods_to_fetch()
    y, p = periods[0]
    params = {
        "companyCode": ticker.upper(),
        "exchange": "TRY",
        "year1": y,
        "period1": p,
        "_": int(time.time() * 1000)
    }
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{settings['ISYATIRIM_BASE_URL']}/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTabloShortTable?{query}"
    pk = period_key_str(y, p)
    try:
        resp = await js_fetch(url, {
            "method": "GET",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json,text/plain,*/*",
                "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"
            }
        })
        if resp.status != 200:
            return {"success": False, "ticker": ticker, "period_key": pk, "error": f"HTTP {resp.status}"}
        text = await resp.text()
        data = json.loads(text)
        if not data.get("ok", True):
            return {"success": False, "ticker": ticker, "period_key": pk, "error": data.get("message", "API Error")}
        items = data.get("value", [])
        values = {}
        for item in items:
            code = item.get("kod", item.get("itemCode", ""))
            val = item.get("valueTutar1", item.get("value1"))
            if val is not None:
                try:
                    clean = str(val).strip().replace(".", "").replace(",", ".")
                    values[code] = float(clean)
                except ValueError:
                    pass
        return {"success": True, "ticker": ticker, "period_key": pk,
                "equity": values.get("2O"), "paid_capital": values.get("2OA"),
                "net_income": values.get("3Z")}
    except Exception as e:
        return {"success": False, "ticker": ticker, "period_key": pk, "error": str(e)}


async def get_companies_for_fetch(db, window_only=False):
    d1 = await db.prepare("SELECT ticker, financial_group FROM companies WHERE is_active = 1 ORDER BY market_cap DESC").all()
    return [dict(r) for r in d1.results]


async def get_existing_checksum(db, ticker, period_key):
    stmt = db.prepare("SELECT checksum_md5 FROM fetch_logs WHERE ticker = ? AND period_key = ? ORDER BY fetched_at DESC LIMIT 1")
    d1 = await stmt.bind(ticker, period_key).all()
    return d1.results[0]["checksum_md5"] if d1.results else None


async def save_statements(db, statements):
    if not statements:
        return
    fetched_at = datetime.now(timezone.utc).isoformat()
    for s in statements:
        try:
            stmt = db.prepare("""
                INSERT OR REPLACE INTO financial_statements_raw
                (ticker, period_key, year, period, financial_group, item_code, item_desc_tr, item_desc_en, value_try, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """)
            await stmt.bind(s["ticker"], s["period_key"], s["year"], s["period"],
                           s["financial_group"], s["item_code"],
                           s.get("item_desc_tr"), s.get("item_desc_en"),
                           s.get("value_try"), fetched_at).run()
        except Exception:
            pass


async def save_fetch_log(db, ticker, period_key, checksum, is_new, http_status, response_time_ms, response_size, error=None):
    try:
        stmt = db.prepare("""
            INSERT INTO fetch_logs (ticker, period_key, fetched_at, http_status, response_size, processing_time_ms, checksum_md5, is_new_data, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)
        await stmt.bind(ticker, period_key, datetime.now(timezone.utc).isoformat(),
                        http_status, response_size, response_time_ms,
                        checksum, 1 if is_new else 0, error).run()
    except Exception:
        pass


async def save_short_summary(db, ticker, period_key, equity, paid_capital, net_income):
    try:
        stmt = db.prepare("""
            INSERT OR REPLACE INTO company_financial_summary (ticker, period_key, equity, paid_capital, net_income, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        await stmt.bind(ticker, period_key, equity, paid_capital, net_income,
                        datetime.now(timezone.utc).isoformat()).run()
    except Exception:
        pass


async def invalidate_cache(cache, ticker):
    try:
        await cache.delete(f"company:{ticker}")
    except Exception:
        pass


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        if request.method.upper() != "POST":
            return Response.json({"error": "Only POST allowed"}, status=403)
        return await self._run_batch()

    async def scheduled(self, event):
        try:
            await self._run_batch()
        except Exception as e:
            print(json.dumps({"msg": "scheduled_error", "error": str(e), "type": type(e).__name__}))

    async def _run_batch(self):
        try:
            db = self.env.TEMEL_DB
            cache = self.env.TEMEL_CACHE

            settings = {"ISYATIRIM_BASE_URL": "https://www.isyatirim.com.tr"}

            companies = await get_companies_for_fetch(db)
            ticker_list = [c["ticker"] for c in companies]
            fin_map = {c["ticker"]: c.get("financial_group", "XI_29") for c in companies}

            cursor_val = await cache.get("fetch:cursor")
            start = int(cursor_val) if cursor_val is not None else 0
            if start >= len(ticker_list):
                start = 0

            from js import fetch as js_fetch
            results = []
            session_start = time.time()
            max_wall = 25
            batch_size = 10

            for i in range(start, min(start + batch_size, len(ticker_list))):
                if time.time() - session_start >= max_wall:
                    break
                ticker = ticker_list[i]
                fin_group = fin_map.get(ticker, "XI_29")
                try:
                    result = await fetch_mali_tablo(ticker, fin_group, settings, js_fetch)
                    if result["success"] and result.get("items"):
                        items = result["items"]
                        await save_statements(db, items)
                        pk = result["period_key"]
                        eq = next((s["value_try"] for s in items if s["item_code"] == "2O"), None)
                        pc = next((s["value_try"] for s in items if s["item_code"] == "2OA"), None)
                        ni = next((s["value_try"] for s in items if s["item_code"] == "3Z"), None)
                        await save_short_summary(db, ticker, pk, eq, pc, ni)
                        await invalidate_cache(cache, ticker)
                    await save_fetch_log(db, ticker, result.get("period_key", ""),
                                         result.get("checksum", ""), len(result.get("items", [])) > 0,
                                         result.get("http_status", 0), result.get("response_time_ms", 0),
                                         result.get("response_size", 0))
                    results.append({"ticker": ticker, "ok": result["success"], "items": len(result.get("items", []))})
                except Exception as e:
                    results.append({"ticker": ticker, "ok": False, "error": str(e)})

            next_idx = start + len(results)
            if next_idx >= len(ticker_list):
                await cache.delete("fetch:cursor")
            else:
                await cache.put("fetch:cursor", str(next_idx))

            return Response.json({
                "processed": len(results),
                "cursor": next_idx if next_idx < len(ticker_list) else 0,
                "total": len(ticker_list),
                "results": results
            })
        except Exception as e:
            return Response.json({"error": str(e), "type": type(e).__name__}, status=500)
