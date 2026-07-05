"""Generate complete tickers.json for finveri from comp database"""
import json
import logging
from sqlalchemy import text
from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_tickers_json():
    """Generate tickers.json with all active companies from comp database"""
    
    with SessionLocal() as db:
        # Get all active companies
        companies = db.execute(text("""
            SELECT ticker, name, industry, sector_main
            FROM companies
            WHERE is_active = TRUE
            ORDER BY ticker
        """)).fetchall()
        
        logger.info(f"Found {len(companies)} active companies")
        
        # Build tickers dict
        tickers = {
            "_meta": {
                "description": "BIST hisse senedi ticker listesi - Auto-generated from comp database",
                "last_updated": "2026-07-05",
                "source": "comp database",
                "total_tickers": len(companies)
            }
        }
        
        for row in companies:
            tickers[row.ticker] = {
                "code": row.ticker,
                "name": row.name,
                "sector": row.industry or row.sector_main,
                "market": "BIST",
                "aliases": {}
            }
        
        # Add major indices
        indices = {
            "XU100": {"code": "XU100", "name": "BIST 100 Endeksi", "sector": "Endeks", "market": "BIST_INDEX", "aliases": {}},
            "XU030": {"code": "XU030", "name": "BIST 30 Endeksi", "sector": "Endeks", "market": "BIST_INDEX", "aliases": {}},
            "XBANK": {"code": "XBANK", "name": "BIST Banka Endeksi", "sector": "Endeks", "market": "BIST_INDEX", "aliases": {}},
            "XUSIN": {"code": "XUSIN", "name": "BIST Sınai Endeksi", "sector": "Endeks", "market": "BIST_INDEX", "aliases": {}},
        }
        
        tickers.update(indices)
        
        # Write to file
        output_path = r"c:\Users\ASUS\hp\finveri\data\tickers.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tickers, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Generated {output_path}")
        logger.info(f"  Total entries: {len(tickers) - 1}")  # -1 for _meta
        logger.info(f"  Companies: {len(companies)}")
        logger.info(f"  Indices: {len(indices)}")
        
        return len(tickers) - 1

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("GENERATE FINVERI TICKERS.JSON")
    logger.info("="*60)
    count = generate_tickers_json()
    logger.info(f"\n✅ Done! Generated {count} tickers")
    logger.info("\nNext steps:")
    logger.info("  1. Restart finveri to reload tickers")
    logger.info("  2. Run finveri historical sync")
    logger.info("  3. Run populate_company_metrics.py")
    logger.info("="*60)
