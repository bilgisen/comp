"""Calculate ratios and scores for yatırım ortaklıkları"""
import asyncio
import logging
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.company import Company
from models.financial import CompanyRatio
from models.score import CompanyScore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_yatirim_scores():
    """Calculate scores for yatırım ortaklıkları using SQL-based approach"""
    
    db = SessionLocal()
    try:
        # Get yatırım ortaklıkları
        companies = db.query(Company).filter(
            Company.industry == 'Yatırım Ortaklıkları',
            Company.is_active == True,
            Company.financial_group == 'XI_29'
        ).all()
        
        logger.info(f"Found {len(companies)} yatırım ortaklıkları")
        
        # Calculate ratios using fast SQL method
        logger.info("\n📊 Step 1: Calculating ratios...")
        
        # Run the fast SQL ratio calculator
        from subprocess import run, PIPE
        result = run(
            ['python', 'calculate_ratios_sql.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            logger.error(f"Ratio calculation failed: {result.stderr}")
            return
        
        logger.info(f"✅ Ratios calculated:\n{result.stdout}")
        
        # Calculate benchmarks
        logger.info("\n📊 Step 2: Calculating benchmarks...")
        result = run(
            ['python', 'calculate_benchmarks_sync.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            logger.error(f"Benchmark calculation failed: {result.stderr}")
            return
        
        logger.info(f"✅ Benchmarks calculated:\n{result.stdout}")
        
        # Verify results
        logger.info("\n📊 Step 3: Verifying results...")
        
        for company in companies[:5]:  # Check first 5
            ticker = company.ticker
            
            # Check ratios
            ratio_count = db.query(CompanyRatio).filter(
                CompanyRatio.ticker == ticker
            ).count()
            
            # Check scores
            score = db.query(CompanyScore).filter(
                CompanyScore.ticker == ticker
            ).order_by(CompanyScore.period_key.desc()).first()
            
            score_value = score.score_genel if score else None
            
            logger.info(f"  {ticker:8} Ratios: {ratio_count:3d}  Score: {score_value or 'NULL'}")
        
        logger.info("\n✅ All done! Check a few companies on the frontend.")
        
    finally:
        db.close()


if __name__ == "__main__":
    calculate_yatirim_scores()
