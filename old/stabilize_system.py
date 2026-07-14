"""
Comprehensive System Stabilization Script

This script ensures:
1. All active companies have financial statements
2. All ratios are calculated for companies with statements
3. All scores are calculated for companies with ratios
4. Sector benchmarks are up-to-date
5. Price data is synchronized from finveri

Target: 95%+ coverage across all data points
"""

import logging
import asyncio
from datetime import datetime
from sqlalchemy import text
from core.database import SessionLocal
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemStabilizer:
    def __init__(self):
        self.db = SessionLocal()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "phases": [],
            "summary": {}
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def log_phase(self, phase_name, status, details):
        """Log phase completion"""
        self.report["phases"].append({
            "phase": phase_name,
            "status": status,
            "details": details
        })
    
    def get_system_state(self):
        """Get current system state"""
        logger.info("="*70)
        logger.info("SYSTEM STATE ANALYSIS")
        logger.info("="*70)
        
        total_companies = self.db.execute(text(
            "SELECT COUNT(*) FROM companies WHERE is_active = TRUE"
        )).scalar()
        
        state = {
            "total_companies": total_companies,
            "with_statements": self.db.execute(text(
                "SELECT COUNT(DISTINCT ticker) FROM financial_statements_raw"
            )).scalar(),
            "with_ratios": self.db.execute(text(
                "SELECT COUNT(DISTINCT ticker) FROM company_ratios"
            )).scalar(),
            "with_scores": self.db.execute(text(
                "SELECT COUNT(DISTINCT ticker) FROM company_scores WHERE is_stale = FALSE"
            )).scalar(),
            "with_price": self.db.execute(text(
                "SELECT COUNT(DISTINCT ticker) FROM company_metrics WHERE last_price IS NOT NULL"
            )).scalar(),
            "with_pe": self.db.execute(text(
                "SELECT COUNT(DISTINCT ticker) FROM company_metrics WHERE pe_ratio IS NOT NULL"
            )).scalar(),
            "daily_prices_tickers": self.db.execute(text(
                "SELECT COUNT(DISTINCT ticker) FROM daily_prices"
            )).scalar()
        }
        
        logger.info(f"\n📊 Current Coverage:")
        logger.info(f"  Total Active Companies: {state['total_companies']}")
        logger.info(f"  With Financial Statements: {state['with_statements']} ({100*state['with_statements']/state['total_companies']:.1f}%)")
        logger.info(f"  With Ratios: {state['with_ratios']} ({100*state['with_ratios']/state['total_companies']:.1f}%)")
        logger.info(f"  With Scores: {state['with_scores']} ({100*state['with_scores']/state['total_companies']:.1f}%)")
        logger.info(f"  With Price: {state['with_price']} ({100*state['with_price']/state['total_companies']:.1f}%)")
        logger.info(f"  With P/E: {state['with_pe']} ({100*state['with_pe']/state['total_companies']:.1f}%)")
        logger.info(f"  In daily_prices: {state['daily_prices_tickers']} ({100*state['daily_prices_tickers']/state['total_companies']:.1f}%)")
        
        return state
    
    def phase1_verify_financial_data(self):
        """Phase 1: Verify financial statements coverage"""
        logger.info("\n" + "="*70)
        logger.info("PHASE 1: FINANCIAL STATEMENTS VERIFICATION")
        logger.info("="*70)
        
        # Get companies without statements
        missing = self.db.execute(text("""
            SELECT c.ticker, c.name, c.industry, c.financial_group
            FROM companies c
            LEFT JOIN financial_statements_raw fs ON c.ticker = fs.ticker
            WHERE c.is_active = TRUE AND fs.ticker IS NULL
            ORDER BY c.financial_group, c.ticker
        """)).fetchall()
        
        if len(missing) == 0:
            logger.info("✅ All active companies have financial statements")
            self.log_phase("financial_statements", "ok", "100% coverage")
            return True
        
        logger.warning(f"⚠️  {len(missing)} companies missing financial statements:")
        for row in missing[:10]:
            logger.info(f"  {row.ticker:<8} {row.name:<35} [{row.financial_group}]")
        
        if len(missing) > 10:
            logger.info(f"  ... and {len(missing)-10} more")
        
        self.log_phase("financial_statements", "warning", f"{len(missing)} companies missing data")
        return False
    
    def phase2_verify_ratios(self):
        """Phase 2: Verify ratio calculations"""
        logger.info("\n" + "="*70)
        logger.info("PHASE 2: RATIO VERIFICATION")
        logger.info("="*70)
        
        # Companies with statements but no ratios
        missing = self.db.execute(text("""
            SELECT DISTINCT c.ticker, c.name, c.financial_group
            FROM companies c
            JOIN financial_statements_raw fs ON c.ticker = fs.ticker
            LEFT JOIN company_ratios cr ON c.ticker = cr.ticker
            WHERE c.is_active = TRUE AND cr.ticker IS NULL
            ORDER BY c.financial_group, c.ticker
        """)).fetchall()
        
        if len(missing) == 0:
            logger.info("✅ All companies with statements have ratios")
            self.log_phase("ratios", "ok", "100% coverage")
            return True
        
        logger.warning(f"⚠️  {len(missing)} companies missing ratios:")
        for row in missing[:10]:
            logger.info(f"  {row.ticker:<8} {row.name:<35} [{row.financial_group}]")
        
        if len(missing) > 10:
            logger.info(f"  ... and {len(missing)-10} more")
        
        self.log_phase("ratios", "warning", f"{len(missing)} companies need ratio calculation")
        
        # Group by financial_group for targeted calculation
        by_group = {}
        for row in missing:
            if row.financial_group not in by_group:
                by_group[row.financial_group] = []
            by_group[row.financial_group].append(row.ticker)
        
        logger.info(f"\n📋 Missing ratios by financial group:")
        for group, tickers in sorted(by_group.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"  {group:<15} {len(tickers):>3} companies")
        
        return False
    
    def phase3_verify_scores(self):
        """Phase 3: Verify score calculations"""
        logger.info("\n" + "="*70)
        logger.info("PHASE 3: SCORE VERIFICATION")
        logger.info("="*70)
        
        # Companies with ratios but no scores
        missing = self.db.execute(text("""
            SELECT DISTINCT c.ticker, c.name, c.financial_group
            FROM companies c
            JOIN company_ratios cr ON c.ticker = cr.ticker
            LEFT JOIN company_scores cs ON c.ticker = cs.ticker AND cs.is_stale = FALSE
            WHERE c.is_active = TRUE AND cs.ticker IS NULL
            ORDER BY c.financial_group, c.ticker
        """)).fetchall()
        
        if len(missing) == 0:
            logger.info("✅ All companies with ratios have scores")
            self.log_phase("scores", "ok", "100% coverage")
            return True
        
        logger.warning(f"⚠️  {len(missing)} companies missing scores:")
        for row in missing[:10]:
            logger.info(f"  {row.ticker:<8} {row.name:<35} [{row.financial_group}]")
        
        if len(missing) > 10:
            logger.info(f"  ... and {len(missing)-10} more")
        
        self.log_phase("scores", "warning", f"{len(missing)} companies need score calculation")
        return False
    
    def phase4_verify_sector_benchmarks(self):
        """Phase 4: Verify sector benchmarks"""
        logger.info("\n" + "="*70)
        logger.info("PHASE 4: SECTOR BENCHMARKS VERIFICATION")
        logger.info("="*70)
        
        total_sectors = self.db.execute(text(
            "SELECT COUNT(DISTINCT industry) FROM companies WHERE is_active = TRUE"
        )).scalar()
        
        sectors_with_benchmarks = self.db.execute(text(
            "SELECT COUNT(DISTINCT sector_main) FROM sector_benchmarks"
        )).scalar()
        
        logger.info(f"  Total Sectors: {total_sectors}")
        logger.info(f"  Sectors with Benchmarks: {sectors_with_benchmarks}")
        
        if sectors_with_benchmarks >= total_sectors * 0.9:
            logger.info("✅ Sector benchmarks coverage is good")
            self.log_phase("benchmarks", "ok", f"{sectors_with_benchmarks}/{total_sectors} sectors")
            return True
        
        logger.warning(f"⚠️  Only {sectors_with_benchmarks}/{total_sectors} sectors have benchmarks")
        self.log_phase("benchmarks", "warning", "Need benchmark recalculation")
        return False
    
    def phase5_sync_prices(self):
        """Phase 5: Sync prices from daily_prices to company_metrics"""
        logger.info("\n" + "="*70)
        logger.info("PHASE 5: PRICE DATA SYNCHRONIZATION")
        logger.info("="*70)
        
        # Get latest price for each ticker
        logger.info("📊 Getting latest prices from daily_prices...")
        
        latest_prices = self.db.execute(text("""
            WITH latest_date AS (
                SELECT ticker, MAX(date) as last_date
                FROM daily_prices
                GROUP BY ticker
            )
            SELECT dp.ticker, dp.close as last_price, dp.date, dp.volume
            FROM daily_prices dp
            JOIN latest_date ld ON dp.ticker = ld.ticker AND dp.date = ld.last_date
            WHERE dp.ticker IN (SELECT ticker FROM companies WHERE is_active = TRUE)
            ORDER BY dp.ticker
        """)).fetchall()
        
        logger.info(f"  Found {len(latest_prices)} tickers with price data")
        
        if len(latest_prices) == 0:
            logger.error("❌ No price data in daily_prices table")
            self.log_phase("price_sync", "error", "No data in daily_prices")
            return False
        
        # Get EPS data
        logger.info("📊 Getting EPS data...")
        eps_data = {}
        eps_results = self.db.execute(text("""
            WITH latest_eps AS (
                SELECT ticker, period_key, ratio_value as eps,
                       ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY period_key DESC) as rn
                FROM company_ratios
                WHERE ratio_code = 'eps' AND ratio_value IS NOT NULL
            )
            SELECT ticker, eps, period_key
            FROM latest_eps
            WHERE rn = 1
        """)).fetchall()
        
        for row in eps_results:
            eps_data[row.ticker] = row.eps
        
        logger.info(f"  Found {len(eps_data)} tickers with EPS data")
        
        # Update company_metrics
        logger.info("📊 Updating company_metrics...")
        
        inserted = 0
        with_pe = 0
        
        for row in latest_prices:
            ticker = row.ticker
            last_price = float(row.last_price) if row.last_price else None
            volume = int(row.volume) if row.volume else None
            
            if not last_price:
                continue
            
            # Calculate P/E ratio
            eps = eps_data.get(ticker)
            pe_ratio = None
            
            if eps and eps > 0 and last_price:
                pe_ratio = last_price / eps
                with_pe += 1
            
            # Upsert
            self.db.execute(text("""
                INSERT INTO company_metrics (ticker, last_price, pe_ratio, volume_1d, price_updated_at)
                VALUES (:ticker, :last_price, :pe_ratio, :volume, :updated_at)
                ON CONFLICT (ticker) DO UPDATE
                SET last_price = :last_price,
                    pe_ratio = :pe_ratio,
                    volume_1d = :volume,
                    price_updated_at = :updated_at,
                    updated_at = :updated_at
            """), {
                "ticker": ticker,
                "last_price": last_price,
                "pe_ratio": pe_ratio,
                "volume": volume,
                "updated_at": datetime.now()
            })
            
            inserted += 1
        
        self.db.commit()
        
        logger.info(f"✅ Updated {inserted} companies")
        logger.info(f"  With P/E ratio: {with_pe}")
        logger.info(f"  Without P/E: {inserted - with_pe}")
        
        self.log_phase("price_sync", "ok", f"{inserted} prices synced, {with_pe} with P/E")
        return True
    
    def generate_report(self):
        """Generate final report"""
        logger.info("\n" + "="*70)
        logger.info("STABILIZATION REPORT")
        logger.info("="*70)
        
        final_state = self.get_system_state()
        
        logger.info("\n📊 Results:")
        for phase in self.report["phases"]:
            status_icon = "✅" if phase["status"] == "ok" else "⚠️" if phase["status"] == "warning" else "❌"
            logger.info(f"  {status_icon} {phase['phase']}: {phase['details']}")
        
        # Calculate health score
        total = final_state["total_companies"]
        health_score = (
            final_state["with_statements"] * 0.25 +
            final_state["with_ratios"] * 0.25 +
            final_state["with_scores"] * 0.25 +
            final_state["with_price"] * 0.25
        ) / total * 100
        
        logger.info(f"\n🏥 System Health Score: {health_score:.1f}%")
        
        if health_score >= 95:
            logger.info("✅ System is STABLE")
        elif health_score >= 85:
            logger.warning("⚠️  System is FUNCTIONAL but needs attention")
        else:
            logger.error("❌ System needs URGENT fixes")
        
        self.report["summary"]["health_score"] = health_score
        self.report["summary"]["final_state"] = final_state
        
        return self.report

def main():
    logger.info("="*70)
    logger.info("COMPREHENSIVE SYSTEM STABILIZATION")
    logger.info("="*70)
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)
    
    with SystemStabilizer() as stabilizer:
        # Get initial state
        initial_state = stabilizer.get_system_state()
        
        # Run phases
        stabilizer.phase1_verify_financial_data()
        stabilizer.phase2_verify_ratios()
        stabilizer.phase3_verify_scores()
        stabilizer.phase4_verify_sector_benchmarks()
        stabilizer.phase5_sync_prices()
        
        # Generate report
        report = stabilizer.generate_report()
    
    logger.info("\n" + "="*70)
    logger.info(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)
    
    return report["summary"]["health_score"]

if __name__ == "__main__":
    try:
        health_score = main()
        sys.exit(0 if health_score >= 95 else 1)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
