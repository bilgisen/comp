"""Fetch financial data for yatırım ortaklıkları with XI_29 financial group"""
import asyncio
import logging
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.database import get_async_db, SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw
from services.isyatirim_client import isyatirim_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_yatirim_data():
    """Fetch financial statements for yatırım ortaklıkları"""
    
    # Get yatırım ortaklıkları
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(
            Company.industry == 'Yatırım Ortaklıkları',
            Company.is_active == True,
            Company.financial_group == 'XI_29'
        ).all()
        
        logger.info(f"Found {len(companies)} yatırım ortaklıkları to process")
        
        # Fetch periods to get
        periods = [
            (2026, 3),
            (2025, 12),
            (2025, 9),
            (2025, 6),
        ]
        
        success_count = 0
        error_count = 0
        
        for company in companies:
            ticker = company.ticker
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing {ticker} - {company.name}")
            
            try:
                # Check if already exists
                existing = db.query(FinancialStatementRaw).filter(
                    FinancialStatementRaw.ticker == ticker,
                    FinancialStatementRaw.period_key == '2026Q1',
                    FinancialStatementRaw.financial_group == 'XI_29'
                ).first()
                
                if existing:
                    logger.info(f"  ⏭️  Data already exists for {ticker}, skipping...")
                    success_count += 1
                    continue
                
                # Fetch from İş Yatırım
                result = await isyatirim_client.fetch_mali_tablo(
                    ticker=ticker,
                    financial_group='XI_29',
                    currency='TRY',
                    periods=periods
                )
                
                if not result.success or result.error:
                    logger.warning(f"  ❌ Failed to fetch {ticker}: {result.error or 'Unknown error'}")
                    error_count += 1
                    continue
                
                # Parse and save data
                item_count = 0
                items = result.data.get('value', [])  # API returns items in 'value' key
                logger.info(f"  📊 Processing {len(items)} items...")
                
                for item in items:
                    item_code = item.get('itemCode')
                    if not item_code:
                        continue
                    
                    # Save for each period
                    for idx, (year, period) in enumerate(periods, start=1):
                        value_key = f'value{idx}'
                        value = item.get(value_key)
                        
                        if value is None or value == '' or value == '0':
                            continue
                        
                        try:
                            # Handle string values with thousand separators
                            if isinstance(value, str):
                                value = value.replace(',', '').replace('.', '')
                                if not value or value == '0':
                                    continue
                            value_numeric = float(value)
                        except (ValueError, AttributeError) as e:
                            logger.debug(f"    ⚠️  Could not parse value for {item_code}: {value}")
                            continue
                        
                        period_key = f"{year}Q{period//3}"
                        
                        statement = FinancialStatementRaw(
                            ticker=ticker,
                            period_key=period_key,
                            year=year,
                            period=period,
                            financial_group='XI_29',
                            item_code=item_code,
                            item_desc_tr=item.get('itemDescTr'),
                            item_desc_en=item.get('itemDescEng'),
                            value_try=value_numeric,
                            fetched_at=datetime.utcnow()
                        )
                        
                        db.add(statement)
                        item_count += 1
                
                db.commit()
                logger.info(f"  ✅ Saved {item_count} items for {ticker}")
                success_count += 1
                
                # Rate limiting
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"  ❌ Error processing {ticker}: {e}", exc_info=True)
                db.rollback()
                error_count += 1
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Completed: {success_count} successful, {error_count} errors")
        logger.info(f"{'='*60}\n")
        
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(fetch_yatirim_data())
