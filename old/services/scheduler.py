"""
HissePro Scheduler Service
Manages automated data fetching with three-layer scheduling system

Author: Kiro AI Assistant
"""

import asyncio
import logging
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_async_db, get_db
from services.isyatirim_client import isyatirim_client
from services.ratio_calculator import RatioCalculator

logger = logging.getLogger(__name__)


class SchedulerService:
    """
    Three-layer scheduling system for automated data fetching:
    
    Layer 1: Daily intensive scan (07:00 TSI) - KAP reporting window companies
    Layer 2: Weekly full scan (Sunday 04:00 TSI) - All active companies  
    Layer 3: Manual triggers (Admin UI) - On-demand fetching
    """
    
    def __init__(self):
        # APScheduler configuration
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': AsyncIOExecutor()
        }
        job_defaults = {
            'coalesce': True,
            'max_instances': 1,
            'misfire_grace_time': 300  # 5 minutes
        }
        
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=settings.SCHEDULER_TIMEZONE
        )
        
        self._running = False
        self._stats = {
            "total_fetches": 0,
            "successful_fetches": 0,
            "failed_fetches": 0,
            "last_run": None,
            "current_job": None
        }

    async def start(self):
        """Start the scheduler with all jobs"""
        if self._running:
            logger.warning("Scheduler already running")
            return
        
        try:
            # Layer 1: Daily intensive scan during KAP reporting window
            self.scheduler.add_job(
                func=self._layer1_intensive_scan,
                trigger=CronTrigger(hour=7, minute=0),  # 07:00 TSI
                id='layer1_daily_intensive',
                name='Layer 1: Daily KAP Window Scan',
                replace_existing=True
            )
            
            # Layer 2: Weekly full scan (safety net)
            self.scheduler.add_job(
                func=self._layer2_full_scan,
                trigger=CronTrigger(day_of_week=6, hour=4, minute=0),  # Sunday 04:00 TSI
                id='layer2_weekly_full',
                name='Layer 2: Weekly Full Scan',
                replace_existing=True
            )
            
            # Performance monitoring job
            self.scheduler.add_job(
                func=self._performance_monitor,
                trigger=CronTrigger(minute='*/30'),  # Every 30 minutes
                id='performance_monitor',
                name='Performance Monitor',
                replace_existing=True
            )
            
            self.scheduler.start()
            self._running = True
            logger.info("✅ Scheduler started with 3-layer system")
            
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            raise

    async def stop(self):
        """Stop the scheduler gracefully"""
        if not self._running:
            return
        
        try:
            self.scheduler.shutdown(wait=True)
            self._running = False
            logger.info("✅ Scheduler stopped gracefully")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")

    async def trigger_manual_fetch(
        self, 
        tickers: Optional[List[str]] = None,
        sector: Optional[str] = None,
        priority: bool = False
    ) -> Dict[str, Any]:
        """
        Layer 3: Manual fetch trigger (Admin UI)
        
        Args:
            tickers: Specific company tickers to fetch
            sector: All companies in sector
            priority: Skip rate limiting for urgent updates
        """
        try:
            self._stats["current_job"] = "Manual Fetch"
            
            # Determine target companies
            if tickers:
                target_companies = tickers
                scope = f"Companies: {', '.join(tickers[:5])}{'...' if len(tickers) > 5 else ''}"
            elif sector:
                async with get_async_db() as db:
                    from models.company import Company
                    from sqlalchemy import select
                    
                    query = select(Company.ticker).where(
                        Company.sector_main == sector,
                        Company.is_active == True
                    )
                    result = await db.execute(query)
                    target_companies = [row.ticker for row in result.fetchall()]
                    scope = f"Sector: {sector} ({len(target_companies)} companies)"
            else:
                raise ValueError("Either tickers or sector must be specified")
            
            logger.info(f"🚀 Manual fetch triggered - {scope}")
            
            # Execute fetch with optional priority
            results = await self._fetch_companies(
                target_companies, 
                priority=priority,
                job_name="Manual"
            )
            
            return {
                "status": "completed",
                "scope": scope,
                "total_companies": len(target_companies),
                "successful_fetches": results["successful"],
                "failed_fetches": results["failed"],
                "duration_seconds": results["duration"],
                "new_data_count": results["new_data_count"]
            }
            
        except Exception as e:
            logger.error(f"Manual fetch failed: {e}", exc_info=True)
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        finally:
            self._stats["current_job"] = None

    async def _layer1_intensive_scan(self):
        """
        Layer 1: Daily scan for companies in KAP reporting window
        
        Targets companies that should be releasing financial statements
        based on quarter end + 75 days window
        """
        try:
            self._stats["current_job"] = "Layer 1: Intensive Scan"
            logger.info("🔍 Layer 1: Starting intensive scan for KAP reporting window")
            
            # Get companies in reporting window
            target_companies = await self._get_reporting_window_companies()
            
            if not target_companies:
                logger.info("📊 Layer 1: No companies in current reporting window")
                return
            
            logger.info(f"📊 Layer 1: Scanning {len(target_companies)} companies in reporting window")
            
            # Execute fetch
            results = await self._fetch_companies(
                target_companies,
                job_name="Layer 1"
            )
            
            logger.info(f"✅ Layer 1 completed - {results['successful']} successful, {results['failed']} failed")
            
        except Exception as e:
            logger.error(f"Layer 1 intensive scan failed: {e}", exc_info=True)
            self._stats["failed_fetches"] += 1
        finally:
            self._stats["current_job"] = None
            self._stats["last_run"] = datetime.utcnow()

    async def _layer2_full_scan(self):
        """
        Layer 2: Weekly full scan of all active companies (safety net)
        
        Catches any companies missed by Layer 1 or irregular reporting
        """
        try:
            self._stats["current_job"] = "Layer 2: Full Scan"
            logger.info("🌊 Layer 2: Starting weekly full scan (safety net)")
            
            async with get_async_db() as db:
                from models.company import Company
                from sqlalchemy import select
                
                # Get all active companies
                query = select(Company.ticker).where(Company.is_active == True)
                result = await db.execute(query)
                all_companies = [row.ticker for row in result.fetchall()]
            
            logger.info(f"🌊 Layer 2: Scanning {len(all_companies)} active companies")
            
            # Execute fetch
            results = await self._fetch_companies(
                all_companies,
                job_name="Layer 2"
            )
            
            logger.info(f"✅ Layer 2 completed - {results['successful']} successful, {results['failed']} failed")
            
        except Exception as e:
            logger.error(f"Layer 2 full scan failed: {e}", exc_info=True)
            self._stats["failed_fetches"] += 1
        finally:
            self._stats["current_job"] = None
            self._stats["last_run"] = datetime.utcnow()

    async def _get_reporting_window_companies(self) -> List[str]:
        """
        Get companies that should be in current KAP reporting window
        
        KAP Reporting Windows:
        - Q1 (March): April & May
        - Q2 (June): July & August  
        - Q3 (September): October & November
        - Q4 (December): January - March (longest window)
        """
        today = date.today()
        month = today.month
        
        # Determine if we're in a reporting window
        in_window = False
        
        if month in [1, 2, 3]:  # Q4 reporting window (longest)
            in_window = True
            window_type = "Q4 Annual Reports"
        elif month in [4, 5]:  # Q1 reporting window
            in_window = True
            window_type = "Q1 Reports"
        elif month in [7, 8]:  # Q2 reporting window
            in_window = True
            window_type = "Q2 Reports"
        elif month in [10, 11]:  # Q3 reporting window
            in_window = True
            window_type = "Q3 Reports"
        
        if not in_window:
            logger.info(f"📅 Not in KAP reporting window (month {month})")
            return []
        
        logger.info(f"📅 In KAP reporting window: {window_type}")
        
        # For now, return all active companies during reporting windows
        # TODO: Implement more sophisticated logic based on company-specific patterns
        async with get_async_db() as db:
            from models.company import Company
            from sqlalchemy import select
            
            query = select(Company.ticker).where(Company.is_active == True)
            result = await db.execute(query)
            return [row.ticker for row in result.fetchall()]

    async def _fetch_companies(
        self, 
        tickers: List[str], 
        priority: bool = False,
        job_name: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Execute fetching for a list of companies with diff-based optimization
        
        Args:
            tickers: List of company tickers
            priority: Skip rate limiting if True
            job_name: Job name for logging
        """
        start_time = datetime.utcnow()
        successful = 0
        failed = 0
        new_data_count = 0
        
        try:
            # Process companies in batches
            batch_size = settings.ISYATIRIM_BATCH_SIZE
            
            for i in range(0, len(tickers), batch_size):
                batch = tickers[i:i + batch_size]
                logger.info(f"📦 {job_name}: Processing batch {i//batch_size + 1} ({len(batch)} companies)")
                
                # Process batch
                batch_results = await asyncio.gather(
                    *[self._fetch_single_company(ticker, priority) for ticker in batch],
                    return_exceptions=True
                )
                
                # Count results
                for result in batch_results:
                    if isinstance(result, Exception):
                        failed += 1
                        logger.error(f"❌ Fetch failed: {result}")
                    elif result and result.get("is_new_data"):
                        successful += 1
                        new_data_count += 1
                        logger.debug(f"✅ New data: {result['ticker']}")
                    elif result:
                        successful += 1
                        logger.debug(f"📊 No change: {result['ticker']}")
                    else:
                        failed += 1
                
                # Session break between batches (unless priority)
                if not priority and i + batch_size < len(tickers):
                    logger.debug(f"😴 Session break: {settings.ISYATIRIM_SESSION_BREAK} seconds")
                    await asyncio.sleep(settings.ISYATIRIM_SESSION_BREAK)
            
        except Exception as e:
            logger.error(f"Fetch execution failed: {e}", exc_info=True)
            failed += len(tickers) - successful
        
        # Update stats
        self._stats["total_fetches"] += len(tickers)
        self._stats["successful_fetches"] += successful
        self._stats["failed_fetches"] += failed
        
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "successful": successful,
            "failed": failed,
            "new_data_count": new_data_count,
            "duration": duration
        }

    async def _fetch_single_company(self, ticker: str, priority: bool = False) -> Optional[Dict[str, Any]]:
        """Fetch mali tablo data for a single company with diff checking and DB persistence"""
        try:
            # Get current period parameters
            periods = self._get_current_periods()
            
            # Fetch with diff check (includes raw data)
            result = await isyatirim_client.fetch_with_diff_check(
                ticker, 
                periods,
                priority=priority
            )
            
            if not result or "data" not in result:
                return result
                
            # Perform DB operations with diff optimization
            from models.financial import FetchLog, FinancialStatementRaw
            from sqlalchemy import select, and_
            from sqlalchemy.dialects.postgresql import insert as pg_insert
            import json
            
            ticker = ticker.upper().strip()
            period_key = result["period_key"]
            new_checksum = result["checksum"]
            financial_group = result["financial_group"]
            
            async with get_async_db() as db:
                # Find last checksum in database
                stmt = select(FetchLog.checksum_md5).where(
                    and_(
                        FetchLog.ticker == ticker,
                        FetchLog.period_key == period_key
                    )
                ).order_by(FetchLog.fetched_at.desc()).limit(1)
                
                db_res = await db.execute(stmt)
                last_checksum = db_res.scalar_one_or_none()
                
                # Check if data is actually new
                is_new = (last_checksum is None) or (last_checksum != new_checksum)
                result["is_new_data"] = is_new
                
                fetched_at = datetime.utcnow()
                
                if is_new:
                    logger.info(f"✨ New financial data detected for {ticker} (Checksum: {new_checksum})")
                    items = result["data"].get("value", [])
                    insert_values = []
                    
                    # Map year and period tuples from periods list
                    periods_tuples = [(p["year"], p["period"]) for p in periods]
                    
                    for item in items:
                        item_code = item.get("itemCode")
                        item_desc_tr = item.get("itemDescTr")
                        item_desc_en = item.get("itemDescEng")
                        
                        for idx, (year, period) in enumerate(periods_tuples, 1):
                            val_key = f"value{idx}"
                            val_str = item.get(val_key)
                            
                            if val_str is None:
                                continue
                            
                            try:
                                # Parse float value from API representation (e.g. "123456" or format string)
                                val_clean = val_str.strip().replace(".", "").replace(",", ".") if isinstance(val_str, str) else str(val_str)
                                value_try = float(val_clean) if val_clean else 0.0
                            except ValueError:
                                value_try = None
                            
                            p_key = f"{year}Q{period//3 if period != 12 else 4}"
                            
                            insert_values.append({
                                "ticker": ticker,
                                "period_key": p_key,
                                "year": year,
                                "period": period,
                                "financial_group": financial_group,
                                "item_code": item_code,
                                "item_desc_tr": item_desc_tr,
                                "item_desc_en": item_desc_en,
                                "value_try": value_try,
                                "fetched_at": fetched_at
                            })
                    
                    if insert_values:
                        stmt_upsert = pg_insert(FinancialStatementRaw).values(insert_values)
                        stmt_upsert = stmt_upsert.on_conflict_do_update(
                            constraint="uq_statements_ticker_period_item",
                            set_={
                                "value_try": stmt_upsert.excluded.value_try,
                                "fetched_at": stmt_upsert.excluded.fetched_at,
                                "item_desc_tr": stmt_upsert.excluded.item_desc_tr,
                                "item_desc_en": stmt_upsert.excluded.item_desc_en
                            }
                        )
                        await db.execute(stmt_upsert)
                        logger.debug(f"💾 Persisted {len(insert_values)} statement entries for {ticker}")
                
                else:
                    logger.debug(f"😴 Checksum matches ({new_checksum}). Skipping persistence for {ticker}")
                
                # Always create a FetchLog entry to document the check
                log_entry = FetchLog(
                    ticker=ticker,
                    period_key=period_key,
                    fetched_at=fetched_at,
                    http_status=result.get("http_status"),
                    response_size=len(json.dumps(result["data"])) if result.get("data") else 0,
                    processing_time_ms=result.get("response_time_ms"),
                    checksum_md5=new_checksum,
                    is_new_data=is_new,
                    error_message=result.get("error")
                )
                db.add(log_entry)
                await db.commit()
            
            # Asynchronously trigger ratio calculations ONLY if data is new!
            if result.get("is_new_data"):
                asyncio.create_task(self._trigger_ratio_calculation(ticker, result["period_key"]))
                
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch {ticker}: {e}", exc_info=True)
            return None

    async def _trigger_ratio_calculation(self, ticker: str, period_key: str):
        """Trigger ratio calculation for updated company data using sync SessionLocal"""
        try:
            from core.database import SessionLocal
            with SessionLocal() as db:
                calculator = RatioCalculator(db)
                await calculator.calculate_company_ratios(ticker, period_key)
                logger.debug(f"✅ Ratios calculated: {ticker} {period_key}")
        except Exception as e:
            logger.error(f"Ratio calculation failed for {ticker}: {e}")

    def _get_current_periods(self) -> List[Dict[str, int]]:
        """Get current 4-quarter period parameters for API"""
        today = date.today()
        month = today.month
        year = today.year
        
        # Determine current reporting quarter with lag
        if month <= 5:       # Jan-May → Q4 previous year is latest
            current = (year-1, 12)
        elif month <= 8:     # Jun-Aug → Q1 current year
            current = (year, 3)
        elif month <= 11:    # Sep-Nov → Q2 current year
            current = (year, 6)
        else:                # Dec → Q3 current year
            current = (year, 9)
        
        periods = []
        y, p = current
        quarter_map = {12: 9, 9: 6, 6: 3, 3: 12}
        
        for i in range(1, 5):
            periods.append({"year": y, "period": p, "idx": i})
            prev_p = quarter_map[p]
            if prev_p == 12:
                y -= 1
            p = prev_p
        
        return periods

    async def _performance_monitor(self):
        """Monitor scheduler performance and log metrics"""
        try:
            jobs = self.scheduler.get_jobs()
            
            logger.info(f"📊 Scheduler Stats - Running Jobs: {len(jobs)}, "
                       f"Total Fetches: {self._stats['total_fetches']}, "
                       f"Success Rate: {self._stats['successful_fetches']/max(1, self._stats['total_fetches'])*100:.1f}%")
            
            # Log current job if any
            if self._stats["current_job"]:
                logger.info(f"🔄 Current Job: {self._stats['current_job']}")
                
        except Exception as e:
            logger.error(f"Performance monitoring failed: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get current scheduler status for admin UI"""
        return {
            "running": self._running,
            "stats": self._stats.copy(),
            "jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                    "trigger": str(job.trigger)
                }
                for job in self.scheduler.get_jobs()
            ] if self._running else []
        }

    async def reschedule_job(self, job_id: str, trigger_kwargs: Dict[str, Any]):
        """Reschedule a job with new trigger parameters"""
        if not self._running:
            raise RuntimeError("Scheduler not running")
        
        job = self.scheduler.get_job(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        self.scheduler.reschedule_job(job_id, trigger=CronTrigger(**trigger_kwargs))
        logger.info(f"✅ Job {job_id} rescheduled")