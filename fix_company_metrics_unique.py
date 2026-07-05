"""Add unique constraint to company_metrics.ticker"""
import logging
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_company_metrics_unique():
    """Add unique constraint to ticker column"""
    
    with SessionLocal() as db:
        logger.info("="*60)
        logger.info("FIX COMPANY_METRICS UNIQUE CONSTRAINT")
        logger.info("="*60)
        
        try:
            # Check for duplicates first
            logger.info("\n1. Checking for duplicate tickers...")
            dupes = db.execute(text("""
                SELECT ticker, COUNT(*) as count
                FROM company_metrics
                GROUP BY ticker
                HAVING COUNT(*) > 1
            """)).fetchall()
            
            if len(dupes) > 0:
                logger.warning(f"  Found {len(dupes)} duplicate tickers, removing...")
                for dup in dupes:
                    logger.info(f"    {dup.ticker}: {dup.count} rows")
                    # Keep only the most recent
                    db.execute(text("""
                        DELETE FROM company_metrics
                        WHERE id NOT IN (
                            SELECT MAX(id)
                            FROM company_metrics
                            WHERE ticker = :ticker
                        ) AND ticker = :ticker
                    """), {"ticker": dup.ticker})
                db.commit()
                logger.info("  ✅ Duplicates removed")
            else:
                logger.info("  ✅ No duplicates found")
            
            # Drop existing index if it's not unique
            logger.info("\n2. Dropping non-unique index...")
            try:
                db.execute(text("DROP INDEX IF EXISTS ix_company_metrics_ticker"))
                db.commit()
                logger.info("  ✅ Index dropped")
            except Exception as e:
                logger.info(f"  Index already dropped or doesn't exist: {e}")
            
            # Add unique constraint
            logger.info("\n3. Adding unique constraint...")
            db.execute(text("""
                ALTER TABLE company_metrics
                ADD CONSTRAINT company_metrics_ticker_unique UNIQUE (ticker)
            """))
            db.commit()
            logger.info("  ✅ Unique constraint added")
            
            # Verify
            logger.info("\n4. Verifying constraint...")
            result = db.execute(text("""
                SELECT conname, contype
                FROM pg_constraint
                WHERE conrelid = 'company_metrics'::regclass
                AND contype = 'u'
            """)).fetchall()
            
            logger.info("  Unique constraints:")
            for row in result:
                logger.info(f"    {row.conname}: {row.contype}")
            
            logger.info("\n" + "="*60)
            logger.info("✅ DONE - company_metrics.ticker is now unique")
            logger.info("="*60)
            
        except Exception as e:
            if "already exists" in str(e):
                logger.info("\n✅ Unique constraint already exists")
            else:
                logger.error(f"\n❌ Error: {e}")
                raise

if __name__ == "__main__":
    fix_company_metrics_unique()
