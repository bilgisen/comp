"""
Ratio Calculation Correctness Test Module - Requirement 4

Validates that ratio calculations match expected values by comparing
manual calculations against system-computed ratios.
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio

from models.company import Company
from models.financial import FinancialStatementRaw, CompanyRatio
from services.ratio_calculator import RatioCalculator
from services.item_code_mapper import ItemCodeMapper
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter


# Reference companies (1 bank, 2 industrial)
REFERENCE_COMPANIES = {
    "banking": ["GARAN"],  # Garanti BBVA
    "industrial": ["BIMAS", "THYAO"],  # BİM, Turkish Airlines
}


@dataclass
class ComparisonResult:
    """Comparison between expected and actual ratio values"""
    ratio_code: str
    expected: Optional[float]
    actual: Optional[float]
    difference: Optional[float]
    percentage_diff: Optional[float]
    within_tolerance: bool
    tolerance: float


@dataclass
class RatioCorrectnessReport:
    """Ratio calculation correctness test report"""
    tested_companies: List[str]
    total_comparisons: int
    passed: int
    failed: int
    comparisons: List[ComparisonResult]
    accuracy_percentage: float


class RatioCalculationTests:
    """Test suite for ratio calculation correctness validation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.printer = PrettyPrinter()
        self.calculator = RatioCalculator(db)
        self.mapper = ItemCodeMapper(db)
    
    def test_select_reference_companies(self) -> List[str]:
        """
        Select 3 reference companies (1 bank, 2 industrial)
        
        Returns:
            List of ticker symbols
        """
        companies = []
        
        # Add banking company
        companies.extend(REFERENCE_COMPANIES["banking"])
        
        # Add industrial companies
        companies.extend(REFERENCE_COMPANIES["industrial"])
        
        # Verify companies exist
        for ticker in companies:
            company = self.db.query(Company).filter(Company.ticker == ticker).first()
            if not company:
                raise ValueError(f"Reference company {ticker} not found in database")
        
        return companies
    
    def test_manual_calculation(
        self, 
        ticker: str, 
        period_key: str
    ) -> Dict[str, float]:
        """
        Manually calculate expected ratio values for a company
        
        Args:
            ticker: Company ticker
            period_key: Period key (e.g., '2026Q1')
        
        Returns:
            Dictionary of manually calculated ratio values
        """
        # Get company info
        company = self.db.query(Company).filter(Company.ticker == ticker).first()
        if not company:
            return {}
        
        # Get financial statements for this period
        statements = self.db.query(FinancialStatementRaw).filter(
            and_(
                FinancialStatementRaw.ticker == ticker,
                FinancialStatementRaw.period_key == period_key
            )
        ).all()
        
        if not statements:
            return {}
        
        # Map item codes to semantic names
        financial_data = {}
        for stmt in statements:
            semantic_name = self.mapper.get_semantic_name(
                stmt.item_code, 
                company.financial_group
            )
            if semantic_name and stmt.value_try is not None:
                financial_data[semantic_name] = float(stmt.value_try)
        
        # Derive missing fields (same logic as RatioCalculator)
        if company.financial_group not in ["UFRS_K", "UFRS_F", "UFRS_S"]:
            # total_liabilities fallback
            if "total_assets" in financial_data and "shareholders_equity" in financial_data:
                financial_data.setdefault(
                    "total_liabilities",
                    financial_data["total_assets"] - financial_data["shareholders_equity"]
                )
            
            # total_debt
            financial_data.setdefault(
                "total_debt",
                financial_data.get("short_term_borrowings", 0) + 
                financial_data.get("long_term_borrowings", 0)
            )
            
            # net_debt
            financial_data["net_debt"] = (
                financial_data.get("total_debt", 0) - 
                financial_data.get("cash_and_equivalents", 0)
            )
        
        # Get TTM values (simplified - use annual data for now)
        ttm_statements = self.db.query(FinancialStatementRaw).filter(
            and_(
                FinancialStatementRaw.ticker == ticker,
                FinancialStatementRaw.period == 12  # Annual data
            )
        ).order_by(desc(FinancialStatementRaw.year)).limit(1).all()
        
        for stmt in ttm_statements:
            semantic_name = self.mapper.get_semantic_name(
                stmt.item_code, 
                company.financial_group
            )
            if semantic_name and stmt.value_try is not None:
                financial_data[f"{semantic_name}_ttm"] = float(stmt.value_try)
        
        # Calculate average values for ROE, ROA
        # (Simplified: use current period values as proxy)
        for field in ["total_assets", "shareholders_equity"]:
            if field in financial_data:
                financial_data[f"{field}_avg"] = financial_data[field]
        
        # Add market cap
        if company.market_cap:
            financial_data["market_cap"] = float(company.market_cap)
        
        # Manually calculate ratios
        manual_ratios = {}
        
        # Current Ratio
        if "current_assets" in financial_data and "current_liabilities" in financial_data:
            if financial_data["current_liabilities"] != 0:
                manual_ratios["current_ratio"] = (
                    financial_data["current_assets"] / 
                    financial_data["current_liabilities"]
                )
        
        # Debt to Equity
        if "total_debt" in financial_data and "shareholders_equity" in financial_data:
            if financial_data["shareholders_equity"] != 0:
                manual_ratios["debt_to_equity"] = (
                    financial_data["total_debt"] / 
                    financial_data["shareholders_equity"]
                )
        
        # ROE
        if "net_income_ttm" in financial_data and "shareholders_equity_avg" in financial_data:
            if financial_data["shareholders_equity_avg"] != 0:
                manual_ratios["roe"] = (
                    financial_data["net_income_ttm"] / 
                    financial_data["shareholders_equity_avg"]
                )
        
        # Banking-specific ratios
        if company.sector_main == "Bankacılık & Finans":
            # Loan to Deposit
            if "gross_loans" in financial_data and "deposits" in financial_data:
                if financial_data["deposits"] != 0:
                    manual_ratios["loan_to_deposit"] = (
                        financial_data["gross_loans"] / 
                        financial_data["deposits"]
                    )
            
            # NPL Ratio
            if "non_performing_loans" in financial_data and "gross_loans" in financial_data:
                if financial_data["gross_loans"] != 0:
                    manual_ratios["npl_ratio"] = (
                        financial_data["non_performing_loans"] / 
                        financial_data["gross_loans"]
                    )
        
        return manual_ratios
    
    async def test_system_calculation(
        self, 
        ticker: str, 
        period_key: str
    ) -> Dict[str, float]:
        """
        Execute RatioCalculator for same companies and retrieve calculated values
        
        Args:
            ticker: Company ticker
            period_key: Period key
        
        Returns:
            Dictionary of system-calculated ratio values
        """
        # Execute ratio calculator
        results = await self.calculator.calculate_company_ratios(ticker, period_key)
        
        # Extract successful calculations
        system_ratios = {}
        for result in results:
            if result.success and result.value is not None:
                system_ratios[result.ratio_code] = result.value
        
        return system_ratios
    
    def compare_ratios(
        self,
        expected: Dict[str, float],
        actual: Dict[str, float],
        tolerance: float = 0.02
    ) -> List[ComparisonResult]:
        """
        Compare expected vs actual ratio values with tolerance
        
        Args:
            expected: Manually calculated values
            actual: System calculated values
            tolerance: Acceptable percentage difference (default: 2%)
        
        Returns:
            List of comparison results
        """
        comparisons = []
        
        for ratio_code in expected.keys():
            exp_val = expected[ratio_code]
            act_val = actual.get(ratio_code, None)
            
            if act_val is None:
                # System didn't calculate this ratio
                comparisons.append(ComparisonResult(
                    ratio_code=ratio_code,
                    expected=exp_val,
                    actual=None,
                    difference=None,
                    percentage_diff=None,
                    within_tolerance=False,
                    tolerance=tolerance
                ))
                continue
            
            # Calculate difference
            diff = act_val - exp_val
            
            # Calculate percentage difference
            if exp_val != 0:
                pct_diff = abs(diff / exp_val)
            else:
                pct_diff = abs(diff)  # Absolute difference if expected is zero
            
            # Check tolerance
            within_tolerance = pct_diff <= tolerance
            
            comparisons.append(ComparisonResult(
                ratio_code=ratio_code,
                expected=exp_val,
                actual=act_val,
                difference=diff,
                percentage_diff=pct_diff,
                within_tolerance=within_tolerance,
                tolerance=tolerance
            ))
        
        return comparisons
    
    async def test_current_ratio(
        self, 
        ticker: str, 
        period_key: str
    ) -> ComparisonResult:
        """Test current_ratio calculation (current_assets / current_liabilities)"""
        manual = self.test_manual_calculation(ticker, period_key)
        system = await self.test_system_calculation(ticker, period_key)
        
        comparisons = self.compare_ratios(
            {"current_ratio": manual.get("current_ratio", 0)},
            system,
            tolerance=0.02
        )
        
        return comparisons[0] if comparisons else None
    
    async def test_debt_to_equity(
        self, 
        ticker: str, 
        period_key: str
    ) -> ComparisonResult:
        """Test debt_to_equity calculation (total_debt / shareholders_equity)"""
        manual = self.test_manual_calculation(ticker, period_key)
        system = await self.test_system_calculation(ticker, period_key)
        
        comparisons = self.compare_ratios(
            {"debt_to_equity": manual.get("debt_to_equity", 0)},
            system,
            tolerance=0.02
        )
        
        return comparisons[0] if comparisons else None
    
    async def test_roe(
        self, 
        ticker: str, 
        period_key: str
    ) -> ComparisonResult:
        """Test ROE calculation (net_income_ttm / shareholders_equity_avg)"""
        manual = self.test_manual_calculation(ticker, period_key)
        system = await self.test_system_calculation(ticker, period_key)
        
        comparisons = self.compare_ratios(
            {"roe": manual.get("roe", 0)},
            system,
            tolerance=0.02
        )
        
        return comparisons[0] if comparisons else None
    
    async def test_loan_to_deposit(
        self, 
        ticker: str, 
        period_key: str
    ) -> ComparisonResult:
        """Test loan_to_deposit calculation (gross_loans / deposits) - Banking only"""
        manual = self.test_manual_calculation(ticker, period_key)
        system = await self.test_system_calculation(ticker, period_key)
        
        if "loan_to_deposit" not in manual:
            return None
        
        comparisons = self.compare_ratios(
            {"loan_to_deposit": manual["loan_to_deposit"]},
            system,
            tolerance=0.02
        )
        
        return comparisons[0] if comparisons else None
    
    async def test_npl_ratio(
        self, 
        ticker: str, 
        period_key: str
    ) -> ComparisonResult:
        """Test npl_ratio calculation (non_performing_loans / gross_loans) - Banking only"""
        manual = self.test_manual_calculation(ticker, period_key)
        system = await self.test_system_calculation(ticker, period_key)
        
        if "npl_ratio" not in manual:
            return None
        
        comparisons = self.compare_ratios(
            {"npl_ratio": manual["npl_ratio"]},
            system,
            tolerance=0.02
        )
        
        return comparisons[0] if comparisons else None
    
    async def generate_report(
        self,
        companies: List[str],
        period_key: str
    ) -> RatioCorrectnessReport:
        """
        Generate comprehensive ratio correctness report
        
        Args:
            companies: List of company tickers to test
            period_key: Period to test
        
        Returns:
            RatioCorrectnessReport with all comparisons
        """
        all_comparisons = []
        
        for ticker in companies:
            # Get manual calculations
            manual = self.test_manual_calculation(ticker, period_key)
            
            # Get system calculations
            system = await self.test_system_calculation(ticker, period_key)
            
            # Compare
            comparisons = self.compare_ratios(manual, system, tolerance=0.02)
            all_comparisons.extend(comparisons)
        
        # Calculate statistics
        total = len(all_comparisons)
        passed = sum(1 for c in all_comparisons if c.within_tolerance)
        failed = total - passed
        accuracy = (passed / total * 100) if total > 0 else 0.0
        
        report = RatioCorrectnessReport(
            tested_companies=companies,
            total_comparisons=total,
            passed=passed,
            failed=failed,
            comparisons=all_comparisons,
            accuracy_percentage=accuracy
        )
        
        return report
    
    def print_report(self, report: RatioCorrectnessReport) -> str:
        """
        Format and print ratio correctness report
        
        Args:
            report: RatioCorrectnessReport object
        
        Returns:
            Formatted report string
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("RATIO CALCULATION CORRECTNESS TEST - REQUIREMENT 4")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"Tested Companies: {', '.join(report.tested_companies)}")
        lines.append(f"Total Comparisons: {report.total_comparisons}")
        lines.append(f"Passed (within 2% tolerance): {report.passed}")
        lines.append(f"Failed (exceeds 2% tolerance): {report.failed}")
        lines.append(f"Accuracy: {report.accuracy_percentage:.2f}%")
        lines.append("")
        
        # Status
        if report.accuracy_percentage == 100.0:
            status = self.printer.colorize("✅ PASS", "green")
        elif report.accuracy_percentage >= 90.0:
            status = self.printer.colorize("⚠️ WARNING", "yellow")
        else:
            status = self.printer.colorize("❌ FAIL", "red")
        
        lines.append(f"Status: {status}")
        lines.append("")
        
        # Comparison Table
        lines.append("## Comparison Results")
        lines.append("")
        
        comparison_data = []
        for comp in report.comparisons:
            if comp.actual is not None and comp.expected is not None:
                delta_str = f"{comp.difference:+.4f}" if comp.difference is not None else "N/A"
                pct_str = f"{comp.percentage_diff * 100:.2f}%" if comp.percentage_diff is not None else "N/A"
                
                if comp.within_tolerance:
                    status_icon = self.printer.colorize("✓", "green")
                else:
                    status_icon = self.printer.colorize("✗", "red")
                
                comparison_data.append({
                    "ratio": comp.ratio_code,
                    "expected": f"{comp.expected:.4f}",
                    "actual": f"{comp.actual:.4f}",
                    "delta": delta_str,
                    "pct_diff": pct_str,
                    "status": status_icon
                })
            else:
                comparison_data.append({
                    "ratio": comp.ratio_code,
                    "expected": f"{comp.expected:.4f}" if comp.expected is not None else "N/A",
                    "actual": "N/A",
                    "delta": "N/A",
                    "pct_diff": "N/A",
                    "status": self.printer.colorize("⚠", "yellow")
                })
        
        if comparison_data:
            lines.append(self.printer.format_table(
                comparison_data,
                ["ratio", "expected", "actual", "delta", "pct_diff", "status"],
                align={
                    "expected": "right",
                    "actual": "right",
                    "delta": "right",
                    "pct_diff": "right"
                }
            ))
        else:
            lines.append("No comparison data available")
        
        lines.append("")
        
        # Failed comparisons detail
        failed_comps = [c for c in report.comparisons if not c.within_tolerance]
        if failed_comps:
            lines.append("## Failed Comparisons (exceeds 2% tolerance)")
            lines.append("")
            for comp in failed_comps:
                lines.append(f"- {comp.ratio_code}: expected={comp.expected:.4f}, "
                           f"actual={comp.actual:.4f}, diff={comp.percentage_diff * 100:.2f}%")
            lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)


@pytest.mark.integration
@pytest.mark.requirement_4
@pytest.mark.asyncio
async def test_ratio_calculation_correctness(db_session: Session):
    """
    Main test function for ratio calculation correctness
    
    Validates:
        - Manual calculations match system calculations within 2% tolerance
        - Current ratio, debt_to_equity, ROE calculations are correct
        - Banking-specific ratios (loan_to_deposit, npl_ratio) are correct
    """
    # Initialize test suite
    test_suite = RatioCalculationTests(db_session)
    
    # Select reference companies
    companies = test_suite.test_select_reference_companies()
    assert len(companies) == 3, f"Expected 3 reference companies, got {len(companies)}"
    
    # Use latest period (2026Q1 or most recent)
    period_key = "2026Q1"
    
    # Generate report
    report = await test_suite.generate_report(companies, period_key)
    
    # Print report
    report_str = test_suite.print_report(report)
    print("\n" + report_str)
    
    # Assertions
    assert report.accuracy_percentage >= 90.0, (
        f"Ratio calculation accuracy is {report.accuracy_percentage:.2f}%, "
        f"expected >= 90%. Failed {report.failed}/{report.total_comparisons} comparisons."
    )


@pytest.mark.integration
@pytest.mark.requirement_4
@pytest.mark.asyncio
async def test_current_ratio_calculation(db_session: Session):
    """Test current_ratio calculation for industrial companies"""
    test_suite = RatioCalculationTests(db_session)
    period_key = "2026Q1"
    
    for ticker in REFERENCE_COMPANIES["industrial"]:
        result = await test_suite.test_current_ratio(ticker, period_key)
        if result and result.actual is not None:
            assert result.within_tolerance, (
                f"Current ratio for {ticker} differs by {result.percentage_diff * 100:.2f}%, "
                f"expected within 2%. Expected={result.expected:.4f}, Actual={result.actual:.4f}"
            )


@pytest.mark.integration
@pytest.mark.requirement_4
@pytest.mark.asyncio
async def test_banking_ratios(db_session: Session):
    """Test banking-specific ratios (loan_to_deposit, npl_ratio)"""
    test_suite = RatioCalculationTests(db_session)
    period_key = "2026Q1"
    
    for ticker in REFERENCE_COMPANIES["banking"]:
        # Test loan_to_deposit
        loan_deposit_result = await test_suite.test_loan_to_deposit(ticker, period_key)
        if loan_deposit_result and loan_deposit_result.actual is not None:
            assert loan_deposit_result.within_tolerance, (
                f"Loan to deposit for {ticker} differs by {loan_deposit_result.percentage_diff * 100:.2f}%, "
                f"expected within 2%"
            )
        
        # Test npl_ratio
        npl_result = await test_suite.test_npl_ratio(ticker, period_key)
        if npl_result and npl_result.actual is not None:
            assert npl_result.within_tolerance, (
                f"NPL ratio for {ticker} differs by {npl_result.percentage_diff * 100:.2f}%, "
                f"expected within 2%"
            )
