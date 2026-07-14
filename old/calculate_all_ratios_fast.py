"""
Fast batch ratio calculation
Process companies in batches with progress tracking
"""
import logging
from datetime import datetime
from typing import List
from sqlalchemy import text

from core.database import SessionLocal
from models.financial import CompanyRatio, FinancialStatementRaw
from models.company import Company
from calculate_ratios_sync import SyncRatioCalculator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calculate_ratios_batch(tickers: List[str], batch_num: int, total_batches: int):
    """Calculate ratios for a batch of companies"""
    with SessionLocal() as db:
        calculator = SyncRatioCalculator(db)
        successful = 0
        failed = 0
        total_ratios = 0
        
        for ticker in tickers:
            try:
                # Get periods for this company
                periods = db.execute(text('''
                    SELECT DISTINCT period_key 
                    FROM financial_statements_raw 
                    WHERE ticker = :ticker
                    ORDER BY period_key DESC
                '''), {"ticker": ticker}).scalars().all()
                
                company_ratios = 0
                
                for period_key in periods:
                    try:
                        results = calculator.calculate_company_ratios(ticker, period_key)
                        
                        for result in results:
                            if result.success and result.value is not None:
                                # Upsert ratio
                                existing = db.query(CompanyRatio).filter(
                                    CompanyRatio.ticker == ticker,
                                    CompanyRatio.period_key == period_key,
                                    CompanyRatio.ratio_code == result.ratio_code
                                ).first()
                                
                                if existing:
                                    existing.ratio_value = result.value
                                    existing.calculation_method = result.calculation_method
                                    existing.data_quality_score = result.data_quality_score
                                    existing.computed_at = datetime.now()
                                else:
                                    ratio = CompanyRatio(
                                        ticker=ticker,
                                        period_key=period_key,
                                        ratio_code=result.ratio_code,
                                        ratio_value=result.value,
                                        is_ttm='ttm' in (result.calculation_method or '').lower(),
                                        calculation_method=result.calculation_method,
                                        data_quality_score=result.data_quality_score,
                                        computed_at=datetime.now()
                                    )
                                    db.add(ratio)
                                
                                company_ratios += 1
                                total_ratios += 1
                    
                    except Exception as e:
                        logger.error(f"Error calculating {ticker} {period_key}: {e}")
                        continue
                
                if company_ratios > 0:
                    successful += 1
                else:
                    failed += 1
                
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
                failed += 1
                continue
        
        db.commit()
        
        logger.info(f"Batch {batch_num}/{total_batches}: {successful} companies, {total_ratios} ratios")
        
        return successful, total_ratios


def main():
    """Main batch calculation"""
    logger.info("=" * 60)
    logger.info("FAST RATIO CALCULATION STARTING")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    
    # Clear existing ratios
    with SessionLocal() as db:
        db.execute(text("DELETE FROM company_ratios"))
        db.commit()
        logger.info("Cleared existing ratios")
    
    # Get all companies with financial data
    with SessionLocal() as db:
        tickers = db.execute(text('''
            SELECT DISTINCT ticker 
            FROM financial_statements_raw
            ORDER BY ticker
        ''')).scalars().all()
    
    total_companies = len(tickers)
    logger.info(f"Found {total_companies} companies")
    
    # Process in batches of 20
    batch_size = 20
    total_batches = (total_companies + batch_size - 1) // batch_size
    
    total_successful = 0
    total_ratios = 0
    
    for batch_idx in range(0, total_companies, batch_size):
        batch = tickers[batch_idx:batch_idx + batch_size]
        batch_num = batch_idx // batch_size + 1
        
        successful, ratios = calculate_ratios_batch(batch, batch_num, total_batches)
        total_successful += successful
        total_ratios += ratios
        
        # Progress
        progress = min(batch_idx + batch_size, total_companies)
        pct = progress / total_companies * 100
        logger.info(f"Progress: {progress}/{total_companies} ({pct:.1f}%) - {total_ratios} ratios calculated")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60
    
    logger.info("=" * 60)
    logger.info("RATIO CALCULATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Duration: {duration:.1f} minutes")
    logger.info(f"Companies processed: {total_successful}/{total_companies}")
    logger.info(f"Total ratios calculated: {total_ratios}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
