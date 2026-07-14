"""Calculate scores for all UFRS_K companies (banks, insurance, etc.)"""
import logging
from datetime import datetime
from sqlalchemy import text

from core.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_all_ufrs_k():
    """Calculate ratios and scores for all UFRS_K companies"""
    
    with SessionLocal() as db:
        # Get all UFRS_K companies
        companies = db.execute(text("""
            SELECT ticker, name, industry
            FROM companies 
            WHERE financial_group = 'UFRS_K' AND is_active = TRUE
            ORDER BY industry, ticker
        """)).fetchall()
        
        logger.info(f"Found {len(companies)} UFRS_K companies")
        
        # Group by industry
        by_industry = {}
        for ticker, name, industry in companies:
            if industry not in by_industry:
                by_industry[industry] = []
            by_industry[industry].append((ticker, name))
        
        for industry, tickers in by_industry.items():
            logger.info(f"  {industry}: {len(tickers)} companies")
        
        # Calculate ratios for companies without them
        logger.info("\n📊 Step 1: Calculating missing ratios...")
        total_ratios = 0
        
        for ticker, name, industry in companies:
            # Check if has ratios
            existing = db.execute(text("""
                SELECT COUNT(*) FROM company_ratios WHERE ticker = :ticker
            """), {"ticker": ticker}).scalar()
            
            if existing > 0:
                continue
            
            logger.info(f"  Processing {ticker} ({industry})...")
            
            # Get periods
            periods = db.execute(text("""
                SELECT DISTINCT period_key FROM financial_statements_raw
                WHERE ticker = :ticker AND financial_group = 'UFRS_K'
                ORDER BY period_key DESC
            """), {"ticker": ticker}).fetchall()
            
            if not periods:
                logger.warning(f"    ⚠️  No financial data")
                continue
            
            for (period_key,) in periods:
                # Get financial data
                data = db.execute(text("""
                    SELECT item_code, value_try
                    FROM financial_statements_raw
                    WHERE ticker = :ticker AND period_key = :period_key
                """), {"ticker": ticker, "period_key": period_key}).fetchall()
                
                fd = {row[0]: float(row[1]) for row in data if row[1] is not None}
                
                # Calculate UFRS_K ratios (banking/insurance style)
                def get(code, default=None):
                    return fd.get(code, default)
                
                def safe_div(a, b):
                    if a is None or b is None or b == 0:
                        return None
                    return a / b
                
                total_assets = get("1Z")
                shareholders_equity = get("2O") or get("2OA")
                net_income = get("3ZA") or get("3Z")
                
                # Basic ratios for UFRS_K
                ratios = {
                    "roe": safe_div(net_income, shareholders_equity),
                    "roa": safe_div(net_income, total_assets),
                }
                
                # For banks specifically
                if industry == "Bankacılık":
                    gross_loans = get("1AF")
                    deposits = get("2A")
                    ratios["loan_to_deposit"] = safe_div(gross_loans, deposits)
                
                # Save ratios
                for ratio_code, ratio_value in ratios.items():
                    if ratio_value is not None:
                        db.execute(text("""
                            INSERT INTO company_ratios (ticker, period_key, ratio_code, ratio_value, is_ttm, computed_at)
                            VALUES (:ticker, :period_key, :ratio_code, :ratio_value, FALSE, :computed_at)
                            ON CONFLICT (ticker, period_key, ratio_code) DO UPDATE
                            SET ratio_value = :ratio_value, computed_at = :computed_at
                        """), {
                            "ticker": ticker,
                            "period_key": period_key,
                            "ratio_code": ratio_code,
                            "ratio_value": ratio_value,
                            "computed_at": datetime.now()
                        })
                        total_ratios += 1
            
            if total_ratios % 50 == 0:
                db.commit()
        
        db.commit()
        logger.info(f"  ✅ Calculated {total_ratios} ratios")
        
        # Calculate scores
        logger.info("\n📊 Step 2: Calculating scores...")
        score_count = 0
        
        for ticker, name, industry in companies:
            # Get latest ratios
            ratios = db.execute(text("""
                SELECT period_key, ratio_code, ratio_value
                FROM company_ratios
                WHERE ticker = :ticker
                ORDER BY period_key DESC
                LIMIT 10
            """), {"ticker": ticker}).fetchall()
            
            if not ratios:
                continue
            
            period_key = ratios[0][0]
            
            # Build ratio dict
            ratio_dict = {}
            for r in ratios:
                if r[0] == period_key:
                    ratio_dict[r[1]] = r[2]
            
            # Calculate score (ROE * 300 + ROA * 700)
            roe = ratio_dict.get('roe', 0) or 0
            roa = ratio_dict.get('roa', 0) or 0
            
            score = min(max((roe * 300 + roa * 700), 0), 100)
            
            # Insert or update score
            db.execute(text("""
                INSERT INTO company_scores (ticker, period_key, score_genel, score_sektor, computed_at, is_stale)
                VALUES (:ticker, :period_key, :score, :score, :computed_at, FALSE)
                ON CONFLICT (ticker, period_key) DO UPDATE
                SET score_genel = :score, score_sektor = :score, computed_at = :computed_at
            """), {
                "ticker": ticker,
                "period_key": period_key,
                "score": score,
                "computed_at": datetime.now()
            })
            
            score_count += 1
        
        db.commit()
        logger.info(f"  ✅ Calculated {score_count} scores")
        
        # Summary by industry
        logger.info("\n📊 Summary by Industry:")
        for industry in by_industry.keys():
            scored = db.execute(text("""
                SELECT COUNT(DISTINCT cs.ticker)
                FROM company_scores cs
                JOIN companies c ON cs.ticker = c.ticker
                WHERE c.industry = :industry AND c.financial_group = 'UFRS_K'
            """), {"industry": industry}).scalar()
            
            total = len(by_industry[industry])
            logger.info(f"  {industry}: {scored}/{total} scored")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("CALCULATE ALL UFRS_K SCORES")
    logger.info("="*60)
    start = datetime.now()
    calculate_all_ufrs_k()
    duration = (datetime.now() - start).total_seconds()
    logger.info(f"\n⏱️  Completed in {duration:.1f} seconds")
    logger.info("="*60)
