"""
Sync Ratio Calculator
Calculate all ratios for all companies with financial data
Uses sync sessions for reliable transaction management
"""

import logging
import math
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.company import Company
from models.financial import FinancialStatementRaw, CompanyRatio
from services.ratio_calculator import RatioConfig
from services.item_code_mapper import ItemCodeMapper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ratio_calculation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class CalculationResult:
    """Result of ratio calculation"""
    ratio_code: str
    value: Optional[float]
    success: bool
    error: Optional[str] = None
    calculation_method: Optional[str] = None
    data_quality_score: Optional[float] = None


class SyncRatioCalculator:
    """Sync ratio calculator with reliable transaction management"""
    
    # Default ratio configurations (XI_29 - Industrial companies)
    DEFAULT_RATIOS = {
        # Liquidity Ratios
        "current_ratio": RatioConfig(
            code="current_ratio",
            formula=lambda d: d.get("current_assets") / d.get("current_liabilities") if d.get("current_assets") is not None and d.get("current_liabilities") is not None and d.get("current_liabilities") != 0 else None,
            type="instant",
            description="Cari Oran = Dönen Varlıklar / Kısa Vadeli Yükümlülükler",
            category="liquidity"
        ),
        
        "acid_test_ratio": RatioConfig(
            code="acid_test_ratio", 
            formula=lambda d: (d.get("current_assets") - d.get("inventories", 0)) / d.get("current_liabilities") if d.get("current_assets") is not None and d.get("current_liabilities") is not None and d.get("current_liabilities") != 0 else None,
            type="instant",
            description="Asit Test Oranı = (Dönen Varlıklar - Stoklar) / Kısa Vadeli Yükümlülükler",
            category="liquidity"
        ),
        
        # Leverage Ratios
        "debt_to_equity": RatioConfig(
            code="debt_to_equity",
            formula=lambda d: d.get("total_debt") / d.get("shareholders_equity") if d.get("total_debt") is not None and d.get("shareholders_equity") is not None and d.get("shareholders_equity") != 0 else None,
            type="instant", 
            description="Borç/Özkaynak = Toplam Borç / Özkaynaklar",
            category="leverage"
        ),
        
        "debt_ratio": RatioConfig(
            code="debt_ratio",
            formula=lambda d: d.get("total_liabilities") / d.get("total_assets") if d.get("total_liabilities") is not None and d.get("total_assets") is not None and d.get("total_assets") != 0 else None,
            type="instant",
            description="Borçlanma Oranı = Toplam Yükümlülükler / Toplam Varlıklar",
            category="leverage"
        ),
        
        "net_debt_to_equity": RatioConfig(
            code="net_debt_to_equity",
            formula=lambda d: (d.get("total_debt") - d.get("cash_and_equivalents", 0)) / d.get("shareholders_equity") if d.get("total_debt") is not None and d.get("shareholders_equity") is not None and d.get("shareholders_equity") != 0 else None,
            type="instant",
            description="Net Borç/Özkaynak = (Toplam Borç - Nakit) / Özkaynaklar", 
            category="leverage"
        ),
        
        # Profitability Ratios (TTM)
        "gross_margin": RatioConfig(
            code="gross_margin",
            formula=lambda d: d.get("gross_profit_ttm") / d.get("revenue_ttm") if d.get("gross_profit_ttm") is not None and d.get("revenue_ttm") is not None and d.get("revenue_ttm") != 0 else None,
            type="ttm",
            description="Brüt Kâr Marjı = Brüt Kâr (TTM) / Satışlar (TTM)",
            category="profitability"
        ),
        
        "operating_margin": RatioConfig(
            code="operating_margin", 
            formula=lambda d: d.get("operating_income_ttm") / d.get("revenue_ttm") if d.get("operating_income_ttm") is not None and d.get("revenue_ttm") is not None and d.get("revenue_ttm") != 0 else None,
            type="ttm",
            description="Faaliyet Kârı Marjı = Faaliyet Kârı (TTM) / Satışlar (TTM)",
            category="profitability"
        ),
        
        "net_margin": RatioConfig(
            code="net_margin",
            formula=lambda d: d.get("net_income_ttm") / d.get("revenue_ttm") if d.get("net_income_ttm") is not None and d.get("revenue_ttm") is not None and d.get("revenue_ttm") != 0 else None,
            type="ttm",
            description="Net Kâr Marjı = Net Kâr (TTM) / Satışlar (TTM)",
            category="profitability"
        ),
        
        "ebitda_margin": RatioConfig(
            code="ebitda_margin",
            formula=lambda d: d.get("ebitda_ttm") / d.get("revenue_ttm") if d.get("ebitda_ttm") is not None and d.get("revenue_ttm") is not None and d.get("revenue_ttm") != 0 else None,
            type="ttm", 
            description="FAVÖK Marjı = FAVÖK (TTM) / Satışlar (TTM)",
            category="profitability"
        ),
        
        # Return Ratios (TTM)
        "roe": RatioConfig(
            code="roe",
            formula=lambda d: d.get("net_income_ttm") / d.get("shareholders_equity_avg") if d.get("net_income_ttm") is not None and d.get("shareholders_equity_avg") is not None and d.get("shareholders_equity_avg") != 0 else None,
            type="ttm",
            description="Özkaynak Kârlılığı = Net Kâr (TTM) / Ortalama Özkaynaklar",
            category="profitability"
        ),
        
        "roa": RatioConfig(
            code="roa", 
            formula=lambda d: d.get("net_income_ttm") / d.get("total_assets_avg") if d.get("net_income_ttm") is not None and d.get("total_assets_avg") is not None and d.get("total_assets_avg") != 0 else None,
            type="ttm",
            description="Aktif Kârlılığı = Net Kâr (TTM) / Ortalama Toplam Aktif",
            category="profitability"
        ),
        
        # Valuation Ratios
        "pe_ratio": RatioConfig(
            code="pe_ratio",
            formula=lambda d: d.get("market_cap") / d.get("net_income_ttm") if d.get("market_cap") is not None and d.get("net_income_ttm") is not None and d.get("net_income_ttm") > 0 else None,
            type="ttm",
            description="F/K Oranı = Piyasa Değeri / Net Kâr (TTM)", 
            category="valuation"
        ),
        
        "pb_ratio": RatioConfig(
            code="pb_ratio",
            formula=lambda d: d.get("market_cap") / d.get("shareholders_equity") if d.get("market_cap") is not None and d.get("shareholders_equity") is not None and d.get("shareholders_equity") != 0 else None,
            type="instant",
            description="PD/DD Oranı = Piyasa Değeri / Defter Değeri",
            category="valuation"
        ),
        
        "ev_ebitda": RatioConfig(
            code="ev_ebitda",
            formula=lambda d: (d.get("market_cap") + d.get("net_debt", 0)) / d.get("ebitda_ttm") if d.get("market_cap") is not None and d.get("ebitda_ttm") is not None and d.get("ebitda_ttm") > 0 else None,
            type="ttm",
            description="FD/FAVÖK = (Piyasa Değeri + Net Borç) / FAVÖK (TTM)",
            category="valuation"
        ),
        
        # Efficiency Ratios (TTM)
        "asset_turnover": RatioConfig(
            code="asset_turnover",
            formula=lambda d: d.get("revenue_ttm") / d.get("total_assets_avg") if d.get("revenue_ttm") is not None and d.get("total_assets_avg") is not None and d.get("total_assets_avg") != 0 else None,
            type="ttm",
            description="Aktif Devir Hızı = Satışlar (TTM) / Ortalama Toplam Aktif",
            category="efficiency"
        ),
        
        "inventory_turnover": RatioConfig(
            code="inventory_turnover", 
            formula=lambda d: d.get("cost_of_goods_sold_ttm") / d.get("inventories_avg") if d.get("cost_of_goods_sold_ttm") is not None and d.get("inventories_avg") is not None and d.get("inventories_avg") != 0 else None,
            type="ttm",
            description="Stok Devir Hızı = Satılan Malın Maliyeti (TTM) / Ortalama Stoklar",
            category="efficiency"
        ),
        
        "receivables_turnover": RatioConfig(
            code="receivables_turnover",
            formula=lambda d: d.get("revenue_ttm") / d.get("accounts_receivable_avg") if d.get("revenue_ttm") is not None and d.get("accounts_receivable_avg") is not None and d.get("accounts_receivable_avg") != 0 else None,
            type="ttm", 
            description="Alacak Devir Hızı = Satışlar (TTM) / Ortalama Ticari Alacaklar",
            category="efficiency"
        ),
    }
    
    # Banking-specific ratios (UFRS_K)
    BANKING_RATIOS = {
        "net_interest_margin": RatioConfig(
            code="net_interest_margin",
            formula=lambda d: d.get("net_interest_income_ttm") / d.get("interest_earning_assets_avg") if d.get("net_interest_income_ttm") is not None and d.get("interest_earning_assets_avg") is not None and d.get("interest_earning_assets_avg") != 0 else None,
            type="ttm",
            description="Net Faiz Marjı = Net Faiz Geliri (TTM) / Ortalama Faiz Getirili Aktifler",
            category="profitability"
        ),
        
        "loan_to_deposit": RatioConfig(
            code="loan_to_deposit",
            formula=lambda d: d.get("gross_loans") / d.get("deposits") if d.get("gross_loans") is not None and d.get("deposits") is not None and d.get("deposits") != 0 else None,
            type="instant", 
            description="Kredi/Mevduat Oranı = Brüt Krediler / Mevduat",
            category="banking"
        ),
        
        "npl_ratio": RatioConfig(
            code="npl_ratio",
            formula=lambda d: d.get("non_performing_loans") / d.get("gross_loans") if d.get("non_performing_loans") is not None and d.get("gross_loans") is not None and d.get("gross_loans") != 0 else None,
            type="instant",
            description="Takipteki Kredi Oranı = Takipteki Krediler / Brüt Krediler",
            category="asset_quality"
        ),
        
        "capital_adequacy": RatioConfig(
            code="capital_adequacy",
            formula=lambda d: d.get("tier1_capital") / d.get("risk_weighted_assets") if d.get("tier1_capital") is not None and d.get("risk_weighted_assets") is not None and d.get("risk_weighted_assets") != 0 else None,
            type="instant",
            description="Sermaye Yeterlilik Oranı = Tier 1 Sermaye / Risk Ağırlıklı Aktifler",
            category="capital"
        ),
        
        "cost_income_ratio": RatioConfig(
            code="cost_income_ratio",
            formula=lambda d: d.get("operating_expenses_ttm") / d.get("total_operating_income_ttm") if d.get("operating_expenses_ttm") is not None and d.get("total_operating_income_ttm") is not None and d.get("total_operating_income_ttm") != 0 else None,
            type="ttm",
            description="Maliyet/Gelir Oranı = Faaliyet Giderleri (TTM) / Toplam Faaliyet Geliri (TTM)",
            category="efficiency"
        ),
        
        "roe": RatioConfig(
            code="roe",
            formula=lambda d: d.get("net_income_ttm") / d.get("shareholders_equity_avg") if d.get("net_income_ttm") is not None and d.get("shareholders_equity_avg") is not None and d.get("shareholders_equity_avg") != 0 else None,
            type="ttm",
            description="Özkaynak Kârlılığı = Net Kâr (TTM) / Ortalama Özkaynaklar",
            category="profitability"
        ),
        
        "roa": RatioConfig(
            code="roa", 
            formula=lambda d: d.get("net_income_ttm") / d.get("total_assets_avg") if d.get("net_income_ttm") is not None and d.get("total_assets_avg") is not None and d.get("total_assets_avg") != 0 else None,
            type="ttm",
            description="Aktif Kârlılığı = Net Kâr (TTM) / Ortalama Toplam Aktif",
            category="profitability"
        ),
    }
    
    # Sector-specific ratio configurations
    SECTOR_RATIOS = {
        "Bankacılık & Finans": BANKING_RATIOS,
        "_default": DEFAULT_RATIOS
    }
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_sector_ratios(self, sector_main: str) -> Dict[str, RatioConfig]:
        """Get applicable ratios for a sector"""
        return self.SECTOR_RATIOS.get(sector_main, self.SECTOR_RATIOS["_default"])
    
    def calculate_company_ratios(
        self, 
        ticker: str, 
        period_key: str
    ) -> List[CalculationResult]:
        """
        Calculate all applicable ratios for a company in a specific period (sync version)
        """
        try:
            # Get company info
            company = self.db.query(Company).filter(Company.ticker == ticker).first()
            if not company:
                return [CalculationResult("unknown", None, False, f"Company {ticker} not found")]
            
            # Get applicable ratios for this sector
            sector_ratios = self.get_sector_ratios(company.sector_main)
            
            # Get financial data
            financial_data = self._get_financial_data(ticker, period_key, company.financial_group)
            if not financial_data:
                return [CalculationResult("unknown", None, False, f"No financial data for {ticker} {period_key}")]
            
            # Calculate each ratio
            results = []
            for ratio_code, config in sector_ratios.items():
                result = self._calculate_single_ratio(
                    ticker, period_key, config, financial_data, company.financial_group
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error calculating ratios for {ticker}: {e}", exc_info=True)
            return [CalculationResult("error", None, False, str(e))]
    
    def _get_financial_data(
        self, 
        ticker: str, 
        period_key: str, 
        financial_group: str
    ) -> Optional[Dict[str, float]]:
        """
        Gather all financial data needed for ratio calculations (sync version)
        """
        try:
            mapper = ItemCodeMapper(self.db)
            
            # Get raw financial statements for this period and previous periods
            statements = self.db.query(FinancialStatementRaw).filter(
                and_(
                    FinancialStatementRaw.ticker == ticker,
                    FinancialStatementRaw.financial_group == financial_group
                )
            ).order_by(desc(FinancialStatementRaw.year), desc(FinancialStatementRaw.period)).all()
            
            if not statements:
                logger.warning(f"No statements found for {ticker}")
                return None
            
            # Group by year and period and map item codes to semantic names
            periods_data = {}
            
            for stmt in statements:
                key = (stmt.year, stmt.period)
                if key not in periods_data:
                    periods_data[key] = {}
                
                semantic_name = mapper.get_semantic_name(stmt.item_code, financial_group)
                
                if semantic_name and stmt.value_try is not None:
                    periods_data[key][semantic_name] = float(stmt.value_try)
            
            # Derive missing financial metrics for each period
            for key, p_data in periods_data.items():
                if financial_group not in ["UFRS_K", "UFRS_F", "UFRS_S"]:
                    # Industrial/General companies (XI_29)
                    
                    # 1. total_liabilities (fallback to assets - equity)
                    if "total_assets" in p_data and "shareholders_equity" in p_data:
                        p_data["total_liabilities"] = p_data.get("total_liabilities", p_data["total_assets"] - p_data["shareholders_equity"])
                    else:
                        p_data["total_liabilities"] = p_data.get("total_liabilities", p_data.get("current_liabilities", 0) + p_data.get("non_current_liabilities", 0))
                    
                    # 2. total_debt (short_term_borrowings + long_term_borrowings)
                    p_data["total_debt"] = p_data.get("total_debt", p_data.get("short_term_borrowings", 0) + p_data.get("long_term_borrowings", 0))
                    
                    # 3. net_debt (total_debt - cash_and_equivalents)
                    p_data["net_debt"] = p_data.get("net_debt", p_data["total_debt"] - p_data.get("cash_and_equivalents", 0))
                    
                    # 4. ebitda (fallback to operating_income)
                    p_data["ebitda"] = p_data.get("ebitda", p_data.get("operating_income", 0))
            
            # Find the target period in our grouped data
            target_key = None
            for s in statements:
                if s.period_key == period_key:
                    target_key = (s.year, s.period)
                    break
            
            if not target_key:
                logger.warning(f"Target period_key {period_key} not found in statements for {ticker}")
                return None
                
            # Current period (instant values)
            financial_data = periods_data.get(target_key, {}).copy()
            
            # TTM calculation for income statement items
            if financial_group in ["UFRS_K", "UFRS_F", "UFRS_S"]:
                # Banks report cumulatively - use annual data directly
                annual_statements = [s for s in statements if s.period == 12]
                if annual_statements:
                    latest_annual = annual_statements[0]  # Most recent annual
                    for statement in annual_statements:
                        if statement.year == latest_annual.year:
                            semantic_name = mapper.get_semantic_name(statement.item_code, financial_group)
                            if semantic_name:
                                ttm_name = f"{semantic_name}_ttm"
                                if statement.value_try is not None:
                                    financial_data[ttm_name] = float(statement.value_try)
            else:
                # Other sectors report quarterly - sum last 4 quarters
                financial_data.update(self._calculate_ttm_values(periods_data))
            
            # Calculate average values for certain ratios
            financial_data.update(self._calculate_average_values(periods_data))
            
            return financial_data
            
        except Exception as e:
            logger.error(f"Error getting financial data for {ticker}: {e}", exc_info=True)
            return None
    
    def _calculate_ttm_values(self, periods_data: dict) -> Dict[str, float]:
        """Calculate TTM values for income statement items (XI_29 only)"""
        ttm_data = {}
        
        # Get last 4 quarters
        sorted_periods = sorted(periods_data.keys(), reverse=True)
        if len(sorted_periods) >= 4:
            last_4_periods = sorted_periods[:4]
            
            # Sum income statement items over 4 quarters
            income_statement_items = ["revenue", "gross_profit", "operating_income", "net_income", "ebitda", "cost_of_goods_sold"]
            
            for item in income_statement_items:
                ttm_value = 0
                periods_with_data = 0
                
                for period_key in last_4_periods:
                    period_data = periods_data[period_key]
                    if item in period_data:
                        ttm_value += period_data[item]
                        periods_with_data += 1
                
                # Only include if we have data for at least 3 of 4 periods
                if periods_with_data >= 3:
                    ttm_data[f"{item}_ttm"] = ttm_value
        
        return ttm_data
    
    def _calculate_average_values(self, periods_data: dict) -> Dict[str, float]:
        """Calculate average values (e.g., for ROE, ROA calculations)"""
        avg_data = {}
        
        sorted_periods = sorted(periods_data.keys(), reverse=True)
        if len(sorted_periods) >= 2:
            current_period = periods_data[sorted_periods[0]]
            previous_period = periods_data[sorted_periods[1]]
            
            # Calculate averages for key balance sheet items
            balance_sheet_items = ["total_assets", "shareholders_equity", "inventories", "accounts_receivable"]
            
            for item in balance_sheet_items:
                if item in current_period and item in previous_period:
                    avg_value = (current_period[item] + previous_period[item]) / 2
                    avg_data[f"{item}_avg"] = avg_value
        
        return avg_data
    
    def _calculate_single_ratio(
        self,
        ticker: str,
        period_key: str, 
        config: RatioConfig,
        financial_data: Dict[str, float],
        financial_group: str
    ) -> CalculationResult:
        """Calculate a single ratio"""
        try:
            # Apply formula
            value = config.formula(financial_data)
            
            # Validate result
            if value is None:
                return CalculationResult(
                    config.code, None, False, 
                    "Missing required data for calculation"
                )
            
            if not math.isfinite(value):
                return CalculationResult(
                    config.code, None, False,
                    "Result is infinite or NaN"
                )
            
            # Calculate data quality score
            quality_score = 0.85  # Default quality score
            
            return CalculationResult(
                config.code, value, True,
                calculation_method=config.description,
                data_quality_score=quality_score
            )
            
        except ZeroDivisionError:
            return CalculationResult(
                config.code, None, False,
                "Division by zero"
            )
        except Exception as e:
            return CalculationResult(
                config.code, None, False,
                f"Calculation error: {str(e)}"
            )


def calculate_all_ratios():
    """Main function to calculate ratios for all companies"""
    logger.info("=" * 60)
    logger.info("SYNC RATIO CALCULATION STARTING")
    logger.info("=" * 60)
    
    start_time = datetime.utcnow()
    
    # Get companies with financial data
    with SessionLocal() as db:
        companies_with_data = db.execute(
            select(FinancialStatementRaw.ticker).distinct()
        ).scalars().all()
    
    logger.info(f"Found {len(companies_with_data)} companies with financial data")
    
    total_ratios = 0
    successful_ratios = 0
    failed_companies = 0
    
    for idx, ticker in enumerate(companies_with_data, 1):
        try:
            # Create a fresh session for each company
            with SessionLocal() as db:
                # Get available periods for this company
                periods = db.execute(
                    select(FinancialStatementRaw.period_key)
                    .where(FinancialStatementRaw.ticker == ticker)
                    .distinct()
                ).scalars().all()
                
                company_ratios = 0
                
                for period_key in periods:
                    try:
                        # Calculate ratios
                        calculator = SyncRatioCalculator(db)
                        results = calculator.calculate_company_ratios(ticker, period_key)
                        
                        # Save results
                        for result in results:
                            if result.success and result.value is not None:
                                # Upsert ratio
                                existing = db.query(CompanyRatio).filter(
                                    and_(
                                        CompanyRatio.ticker == ticker,
                                        CompanyRatio.period_key == period_key,
                                        CompanyRatio.ratio_code == result.ratio_code
                                    )
                                ).first()
                                
                                if existing:
                                    existing.ratio_value = result.value
                                    existing.calculation_method = result.calculation_method
                                    existing.data_quality_score = result.data_quality_score
                                    existing.computed_at = datetime.utcnow()
                                else:
                                    ratio = CompanyRatio(
                                        ticker=ticker,
                                        period_key=period_key,
                                        ratio_code=result.ratio_code,
                                        ratio_value=result.value,
                                        is_ttm='ttm' in (result.calculation_method or '').lower(),
                                        calculation_method=result.calculation_method,
                                        data_quality_score=result.data_quality_score,
                                        computed_at=datetime.utcnow()
                                    )
                                    db.add(ratio)
                                
                                company_ratios += 1
                                successful_ratios += 1
                        
                        # Commit after each period
                        db.commit()
                        
                    except Exception as e:
                        logger.error(f"Error calculating ratios for {ticker} {period_key}: {e}")
                        db.rollback()
                        continue
                
                total_ratios += company_ratios
                
                if idx % 10 == 0:
                    logger.info(f"Progress: {idx}/{len(companies_with_data)} companies, {successful_ratios} ratios calculated")
        
        except Exception as e:
            logger.error(f"Error processing company {ticker}: {e}")
            failed_companies += 1
            continue
    
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds() / 60
    
    logger.info("=" * 60)
    logger.info("RATIO CALCULATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Duration: {duration:.1f} minutes")
    logger.info(f"Companies processed: {len(companies_with_data)}")
    logger.info(f"Total ratios calculated: {successful_ratios}")
    logger.info(f"Failed companies: {failed_companies}")
    logger.info("=" * 60)


if __name__ == "__main__":
    calculate_all_ratios()
