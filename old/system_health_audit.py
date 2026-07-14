"""Comprehensive system health audit for comp API stability"""
import logging
from sqlalchemy import text
from core.database import SessionLocal
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_system_health():
    """Audit all critical components of the system"""
    
    with SessionLocal() as db:
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "warnings": [],
            "summary": {}
        }
        
        logger.info("="*70)
        logger.info("COMPREHENSIVE SYSTEM HEALTH AUDIT")
        logger.info("="*70)
        
        # 1. COMPANIES
        logger.info("\n📊 1. COMPANIES")
        total_companies = db.execute(text("SELECT COUNT(*) FROM companies WHERE is_active = TRUE")).scalar()
        by_financial_group = db.execute(text("""
            SELECT financial_group, COUNT(*) as count
            FROM companies
            WHERE is_active = TRUE
            GROUP BY financial_group
            ORDER BY count DESC
        """)).fetchall()
        
        logger.info(f"  Total Active Companies: {total_companies}")
        for row in by_financial_group:
            logger.info(f"    {row.financial_group}: {row.count}")
        
        report["summary"]["total_companies"] = total_companies
        
        # 2. FINANCIAL STATEMENTS
        logger.info("\n📊 2. FINANCIAL STATEMENTS")
        total_statements = db.execute(text("SELECT COUNT(*) FROM financial_statements_raw")).scalar()
        companies_with_statements = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM financial_statements_raw")).scalar()
        companies_without_statements = total_companies - companies_with_statements
        
        logger.info(f"  Total Statements: {total_statements:,}")
        logger.info(f"  Companies with Statements: {companies_with_statements}/{total_companies}")
        
        if companies_without_statements > 0:
            logger.warning(f"  ⚠️  {companies_without_statements} companies have NO financial statements")
            report["warnings"].append(f"{companies_without_statements} companies missing financial statements")
            
            # List them
            missing = db.execute(text("""
                SELECT c.ticker, c.name, c.industry, c.financial_group
                FROM companies c
                LEFT JOIN financial_statements_raw fs ON c.ticker = fs.ticker
                WHERE c.is_active = TRUE AND fs.ticker IS NULL
                ORDER BY c.industry, c.ticker
                LIMIT 20
            """)).fetchall()
            
            logger.info(f"\n  Sample companies without statements:")
            for row in missing:
                logger.info(f"    {row.ticker:<8} {row.name:<30} [{row.financial_group}] {row.industry}")
        
        report["summary"]["companies_with_statements"] = companies_with_statements
        report["summary"]["companies_without_statements"] = companies_without_statements
        
        # 3. RATIOS
        logger.info("\n📊 3. COMPANY RATIOS")
        total_ratios = db.execute(text("SELECT COUNT(*) FROM company_ratios")).scalar()
        companies_with_ratios = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM company_ratios")).scalar()
        companies_without_ratios = total_companies - companies_with_ratios
        
        ratio_coverage = db.execute(text("""
            SELECT ratio_code, COUNT(DISTINCT ticker) as company_count
            FROM company_ratios
            GROUP BY ratio_code
            ORDER BY company_count DESC
            LIMIT 15
        """)).fetchall()
        
        logger.info(f"  Total Ratios: {total_ratios:,}")
        logger.info(f"  Companies with Ratios: {companies_with_ratios}/{total_companies}")
        logger.info(f"  Top Ratios by Coverage:")
        for row in ratio_coverage:
            coverage_pct = 100 * row.company_count / total_companies
            logger.info(f"    {row.ratio_code:<20} {row.company_count:>3} companies ({coverage_pct:.1f}%)")
        
        if companies_without_ratios > 0:
            logger.warning(f"  ⚠️  {companies_without_ratios} companies have NO ratios")
            report["warnings"].append(f"{companies_without_ratios} companies missing ratios")
        
        report["summary"]["companies_with_ratios"] = companies_with_ratios
        report["summary"]["companies_without_ratios"] = companies_without_ratios
        
        # 4. SCORES
        logger.info("\n📊 4. COMPANY SCORES")
        total_scores = db.execute(text("SELECT COUNT(*) FROM company_scores WHERE is_stale = FALSE")).scalar()
        companies_with_scores = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM company_scores WHERE is_stale = FALSE")).scalar()
        companies_without_scores = total_companies - companies_with_scores
        
        logger.info(f"  Total Scores: {total_scores:,}")
        logger.info(f"  Companies with Scores: {companies_with_scores}/{total_companies}")
        
        if companies_without_scores > 0:
            logger.warning(f"  ⚠️  {companies_without_scores} companies have NO scores")
            report["warnings"].append(f"{companies_without_scores} companies missing scores")
        
        report["summary"]["companies_with_scores"] = companies_with_scores
        report["summary"]["companies_without_scores"] = companies_without_scores
        
        # 5. SECTOR BENCHMARKS
        logger.info("\n📊 5. SECTOR BENCHMARKS")
        total_benchmarks = db.execute(text("SELECT COUNT(*) FROM sector_benchmarks")).scalar()
        sectors_with_benchmarks = db.execute(text("SELECT COUNT(DISTINCT sector_main) FROM sector_benchmarks")).scalar()
        
        logger.info(f"  Total Benchmarks: {total_benchmarks:,}")
        logger.info(f"  Sectors with Benchmarks: {sectors_with_benchmarks}")
        
        if sectors_with_benchmarks < 20:
            logger.warning(f"  ⚠️  Only {sectors_with_benchmarks} sectors have benchmarks")
            report["warnings"].append(f"Only {sectors_with_benchmarks} sectors have benchmarks")
        
        report["summary"]["sectors_with_benchmarks"] = sectors_with_benchmarks
        
        # 6. PRICE DATA (company_metrics)
        logger.info("\n📊 6. PRICE DATA (company_metrics)")
        companies_with_price = db.execute(text("""
            SELECT COUNT(DISTINCT ticker) FROM company_metrics WHERE last_price IS NOT NULL
        """)).scalar()
        companies_with_pe = db.execute(text("""
            SELECT COUNT(DISTINCT ticker) FROM company_metrics WHERE pe_ratio IS NOT NULL
        """)).scalar()
        companies_without_price = total_companies - companies_with_price
        
        logger.info(f"  Companies with Price: {companies_with_price}/{total_companies} ({100*companies_with_price/total_companies:.1f}%)")
        logger.info(f"  Companies with P/E: {companies_with_pe}/{total_companies} ({100*companies_with_pe/total_companies:.1f}%)")
        
        if companies_with_price < total_companies * 0.5:
            report["issues"].append(f"CRITICAL: Only {companies_with_price}/{total_companies} companies have price data")
            logger.error(f"  ❌ CRITICAL: Only {companies_with_price}/{total_companies} companies have price data")
        
        report["summary"]["companies_with_price"] = companies_with_price
        report["summary"]["companies_with_pe"] = companies_with_pe
        
        # 7. FINVERI PRICE SOURCE (daily_prices)
        logger.info("\n📊 7. FINVERI PRICE SOURCE (daily_prices)")
        total_price_records = db.execute(text("SELECT COUNT(*) FROM daily_prices")).scalar()
        tickers_in_daily_prices = db.execute(text("SELECT COUNT(DISTINCT ticker) FROM daily_prices")).scalar()
        
        latest_price_date = db.execute(text("SELECT MAX(date) FROM daily_prices")).scalar()
        days_old = (datetime.now().date() - latest_price_date).days if latest_price_date else None
        
        logger.info(f"  Total Price Records: {total_price_records:,}")
        logger.info(f"  Tickers in daily_prices: {tickers_in_daily_prices}/{total_companies}")
        logger.info(f"  Latest Price Date: {latest_price_date} ({days_old} days old)" if days_old is not None else "  Latest Price Date: N/A")
        
        if days_old and days_old > 1:
            report["warnings"].append(f"Price data is {days_old} days old")
            logger.warning(f"  ⚠️  Price data is {days_old} days old")
        
        if tickers_in_daily_prices < total_companies * 0.8:
            report["issues"].append(f"Only {tickers_in_daily_prices}/{total_companies} companies in daily_prices")
            logger.error(f"  ❌ Only {tickers_in_daily_prices}/{total_companies} companies have price history")
        
        report["summary"]["tickers_in_daily_prices"] = tickers_in_daily_prices
        report["summary"]["price_data_age_days"] = days_old
        
        # 8. DATA FRESHNESS
        logger.info("\n📊 8. DATA FRESHNESS")
        
        latest_fetch = db.execute(text("SELECT MAX(fetched_at) FROM financial_statements_raw")).scalar()
        latest_ratio_calc = db.execute(text("SELECT MAX(computed_at) FROM company_ratios")).scalar()
        latest_score_calc = db.execute(text("SELECT MAX(computed_at) FROM company_scores WHERE is_stale = FALSE")).scalar()
        
        logger.info(f"  Latest Financial Data Fetch: {latest_fetch}")
        logger.info(f"  Latest Ratio Calculation: {latest_ratio_calc}")
        logger.info(f"  Latest Score Calculation: {latest_score_calc}")
        
        # SUMMARY
        logger.info("\n" + "="*70)
        logger.info("SUMMARY")
        logger.info("="*70)
        
        issues_count = len(report["issues"])
        warnings_count = len(report["warnings"])
        
        if issues_count > 0:
            logger.error(f"\n❌ CRITICAL ISSUES ({issues_count}):")
            for issue in report["issues"]:
                logger.error(f"  - {issue}")
        
        if warnings_count > 0:
            logger.warning(f"\n⚠️  WARNINGS ({warnings_count}):")
            for warning in report["warnings"]:
                logger.warning(f"  - {warning}")
        
        if issues_count == 0 and warnings_count == 0:
            logger.info("\n✅ All systems healthy!")
        
        logger.info(f"\nData Coverage:")
        logger.info(f"  Financial Statements: {100*companies_with_statements/total_companies:.1f}%")
        logger.info(f"  Ratios: {100*companies_with_ratios/total_companies:.1f}%")
        logger.info(f"  Scores: {100*companies_with_scores/total_companies:.1f}%")
        logger.info(f"  Prices: {100*companies_with_price/total_companies:.1f}%")
        
        return report

if __name__ == "__main__":
    audit_system_health()
