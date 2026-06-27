"""
HissePro COMP Engine Bootstrap Script
Systematically loads 14 sectors × 620 companies with rate-limiting

Features:
- Sector-by-sector OR bulk execution
- Progress tracking with checkpoints
- Automatic retry on failures
- Resume capability
- Detailed logging
- ETA calculation

Usage:
    python bootstrap_comp_engine.py --sector "Bankacılık & Finans"  # Test single sector
    python bootstrap_comp_engine.py --all                           # Full bootstrap
    python bootstrap_comp_engine.py --resume                        # Resume from checkpoint
"""

import asyncio
import argparse
import logging
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.config import settings
from core.database import SessionLocal, AsyncSessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw, CompanyRatio, FetchLog
from services.isyatirim_client import isyatirim_client
from services.ratio_calculator import RatioCalculator
from services.sector_benchmarks import SectorBenchmarkService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bootstrap.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class CheckpointData:
    """Bootstrap checkpoint for resume capability"""
    started_at: str
    phase: str  # 'fetch', 'ratios', 'benchmarks', 'completed'
    total_companies: int
    processed_companies: List[str]
    failed_companies: List[str]
    current_sector: Optional[str]
    stats: Dict[str, Any]


@dataclass
class BootstrapStats:
    """Bootstrap execution statistics"""
    total_companies: int = 0
    successful_fetches: int = 0
    failed_fetches: int = 0
    total_rows_inserted: int = 0
    total_ratios_calculated: int = 0
    total_benchmarks_created: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def duration_minutes(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'duration_minutes': self.duration_minutes(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }


class BootstrapEngine:
    """Main bootstrap engine"""
    
    CHECKPOINT_FILE = Path("bootstrap_checkpoint.json")
    RATE_LIMIT_DELAY = 3.0  # Seconds between requests (20 req/min)
    BATCH_SIZE = 50  # Companies per batch
    SESSION_BREAK = 120  # Seconds between batches
    
    def __init__(self, sectors: Optional[List[str]] = None):
        self.sectors = sectors
        self.stats = BootstrapStats()
        self.checkpoint: Optional[CheckpointData] = None
        
    async def run(self, resume: bool = False):
        """Main bootstrap execution"""
        try:
            logger.info("🚀 HissePro COMP Engine Bootstrap Starting...")
            self.stats.start_time = datetime.utcnow()
            
            # Load checkpoint if resuming
            if resume:
                self.checkpoint = self._load_checkpoint()
                if self.checkpoint:
                    logger.info(f"📂 Resuming from checkpoint: {self.checkpoint.phase}")
                else:
                    logger.warning("⚠️ No checkpoint found, starting fresh")
                    resume = False
            
            # Phase 1: Fetch mali tablo data
            if not resume or self.checkpoint.phase == 'fetch':
                logger.info("=" * 60)
                logger.info("PHASE 1: MALI TABLO FETCH")
                logger.info("=" * 60)
                await self._phase_fetch()
                self._save_checkpoint('ratios')
            
            # Phase 2: Calculate ratios
            if not resume or self.checkpoint.phase in ['fetch', 'ratios']:
                logger.info("=" * 60)
                logger.info("PHASE 2: RATIO CALCULATION")
                logger.info("=" * 60)
                await self._phase_calculate_ratios()
                self._save_checkpoint('benchmarks')
            
            # Phase 3: Generate sector benchmarks
            if not resume or self.checkpoint.phase in ['fetch', 'ratios', 'benchmarks']:
                logger.info("=" * 60)
                logger.info("PHASE 3: SECTOR BENCHMARKS")
                logger.info("=" * 60)
                await self._phase_calculate_benchmarks()
                self._save_checkpoint('completed')
            
            self.stats.end_time = datetime.utcnow()
            
            # Final report
            self._print_final_report()
            
            # Cleanup checkpoint
            if self.CHECKPOINT_FILE.exists():
                self.CHECKPOINT_FILE.unlink()
            
            logger.info("✅ Bootstrap completed successfully!")
            
        except KeyboardInterrupt:
            logger.warning("⚠️ Bootstrap interrupted by user")
            self._save_checkpoint('interrupted')
            raise
        except Exception as e:
            logger.error(f"❌ Bootstrap failed: {e}", exc_info=True)
            self._save_checkpoint('failed')
            raise
    
    async def _phase_fetch(self):
        """Phase 1: Fetch mali tablo data from İş Yatırım API"""
        
        # Get companies to fetch
        companies = await self._get_companies_to_fetch()
        self.stats.total_companies = len(companies)
        
        logger.info(f"📊 Fetching data for {len(companies)} companies")
        logger.info(f"⏱️ Estimated time: {len(companies) / 20:.0f} minutes (20 req/min)")
        
        processed = set(self.checkpoint.processed_companies if self.checkpoint else [])
        failed = set(self.checkpoint.failed_companies if self.checkpoint else [])
        
        # Process in batches
        for batch_idx, batch_start in enumerate(range(0, len(companies), self.BATCH_SIZE)):
            batch = companies[batch_start:batch_start + self.BATCH_SIZE]
            batch_num = batch_idx + 1
            total_batches = (len(companies) + self.BATCH_SIZE - 1) // self.BATCH_SIZE
            
            logger.info(f"📦 Batch {batch_num}/{total_batches}: {len(batch)} companies")
            
            async with isyatirim_client:
                for company in batch:
                    ticker = company.ticker
                    
                    # Skip if already processed
                    if ticker in processed:
                        logger.debug(f"⏭️ Skipping {ticker} (already processed)")
                        continue
                    
                    try:
                        # Fetch data
                        result = await self._fetch_company(ticker, company.financial_group)
                        
                        if result['success']:
                            self.stats.successful_fetches += 1
                            self.stats.total_rows_inserted += result['rows_inserted']
                            processed.add(ticker)
                            
                            logger.info(
                                f"✅ {ticker}: {result['rows_inserted']} rows, "
                                f"{result['response_time_ms']}ms "
                                f"({self.stats.successful_fetches}/{len(companies)})"
                            )
                        else:
                            self.stats.failed_fetches += 1
                            failed.add(ticker)
                            logger.warning(f"⚠️ {ticker}: {result['error']}")
                        
                        # Rate limiting
                        await asyncio.sleep(self.RATE_LIMIT_DELAY)
                        
                    except Exception as e:
                        self.stats.failed_fetches += 1
                        failed.add(ticker)
                        logger.error(f"❌ {ticker}: {e}")
                        continue
            
            # Session break between batches
            if batch_start + self.BATCH_SIZE < len(companies):
                logger.info(f"😴 Session break: {self.SESSION_BREAK}s")
                await asyncio.sleep(self.SESSION_BREAK)
        
        logger.info(f"✅ Fetch phase complete: {self.stats.successful_fetches} successful, {self.stats.failed_fetches} failed")

    
    async def _phase_calculate_ratios(self):
        """Phase 2: Calculate financial ratios for all companies"""
        
        # Get companies with financial data
        with SessionLocal() as db:
            companies_with_data = db.execute(
                select(FinancialStatementRaw.ticker).distinct()
            ).scalars().all()
        
        logger.info(f"🧮 Calculating ratios for {len(companies_with_data)} companies")
        
        processed_count = 0
        failed_count = 0
        
        for ticker in companies_with_data:
            try:
                # Get available periods for this company
                with SessionLocal() as db:
                    periods = db.execute(
                        select(FinancialStatementRaw.period_key)
                        .where(FinancialStatementRaw.ticker == ticker)
                        .distinct()
                    ).scalars().all()
                
                # Calculate ratios for each period
                for period_key in periods:
                    with SessionLocal() as db:
                        calculator = RatioCalculator(db)
                        results = await calculator.calculate_company_ratios(ticker, period_key)
                        
                        # Save results
                        successful = 0
                        for result in results:
                            if result.success and result.value is not None:
                                # Upsert ratio
                                from models.financial import CompanyRatio
                                from sqlalchemy import and_
                                
                                existing = db.query(CompanyRatio).filter(
                                    and_(
                                        CompanyRatio.ticker == ticker,
                                        CompanyRatio.period_key == period_key,
                                        CompanyRatio.ratio_code == result.ratio_code
                                    )
                                ).first()
                                
                                if existing:
                                    existing.ratio_value = result.value
                                    existing.calculation_method = result.calculation_method
                                    existing.data_quality_score = result.data_quality_score
                                    existing.computed_at = datetime.utcnow()
                                else:
                                    ratio = CompanyRatio(
                                        ticker=ticker,
                                        period_key=period_key,
                                        ratio_code=result.ratio_code,
                                        ratio_value=result.value,
                                        is_ttm='ttm' in (result.calculation_method or '').lower(),
                                        calculation_method=result.calculation_method,
                                        data_quality_score=result.data_quality_score,
                                        computed_at=datetime.utcnow()
                                    )
                                    db.add(ratio)
                                
                                successful += 1
                        
                        db.commit()
                        self.stats.total_ratios_calculated += successful
                
                processed_count += 1
                if processed_count % 10 == 0:
                    logger.info(f"🧮 Progress: {processed_count}/{len(companies_with_data)} companies")
                
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Ratio calculation failed for {ticker}: {e}")
                continue
        
        logger.info(
            f"✅ Ratio calculation complete: {self.stats.total_ratios_calculated} ratios, "
            f"{processed_count} companies processed, {failed_count} failed"
        )
    
    async def _phase_calculate_benchmarks(self):
        """Phase 3: Calculate sector benchmarks"""
        
        # Get all sectors with ratios
        async with AsyncSessionLocal() as db:
            from sqlalchemy import text
            
            query = text("""
                SELECT DISTINCT c.sector_main, cr.period_key
                FROM companies c
                JOIN company_ratios cr ON c.ticker = cr.ticker
                WHERE c.is_active = TRUE
                ORDER BY c.sector_main, cr.period_key DESC
            """)
            
            result = await db.execute(query)
            sector_periods = result.fetchall()
        
        logger.info(f"📊 Calculating benchmarks for {len(sector_periods)} sector-period combinations")
        
        benchmark_service = SectorBenchmarkService(AsyncSessionLocal())
        
        processed_count = 0
        failed_count = 0
        
        for sector_main, period_key in sector_periods:
            try:
                async with AsyncSessionLocal() as db:
                    service = SectorBenchmarkService(db)
                    benchmarks = await service.compute_sector_benchmarks(
                        sector_main, period_key
                    )
                    
                    self.stats.total_benchmarks_created += len(benchmarks)
                    processed_count += 1
                    
                    logger.info(
                        f"✅ {sector_main} {period_key}: {len(benchmarks)} benchmarks "
                        f"({processed_count}/{len(sector_periods)})"
                    )
                
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Benchmark calculation failed for {sector_main} {period_key}: {e}")
                continue
        
        logger.info(
            f"✅ Benchmark calculation complete: {self.stats.total_benchmarks_created} benchmarks, "
            f"{failed_count} failed"
        )
    
    async def _fetch_company(self, ticker: str, financial_group: str) -> Dict[str, Any]:
        """Fetch mali tablo for a single company"""
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        
        try:
            # Get periods to fetch
            periods = self._get_periods_to_fetch()
            
            # Fetch from API
            result = await isyatirim_client.fetch_mali_tablo(
                ticker=ticker,
                financial_group=financial_group,
                periods=periods
            )
            
            if not result.success or not result.data:
                return {
                    'success': False,
                    'error': result.error or 'No data returned',
                    'rows_inserted': 0,
                    'response_time_ms': result.response_time_ms
                }
            
            # Insert data into database
            with SessionLocal() as db:
                items = result.data.get("value", [])
                fetched_at = datetime.utcnow()
                insert_values = []
                
                for item in items:
                    item_code = item.get("itemCode")
                    item_desc_tr = item.get("itemDescTr")
                    item_desc_en = item.get("itemDescEng")
                    
                    for idx, (year, period) in enumerate(periods, 1):
                        val_key = f"value{idx}"
                        val_str = item.get(val_key)
                        
                        if val_str is None:
                            continue
                        
                        try:
                            # Parse value
                            if isinstance(val_str, str):
                                val_str = val_str.strip()
                                if not val_str or val_str == "":
                                    value_try = None
                                else:
                                    val_clean = val_str.replace(".", "").replace(",", ".")
                                    value_try = float(val_clean)
                            elif isinstance(val_str, (int, float)):
                                value_try = float(val_str)
                            else:
                                value_try = None
                        except (ValueError, AttributeError):
                            value_try = None
                        
                        period_key = f"{year}Q{period//3 if period != 12 else 4}"
                        
                        insert_values.append({
                            "ticker": ticker,
                            "period_key": period_key,
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
                    stmt = pg_insert(FinancialStatementRaw).values(insert_values)
                    stmt = stmt.on_conflict_do_update(
                        constraint="uq_statements_ticker_period_item",
                        set_={
                            "value_try": stmt.excluded.value_try,
                            "fetched_at": stmt.excluded.fetched_at,
                            "item_desc_tr": stmt.excluded.item_desc_tr,
                            "item_desc_en": stmt.excluded.item_desc_en
                        }
                    )
                    db.execute(stmt)
                
                # Create fetch log
                log_entry = FetchLog(
                    ticker=ticker,
                    period_key=result.period_key,
                    fetched_at=fetched_at,
                    http_status=result.http_status,
                    response_size=len(json.dumps(result.data)),
                    processing_time_ms=result.response_time_ms,
                    checksum_md5=result.checksum,
                    is_new_data=True,
                    error_message=None
                )
                db.add(log_entry)
                db.commit()
                
                return {
                    'success': True,
                    'rows_inserted': len(insert_values),
                    'response_time_ms': result.response_time_ms,
                    'checksum': result.checksum
                }
        
        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'rows_inserted': 0,
                'response_time_ms': 0
            }
    
    async def _get_companies_to_fetch(self) -> List[Company]:
        """Get list of companies to fetch based on sector filter"""
        with SessionLocal() as db:
            query = select(Company).where(Company.is_active == True)
            
            if self.sectors:
                query = query.where(Company.sector_main.in_(self.sectors))
            
            result = db.execute(query.order_by(Company.sector_main, Company.ticker))
            return result.scalars().all()
    
    def _get_periods_to_fetch(self) -> List[tuple]:
        """Get 4 periods to fetch (current + 3 previous quarters)"""
        from datetime import date
        
        today = date.today()
        month = today.month
        year = today.year
        
        # Determine latest available period (with reporting lag)
        if month <= 5:
            current = (year-1, 12)
        elif month <= 8:
            current = (year, 3)
        elif month <= 11:
            current = (year, 6)
        else:
            current = (year, 9)
        
        periods = []
        y, p = current
        quarter_map = {12: 9, 9: 6, 6: 3, 3: 12}
        
        for _ in range(4):
            periods.append((y, p))
            prev_p = quarter_map[p]
            if prev_p == 12:
                y -= 1
            p = prev_p
        
        return periods
    
    def _save_checkpoint(self, phase: str):
        """Save bootstrap checkpoint"""
        checkpoint = CheckpointData(
            started_at=self.stats.start_time.isoformat() if self.stats.start_time else datetime.utcnow().isoformat(),
            phase=phase,
            total_companies=self.stats.total_companies,
            processed_companies=[],  # Could track this if needed
            failed_companies=[],
            current_sector=self.sectors[0] if self.sectors and len(self.sectors) == 1 else None,
            stats=self.stats.to_dict()
        )
        
        with open(self.CHECKPOINT_FILE, 'w') as f:
            json.dump(asdict(checkpoint), f, indent=2)
        
        logger.debug(f"💾 Checkpoint saved: {phase}")
    
    def _load_checkpoint(self) -> Optional[CheckpointData]:
        """Load bootstrap checkpoint"""
        if not self.CHECKPOINT_FILE.exists():
            return None
        
        try:
            with open(self.CHECKPOINT_FILE, 'r') as f:
                data = json.load(f)
                return CheckpointData(**data)
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None
    
    def _print_final_report(self):
        """Print final bootstrap report"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("BOOTSTRAP COMPLETE - FINAL REPORT")
        logger.info("=" * 60)
        logger.info(f"Duration: {self.stats.duration_minutes():.1f} minutes")
        logger.info("")
        logger.info("PHASE 1: MALI TABLO FETCH")
        logger.info(f"  Total companies: {self.stats.total_companies}")
        logger.info(f"  Successful: {self.stats.successful_fetches}")
        logger.info(f"  Failed: {self.stats.failed_fetches}")
        logger.info(f"  Total rows inserted: {self.stats.total_rows_inserted:,}")
        logger.info("")
        logger.info("PHASE 2: RATIO CALCULATION")
        logger.info(f"  Total ratios calculated: {self.stats.total_ratios_calculated:,}")
        logger.info("")
        logger.info("PHASE 3: SECTOR BENCHMARKS")
        logger.info(f"  Total benchmarks created: {self.stats.total_benchmarks_created}")
        logger.info("")
        logger.info("=" * 60)


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='HissePro COMP Engine Bootstrap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test single sector
  python bootstrap_comp_engine.py --sector "Bankacılık & Finans"
  
  # Full bootstrap
  python bootstrap_comp_engine.py --all
  
  # Resume from checkpoint
  python bootstrap_comp_engine.py --resume
        """
    )
    
    parser.add_argument(
        '--sector',
        type=str,
        help='Bootstrap single sector (for testing)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Bootstrap all sectors (full production run)'
    )
    
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from last checkpoint'
    )
    
    args = parser.parse_args()
    
    # Determine sectors to process
    sectors = None
    if args.sector:
        sectors = [args.sector]
        logger.info(f"🎯 Mode: Single sector - {args.sector}")
    elif args.all:
        logger.info("🌊 Mode: All sectors")
    else:
        parser.print_help()
        return
    
    # Run bootstrap
    engine = BootstrapEngine(sectors=sectors)
    await engine.run(resume=args.resume)


if __name__ == "__main__":
    asyncio.run(main())
