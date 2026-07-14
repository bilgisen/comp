"""
İş Yatırım API Client with rate limiting and error handling
"""

import asyncio
import hashlib
import json
import logging
import time
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

import httpx
from httpx import AsyncClient, Response

from core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class FetchResult:
    """Result of a fetch operation"""
    success: bool
    ticker: str
    period_key: str
    data: Optional[Dict[str, Any]] = None
    checksum: Optional[str] = None
    error: Optional[str] = None
    response_time_ms: Optional[int] = None
    http_status: Optional[int] = None


class RateLimiter:
    """Rate limiter for İş Yatırım API requests"""
    
    def __init__(self, requests_per_minute: int = 20, delay_between_requests: float = 3.0):
        self.requests_per_minute = requests_per_minute
        self.delay_between_requests = delay_between_requests
        self.request_times = []
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire permission to make a request"""
        async with self._lock:
            now = time.time()
            
            # Remove old requests (older than 1 minute)
            cutoff = now - 60
            self.request_times = [t for t in self.request_times if t > cutoff]
            
            # Check if we're at the limit
            if len(self.request_times) >= self.requests_per_minute:
                sleep_time = 60 - (now - self.request_times[0])
                if sleep_time > 0:
                    logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                    await asyncio.sleep(sleep_time)
            
            # Add jitter to delay (2.5-4.0 seconds for 3.0 base)
            jitter = 0.5
            actual_delay = self.delay_between_requests + (asyncio.get_event_loop().time() % (jitter * 2) - jitter)
            await asyncio.sleep(max(0, actual_delay))
            
            # Record this request
            self.request_times.append(time.time())


class IsYatirimClient:
    """İş Yatırım API client with professional error handling"""
    
    BASE_URL = "https://www.isyatirim.com.tr"
    MALI_TABLO_ENDPOINT = f"{BASE_URL}/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
    
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    def __init__(self):
        self.rate_limiter = RateLimiter(
            requests_per_minute=settings.ISYATIRIM_RATE_LIMIT,
            delay_between_requests=settings.ISYATIRIM_DELAY
        )
        self.client: Optional[AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
    
    async def connect(self):
        """Initialize HTTP client"""
        if self.client is None:
            self.client = AsyncClient(
                timeout=httpx.Timeout(settings.ISYATIRIM_TIMEOUT),
                headers={
                    "User-Agent": self.USER_AGENT,
                    "Accept": "application/json,text/plain,*/*",
                    "Referer": f"{self.BASE_URL}/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx",
                    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache"
                },
                follow_redirects=True
            )
            logger.info("✅ İş Yatırım API client initialized")
    
    async def disconnect(self):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None
            logger.info("✅ İş Yatırım API client closed")
    
    def _get_periods_to_fetch(self, reference_date: Optional[date] = None) -> List[Tuple[int, int]]:
        """
        Calculate 4 periods to fetch based on reporting lag
        Returns list of (year, period) tuples
        """
        if reference_date is None:
            reference_date = date.today()
        
        month = reference_date.month
        year = reference_date.year
        
        # Account for reporting lag (companies report 45-75 days after period end)
        if month <= 5:       # Jan-May → Q4 previous year is latest
            current = (year - 1, 12)
        elif month <= 8:     # Jun-Aug → Q1 current year is latest
            current = (year, 3)
        elif month <= 11:    # Sep-Nov → Q2 current year is latest
            current = (year, 6)
        else:                # Dec → Q3 current year is latest
            current = (year, 9)
        
        # Build 4 consecutive quarters going backwards
        periods = []
        y, p = current
        quarter_sequence = {12: 9, 9: 6, 6: 3, 3: 12}
        
        for i in range(4):
            periods.append((y, p))
            prev_p = quarter_sequence[p]
            if prev_p == 12:  # Going from Q1 to Q4 of previous year
                y -= 1
            p = prev_p
        
        return periods
    
    def _normalize_currency(self, currency: str) -> str:
        """Normalize currency code"""
        cur = (currency or "TRY").strip().upper()
        return "TRY" if cur in ["TL", "TRY"] else cur
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate MD5 checksum of response data"""
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    async def fetch_mali_tablo(
        self,
        ticker: str,
        currency: str = "TRY",
        financial_group: str = "XI_29",
        periods: Optional[List[Tuple[int, int]]] = None
    ) -> FetchResult:
        """
        Fetch mali tablo for a company
        
        Args:
            ticker: Company ticker (e.g., 'THYAO')
            currency: Currency code ('TRY' or 'USD')
            financial_group: Financial group ('UFRS_K', 'XI_29', etc.)
            periods: List of (year, period) tuples. If None, auto-calculated.
        
        Returns:
            FetchResult with data or error
        """
        if not self.client:
            await self.connect()
        
        ticker = ticker.upper().strip()
        currency = self._normalize_currency(currency)
        
        if periods is None:
            periods = self._get_periods_to_fetch()
        
        if len(periods) != 4:
            return FetchResult(
                success=False,
                ticker=ticker,
                period_key="unknown",
                error="Exactly 4 periods required"
            )
        
        # Rate limiting
        await self.rate_limiter.acquire()
        
        # Build request parameters
        params = {
            "companyCode": ticker,
            "exchange": currency,
            "financialGroup": financial_group,
            "_": int(time.time() * 1000)  # Cache busting timestamp
        }
        
        # Add period parameters
        for i, (year, period) in enumerate(periods, 1):
            params[f"year{i}"] = year
            params[f"period{i}"] = period
        
        period_key = f"{periods[0][0]}Q{periods[0][1]//3 if periods[0][1] != 12 else 4}"
        
        start_time = time.time()
        
        try:
            logger.info(f"📥 Fetching {ticker} mali tablo for periods {periods}")
            
            response: Response = await self.client.get(
                self.MALI_TABLO_ENDPOINT,
                params=params
            )
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Check HTTP status
            if response.status_code != 200:
                return FetchResult(
                    success=False,
                    ticker=ticker,
                    period_key=period_key,
                    error=f"HTTP {response.status_code}: {response.text[:200]}",
                    response_time_ms=response_time_ms,
                    http_status=response.status_code
                )
            
            # Parse JSON
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                return FetchResult(
                    success=False,
                    ticker=ticker,
                    period_key=period_key,
                    error=f"Invalid JSON response: {str(e)}",
                    response_time_ms=response_time_ms,
                    http_status=response.status_code
                )
            
            # Validate response structure
            if not isinstance(data, dict):
                return FetchResult(
                    success=False,
                    ticker=ticker,
                    period_key=period_key,
                    error="Response is not a JSON object",
                    response_time_ms=response_time_ms,
                    http_status=response.status_code
                )
            
            # Check for API errors
            if not data.get("ok", True):
                error_msg = data.get("message", "Unknown API error")
                return FetchResult(
                    success=False,
                    ticker=ticker,
                    period_key=period_key,
                    error=f"API Error: {error_msg}",
                    response_time_ms=response_time_ms,
                    http_status=response.status_code
                )
            
            # Validate data content
            items = data.get("value", [])
            if not isinstance(items, list):
                return FetchResult(
                    success=False,
                    ticker=ticker,
                    period_key=period_key,
                    error="Response 'value' is not a list",
                    response_time_ms=response_time_ms,
                    http_status=response.status_code
                )
            
            if len(items) == 0:
                logger.warning(f"⚠️ Empty response for {ticker} - no financial data available")
            
            checksum = self._calculate_checksum(data)
            
            logger.info(f"✅ Successfully fetched {ticker}: {len(items)} items, {response_time_ms}ms")
            
            return FetchResult(
                success=True,
                ticker=ticker,
                period_key=period_key,
                data=data,
                checksum=checksum,
                response_time_ms=response_time_ms,
                http_status=response.status_code
            )
            
        except httpx.TimeoutException:
            return FetchResult(
                success=False,
                ticker=ticker,
                period_key=period_key,
                error="Request timeout",
                response_time_ms=int((time.time() - start_time) * 1000)
            )
            
        except httpx.NetworkError as e:
            return FetchResult(
                success=False,
                ticker=ticker,
                period_key=period_key,
                error=f"Network error: {str(e)}",
                response_time_ms=int((time.time() - start_time) * 1000)
            )
            
        except Exception as e:
            logger.error(f"❌ Unexpected error fetching {ticker}: {e}", exc_info=True)
            return FetchResult(
                success=False,
                ticker=ticker,
                period_key=period_key,
                error=f"Unexpected error: {str(e)}",
                response_time_ms=int((time.time() - start_time) * 1000)
            )
    
    async def fetch_with_diff_check(
        self,
        ticker: str,
        periods: List[Dict[str, int]],
        priority: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch with diff check for scheduler integration
        
        Args:
            ticker: Company ticker
            periods: List of period dictionaries with year/period keys
            priority: Skip normal rate limiting if True
            
        Returns:
            Dict with ticker, is_new_data, checksum or None if failed
        """
        try:
            # Convert periods format
            period_tuples = [(p["year"], p["period"]) for p in periods]
            
            # Determine financial group (simplified logic)
            # TODO: Get from company metadata in database
            financial_group = "UFRS_K" if ticker in ["GARAN", "YKBNK", "AKBNK", "HALKB"] else "XI_29"
            
            # Override rate limiting for priority fetches
            if priority and self.rate_limiter:
                original_delay = self.rate_limiter.delay_between_requests
                self.rate_limiter.delay_between_requests = 0.5  # Faster for priority
            
            # Fetch data
            result = await self.fetch_mali_tablo(
                ticker=ticker,
                financial_group=financial_group,
                periods=period_tuples
            )
            
            # Restore original delay
            if priority and self.rate_limiter:
                self.rate_limiter.delay_between_requests = original_delay
            
            if not result.success:
                logger.error(f"Failed to fetch {ticker}: {result.error}")
                return None
            
            # Return rich response data so scheduler can handle DB operations
            return {
                "ticker": ticker,
                "is_new_data": True,
                "checksum": result.checksum,
                "period_key": result.period_key,
                "row_count": len(result.data.get("value", [])) if result.data else 0,
                "data": result.data,
                "financial_group": financial_group,
                "http_status": result.http_status,
                "response_time_ms": result.response_time_ms,
                "error": result.error
            }
            
        except Exception as e:
            logger.error(f"Fetch with diff check failed for {ticker}: {e}")
            return None
    
    async def fetch_multiple_companies(
        self,
        tickers: List[str],
        currency: str = "TRY",
        batch_size: Optional[int] = None
    ) -> List[FetchResult]:
        """
        Fetch mali tablo for multiple companies with batching
        
        Args:
            tickers: List of company tickers
            currency: Currency code
            batch_size: Override default batch size
            
        Returns:
            List of FetchResults
        """
        if batch_size is None:
            batch_size = settings.ISYATIRIM_BATCH_SIZE
        
        results = []
        
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]
            logger.info(f"📦 Processing batch {i//batch_size + 1}: {len(batch)} companies")
            
            # Process batch
            batch_results = []
            for ticker in batch:
                result = await self.fetch_mali_tablo(ticker, currency)
                batch_results.append(result)
            
            results.extend(batch_results)
            
            # Session break between batches (except for last batch)
            if i + batch_size < len(tickers):
                logger.info("⏸️ Taking session break...")
                await asyncio.sleep(120)  # 2 minute break
        
        success_count = sum(1 for r in results if r.success)
        logger.info(f"📊 Batch complete: {success_count}/{len(results)} successful")
        
        return results


# Global client instance
isyatirim_client = IsYatirimClient()