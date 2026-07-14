"""
Calculate Industry-based Benchmarks
Uses new 21-28 industry classification for more accurate peer comparisons
"""

import logging
import asyncio
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal
from services.sector_benchmarks import SectorBenchmarkService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('industry_benchmark_calculation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def calculate_all_industry_benchmarks():
    """Calculate benchmarks for all industries"""
    logger.info("=" * 80)
    logger.info("INDUSTRY BENCHMARK CALCULATION STARTING")
    logger.info("=" * 80)
    
    start_time = datetime.utcnow()
    
    async with AsyncSessionLocal() as db:
        # Get all industry-period combinations
        query = text("""
            SELECT DISTINCT c.industry, cr.period_key
            FROM companies c
            JOIN company_ratios cr ON c.ticker = cr.ticker
            WHERE c.is_active = TRUE
              AND c.industry IS NOT NULL
            ORDER BY c.industry, cr.period_key DESC
        """)
        
        result = await db.execute(query)
        industry_periods = result.fetchall()
    
    logger.info(f"Found {len(industry_periods)} industry-period combinations")
    
    total_benchmarks = 0
    failed_industries = 0
    
    for industry, period_key in industry_periods:
        try:
            async with AsyncSessionLocal() as db:
                service = SectorBenchmarkService(db)
                
                # Use new industry parameter
                benchmarks = await service.compute_sector_benchmarks(
                    industry=industry,
                    period_key=period_key
                )
                
                total_benchmarks += len(benchmarks)
                
                logger.info(f"✅ Computed {len(benchmarks)} benchmarks for {industry} {period_key}")
        
        except Exception as e:
            logger.error(f"❌ Error computing benchmarks for {industry} {period_key}: {e}")
            failed_industries += 1
            continue
    
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds() / 60
    
    logger.info("=" * 80)
    logger.info("INDUSTRY BENCHMARK CALCULATION COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Duration: {duration:.1f} minutes")
    logger.info(f"Total benchmarks: {total_benchmarks}")
    logger.info(f"Failed industries: {failed_industries}")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(calculate_all_industry_benchmarks())
