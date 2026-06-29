"""
Create Score Tables
Creates company_scores, company_score_details, and global_benchmarks tables
"""

import sys
import logging
from sqlalchemy import text

from core.database import SessionLocal, engine
from models.score import CompanyScore, CompanyScoreDetail, GlobalBenchmark
from models.company import Company
from models.financial import CompanyRatio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    """Create score tables in database"""
    logger.info("Creating score tables...")
    
    # Create tables using SQLAlchemy models
    from core.database import Base
    Base.metadata.create_all(bind=engine)
    
    logger.info("✅ Tables created successfully")
    
    # Verify tables exist
    db = SessionLocal()
    try:
        # Check if tables exist by querying
        db.execute(text("SELECT 1 FROM company_scores LIMIT 1"))
        logger.info("✅ company_scores table exists")
    except Exception as e:
        logger.info(f"company_scores table will be created on first use: {e}")
    finally:
        db.close()


def check_data_availability():
    """Check if we have data to compute scores"""
    db = SessionLocal()
    try:
        # Check companies
        company_count = db.execute(text("SELECT COUNT(*) FROM companies WHERE is_active = TRUE")).scalar()
        logger.info(f"Active companies: {company_count}")
        
        # Check ratios
        ratio_count = db.execute(text("SELECT COUNT(*) FROM company_ratios")).scalar()
        logger.info(f"Total ratios: {ratio_count}")
        
        # Check periods
        periods = db.execute(text("""
            SELECT period_key, COUNT(DISTINCT ticker) as companies
            FROM company_ratios
            GROUP BY period_key
            ORDER BY period_key DESC
            LIMIT 5
        """)).fetchall()
        
        logger.info("Available periods:")
        for row in periods:
            logger.info(f"  {row.period_key}: {row.companies} companies")
        
        # Check benchmarks
        benchmark_count = db.execute(text("SELECT COUNT(*) FROM sector_benchmarks WHERE is_stale = FALSE")).scalar()
        logger.info(f"Sector benchmarks: {benchmark_count}")
        
        return company_count > 0 and ratio_count > 0
        
    finally:
        db.close()


def run_initial_scoring():
    """Run scoring for the latest period"""
    logger.info("\n" + "="*50)
    logger.info("Running initial scoring...")
    logger.info("="*50)
    
    from services.scoring.worker import ScoringWorker
    
    db = SessionLocal()
    try:
        worker = ScoringWorker(db)
        
        # Get latest period
        latest_period = db.execute(text("""
            SELECT MAX(period_key) FROM company_ratios
        """)).scalar()
        
        if not latest_period:
            logger.error("No periods found in company_ratios")
            return
        
        logger.info(f"Scoring period: {latest_period}")
        
        results = worker.run_scoring_for_period(latest_period)
        
        logger.info("\n" + "="*50)
        logger.info("SCORING RESULTS")
        logger.info("="*50)
        logger.info(f"Success: {results['success']}")
        logger.info(f"Failed: {results['failed']}")
        logger.info(f"Skipped: {results['skipped']}")
        
        if results['errors']:
            logger.info("\nErrors:")
            for err in results['errors'][:10]:
                logger.info(f"  {err}")
        
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create score tables and run initial scoring")
    parser.add_argument("--create-tables", action="store_true", help="Only create tables")
    parser.add_argument("--check-data", action="store_true", help="Check data availability")
    parser.add_argument("--score", action="store_true", help="Run initial scoring")
    args = parser.parse_args()
    
    if args.create_tables:
        create_tables()
    elif args.check_data:
        check_data_availability()
    elif args.score:
        run_initial_scoring()
    else:
        # Run all
        create_tables()
        if check_data_availability():
            run_initial_scoring()
