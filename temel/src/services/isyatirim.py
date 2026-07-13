import json
import hashlib
import time
from typing import Optional, List, Tuple
from urllib.parse import urlencode

class IsYatirimClient:
    BASE_URL = "https://www.isyatirim.com.tr"
    MALI_TABLO_ENDPOINT = f"{BASE_URL}/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"

    def __init__(self, settings):
        self.settings = settings
        self._last_request_time = 0
        self._request_timestamps = []

    def _get_periods_to_fetch(self) -> List[Tuple[int, int]]:
        import datetime
        now = datetime.datetime.now()
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
        quarter_sequence = {12: 9, 9: 6, 6: 3, 3: 12}
        for _ in range(4):
            periods.append((y, p))
            prev_p = quarter_sequence[p]
            if prev_p == 12:
                y -= 1
            p = prev_p
        return periods

    def _calculate_checksum(self, data: dict) -> str:
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(json_str.encode()).hexdigest()

    async def _rate_limit(self):
        now = time.time()
        cutoff = now - 60
        self._request_timestamps = [t for t in self._request_timestamps if t > cutoff]
        if len(self._request_timestamps) >= self.settings.ISYATIRIM_RATE_LIMIT:
            sleep_time = 60 - (now - self._request_timestamps[0])
            if sleep_time > 0:
                import asyncio
                await asyncio.sleep(sleep_time)
        elapsed = now - self._last_request_time
        if elapsed < self.settings.ISYATIRIM_DELAY:
            import asyncio
            await asyncio.sleep(self.settings.ISYATIRIM_DELAY - elapsed)
        self._last_request_time = time.time()
        self._request_timestamps.append(time.time())

    async def fetch_mali_tablo(self, ticker: str, financial_group: str = "XI_29",
                                periods: Optional[List[Tuple[int, int]]] = None) -> dict:
        await self._rate_limit()
        if periods is None:
            periods = self._get_periods_to_fetch()
        params = {
            "companyCode": ticker.upper(),
            "exchange": "TRY",
            "financialGroup": financial_group,
            "_": int(time.time() * 1000)
        }
        for i, (year, period) in enumerate(periods, 1):
            params[f"year{i}"] = year
            params[f"period{i}"] = period
        url = f"{self.MALI_TABLO_ENDPOINT}?{urlencode(params)}"
        period_key = f"{periods[0][0]}Q{periods[0][1] // 3 if periods[0][1] != 12 else 4}"
        start = time.time()
        try:
            import js
            response = await js.fetch(url, {
                "method": "GET",
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json,text/plain,*/*",
                    "Referer": f"{self.BASE_URL}/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx",
                    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"
                }
            })
            response_time = int((time.time() - start) * 1000)
            if response.status != 200:
                text = await response.text()
                return {"success": False, "ticker": ticker, "period_key": period_key,
                        "error": f"HTTP {response.status}", "response_time_ms": response_time,
                        "http_status": response.status}
            text = await response.text()
            data = json.loads(text)
            if not data.get("ok", True):
                return {"success": False, "ticker": ticker, "period_key": period_key,
                        "error": data.get("message", "API Error"), "response_time_ms": response_time}
            items = data.get("value", [])
            checksum = self._calculate_checksum(data)
            return {"success": True, "ticker": ticker, "period_key": period_key,
                    "data": data, "checksum": checksum, "response_time_ms": response_time,
                    "items": items, "row_count": len(items)}
        except Exception as e:
            return {"success": False, "ticker": ticker, "period_key": period_key,
                    "error": str(e), "response_time_ms": int((time.time() - start) * 1000)}
