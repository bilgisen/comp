"""Recalculate benchmarks for Banking & Finance sector only"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from calculate_benchmarks_sync import SyncBenchmarkCalculator
from core.config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sync_db_url = settings.database_url.replace('postgresql+asyncpg://', 'postgresql://')
engine = create_engine(sync_db_url)
SessionLocal = sessionmaker(bind=engine)

logger.info("=" * 60)
logger.info("RECALCULATING BANKING SECTOR BENCHMARKS")
logger.info("=" * 60)

sector = "Bankacılık & Finans"
periods = ["2026Q1", "2025Q4", "2025Q3", "2025Q2"]

for period in periods:
    logger.info(f"\nProcessing: {sector} {period}")
    
    with SessionLocal() as db:
        calculator = SyncBenchmarkCalculator(db)
        benchmarks = calculator.compute_sector_benchmarks(sector, period)
        
        logger.info(f"✅ Computed {len(benchmarks)} benchmarks for {sector} {period}")
        
        # Show sample benchmarks
        for bm in benchmarks:
            if bm.ratio_code in ['roa', 'roe']:
                logger.info(f"   {bm.ratio_code}: median={bm.median_ew*100:.2f}%, n_peers={bm.n_peers}, reliability={bm.reliability}")

logger.info("\n" + "=" * 60)
logger.info("✅ Banking sector benchmarks recalculated successfully!")
logger.info("=" * 60)
