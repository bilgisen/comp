"""
Simple and fast ratio calculation using direct SQL
"""
import logging
from datetime import datetime
from sqlalchemy import text

from core.database import SessionLocal
from models.financial import CompanyRatio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calculate_ratios_sql():
    """Calculate ratios using direct SQL for speed"""
    
    with SessionLocal() as db:
        # Clear existing ratios
        db.execute(text("DELETE FROM company_ratios"))
        db.commit()
        logger.info("Cleared existing ratios")
        
        # Get all companies with their financial data
        companies = db.execute(text('''
            SELECT DISTINCT 
                fsr.ticker,
                c.sector_main,
                c.financial_group
            FROM financial_statements_raw fsr
            JOIN companies c ON fsr.ticker = c.ticker
            ORDER BY fsr.ticker
        ''')).fetchall()
        
        logger.info(f"Found {len(companies)} companies")
        
        total_ratios = 0
        processed = 0
        
        for company in companies:
            ticker = company[0]
            sector_main = company[1]
            financial_group = company[2]
            
            try:
                # Get periods for this company
                periods = db.execute(text('''
                    SELECT DISTINCT period_key, year, period
                    FROM financial_statements_raw
                    WHERE ticker = :ticker
                    ORDER BY period_key DESC
                '''), {"ticker": ticker}).fetchall()
                
                for period in periods:
                    period_key = period[0]
                    
                    # Get financial data for this period
                    data = db.execute(text('''
                        SELECT item_code, value_try
                        FROM financial_statements_raw
                        WHERE ticker = :ticker AND period_key = :period_key
                    '''), {"ticker": ticker, "period_key": period_key}).fetchall()
                    
                    # Build data dict
                    financial_data = {}
                    for item in data:
                        item_code = item[0]
                        value = item[1]
                        if value is not None:
                            financial_data[item_code] = float(value)
                    
                    # Calculate ratios based on financial group
                    ratios = calculate_ratios_for_data(financial_data, financial_group)
                    
                    # Save ratios
                    for ratio_code, ratio_value in ratios.items():
                        if ratio_value is not None:
                            db.execute(text('''
                                INSERT INTO company_ratios 
                                (ticker, period_key, ratio_code, ratio_value, is_ttm, calculation_method, data_quality_score, computed_at)
                                VALUES (:ticker, :period_key, :ratio_code, :ratio_value, :is_ttm, :method, 0.85, NOW())
                                ON CONFLICT (ticker, period_key, ratio_code) 
                                DO UPDATE SET 
                                    ratio_value = EXCLUDED.ratio_value,
                                    computed_at = NOW()
                            '''), {
                                "ticker": ticker,
                                "period_key": period_key,
                                "ratio_code": ratio_code,
                                "ratio_value": ratio_value,
                                "is_ttm": "ttm" in ratio_code.lower() or ratio_code in ["roe", "roa", "gross_margin", "operating_margin", "net_margin", "ebitda_margin"],
                                "method": "SQL_CALC"
                            })
                            total_ratios += 1
                
                processed += 1
                if processed % 50 == 0:
                    db.commit()
                    logger.info(f"Progress: {processed}/{len(companies)} companies, {total_ratios} ratios")
            
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
                continue
        
        db.commit()
        
        logger.info(f"Completed: {processed} companies, {total_ratios} ratios")
        return total_ratios


def calculate_ratios_for_data(data: dict, financial_group: str) -> dict:
    """Calculate ratios from financial data dict"""
    ratios = {}
    
    def safe_div(a, b):
        if a is None or b is None or b == 0:
            return None
        return a / b
    
    def get(code, default=0):
        val = data.get(code)
        return float(val) if val is not None else default
    
    if financial_group in ["UFRS_K", "UFRS_F", "UFRS_S"]:
        # Banking ratios
        total_assets = get("1Z")
        gross_loans = get("1AF")
        deposits = get("2A")
        shareholders_equity = get("2O")
        net_income = get("3ZA")
        
        ratios["loan_to_deposit"] = safe_div(gross_loans, deposits)
        ratios["roe"] = safe_div(net_income, shareholders_equity)
        ratios["roa"] = safe_div(net_income, total_assets)
        
    else:
        # Industrial (XI_29) ratios
        total_assets = get("1BL")
        current_assets = get("1A")
        cash = get("1AA")
        inventories = get("1AF")
        current_liabilities = get("2A")
        short_term_debt = get("2AA")
        long_term_debt = get("2BA")
        shareholders_equity = get("2O")
        revenue = get("3C")
        gross_profit = get("3D")
        operating_income = get("3DF")
        net_income = get("3Z")
        
        total_liabilities = total_assets - shareholders_equity if total_assets and shareholders_equity else None
        total_debt = (short_term_debt or 0) + (long_term_debt or 0)
        
        # Liquidity
        ratios["current_ratio"] = safe_div(current_assets, current_liabilities)
        ratios["acid_test_ratio"] = safe_div((current_assets or 0) - (inventories or 0), current_liabilities)
        
        # Leverage
        ratios["debt_to_equity"] = safe_div(total_debt, shareholders_equity)
        ratios["debt_ratio"] = safe_div(total_liabilities, total_assets)
        ratios["net_debt_to_equity"] = safe_div((total_debt or 0) - (cash or 0), shareholders_equity)
        
        # Profitability
        ratios["gross_margin"] = safe_div(gross_profit, revenue)
        ratios["operating_margin"] = safe_div(operating_income, revenue)
        ratios["net_margin"] = safe_div(net_income, revenue)
        ratios["ebitda_margin"] = safe_div(operating_income, revenue)
        ratios["roe"] = safe_div(net_income, shareholders_equity)
        ratios["roa"] = safe_div(net_income, total_assets)
        
        # Efficiency
        ratios["asset_turnover"] = safe_div(revenue, total_assets)
    
    return ratios


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SQL RATIO CALCULATION STARTING")
    logger.info("=" * 60)
    
    start = datetime.now()
    total = calculate_ratios_sql()
    duration = (datetime.now() - start).total_seconds() / 60
    
    logger.info("=" * 60)
    logger.info(f"COMPLETED in {duration:.1f} minutes")
    logger.info(f"Total ratios: {total}")
    logger.info("=" * 60)
