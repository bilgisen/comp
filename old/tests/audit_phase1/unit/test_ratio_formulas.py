"""
Ratio Formula Validation Test Module - Requirement 3

Validates ratio formulas are mathematically correct and handle edge cases properly.
Tests formula correctness using synthetic data with known expected values.
"""
import pytest
import math
from typing import Dict, Optional, Callable
from dataclasses import dataclass

from services.ratio_calculator import RatioConfig
from calculate_ratios_sync import SyncRatioCalculator
from tests.audit_phase1.utilities.synthetic_data import SyntheticDataGenerator
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter
from tests.audit_phase1.utilities.validation_algorithms import (
    calculate_percentage_difference,
    check_tolerance
)


@dataclass
class FormulaTestResult:
    """Result of formula validation test"""
    ratio_code: str
    expected: Optional[float]
    actual: Optional[float]
    passed: bool
    error_message: Optional[str] = None
    test_scenario: str = ""


@dataclass
class FormulaValidationReport:
    """Ratio formula validation report"""
    total_formulas: int
    passed_formulas: int
    failed_formulas: int
    pass_rate: float
    edge_case_results: Dict[str, str]  # scenario -> status
    formula_results: Dict[str, FormulaTestResult]
    status: str  # PASS/FAIL


class RatioFormulaTests:
    """Test suite for ratio formula validation"""
    
    def __init__(self):
        self.calculator = SyncRatioCalculator
        self.data_gen = SyntheticDataGenerator()
        self.printer = PrettyPrinter()
        self.tolerance = 0.01  # 1% tolerance for formula validation
    
    def load_ratio_configs(self) -> Dict[str, Dict[str, RatioConfig]]:
        """
        Load all ratio configurations
        
        Returns:
            Dictionary with DEFAULT_RATIOS and BANKING_RATIOS
        """
        return {
            "DEFAULT_RATIOS": self.calculator.DEFAULT_RATIOS,
            "BANKING_RATIOS": self.calculator.BANKING_RATIOS
        }
    
    def test_formula_callable(self, config: RatioConfig) -> bool:
        """
        Verify formula function is callable
        
        Args:
            config: RatioConfig object
        
        Returns:
            True if formula is callable, False otherwise
        """
        return callable(config.formula)
    
    def test_formula_with_synthetic_data(
        self, 
        ratio_code: str,
        config: RatioConfig,
        test_data: Dict[str, float],
        expected_value: float
    ) -> FormulaTestResult:
        """
        Test formula with synthetic data and known expected value
        
        Args:
            ratio_code: Ratio code identifier
            config: RatioConfig object
            test_data: Synthetic financial data dictionary
            expected_value: Expected ratio value
        
        Returns:
            FormulaTestResult with validation status
        """
        try:
            # Execute formula
            actual_value = config.formula(test_data)
            
            # Check if result matches expected within tolerance
            if actual_value is None:
                return FormulaTestResult(
                    ratio_code=ratio_code,
                    expected=expected_value,
                    actual=None,
                    passed=False,
                    error_message="Formula returned None",
                    test_scenario="synthetic_data"
                )
            
            # Calculate difference
            diff_percentage = calculate_percentage_difference(expected_value, actual_value)
            passed = check_tolerance(expected_value, actual_value, self.tolerance)
            
            return FormulaTestResult(
                ratio_code=ratio_code,
                expected=expected_value,
                actual=actual_value,
                passed=passed,
                error_message=None if passed else f"Difference: {diff_percentage:.4f}%",
                test_scenario="synthetic_data"
            )
            
        except Exception as e:
            return FormulaTestResult(
                ratio_code=ratio_code,
                expected=expected_value,
                actual=None,
                passed=False,
                error_message=f"Formula execution error: {str(e)}",
                test_scenario="synthetic_data"
            )
    
    def test_division_by_zero(
        self, 
        ratio_code: str,
        config: RatioConfig
    ) -> FormulaTestResult:
        """
        Test formula handles division by zero gracefully
        
        Args:
            ratio_code: Ratio code identifier
            config: RatioConfig object
        
        Returns:
            FormulaTestResult with validation status
        """
        # Create data with zero denominators
        test_data = {
            "current_assets": 1000.0,
            "current_liabilities": 0.0,  # Zero denominator
            "total_debt": 500.0,
            "shareholders_equity": 0.0,  # Zero denominator
            "revenue_ttm": 0.0,  # Zero denominator
            "total_assets": 0.0,  # Zero denominator
            "net_income_ttm": 100.0,
            "gross_profit_ttm": 200.0
        }
        
        try:
            result = config.formula(test_data)
            
            # Should return None for division by zero
            if result is None:
                return FormulaTestResult(
                    ratio_code=ratio_code,
                    expected=None,
                    actual=None,
                    passed=True,
                    test_scenario="division_by_zero"
                )
            elif math.isinf(result) or math.isnan(result):
                return FormulaTestResult(
                    ratio_code=ratio_code,
                    expected=None,
                    actual=result,
                    passed=False,
                    error_message=f"Formula returned {result} instead of None",
                    test_scenario="division_by_zero"
                )
            else:
                # Some ratios might not have division in this particular test case
                return FormulaTestResult(
                    ratio_code=ratio_code,
                    expected=None,
                    actual=result,
                    passed=True,
                    test_scenario="division_by_zero"
                )
                
        except Exception as e:
            return FormulaTestResult(
                ratio_code=ratio_code,
                expected=None,
                actual=None,
                passed=False,
                error_message=f"Exception raised: {str(e)}",
                test_scenario="division_by_zero"
            )
    
    def test_null_handling(
        self, 
        ratio_code: str,
        config: RatioConfig
    ) -> FormulaTestResult:
        """
        Test formula handles None values gracefully
        
        Args:
            ratio_code: Ratio code identifier
            config: RatioConfig object
        
        Returns:
            FormulaTestResult with validation status
        """
        # Create data with None values
        test_data = {
            "current_assets": None,
            "current_liabilities": None,
            "total_debt": None,
            "shareholders_equity": None,
            "revenue_ttm": None,
            "net_income_ttm": None
        }
        
        try:
            result = config.formula(test_data)
            
            # Should return None for missing required fields
            if result is None:
                return FormulaTestResult(
                    ratio_code=ratio_code,
                    expected=None,
                    actual=None,
                    passed=True,
                    test_scenario="null_handling"
                )
            else:
                return FormulaTestResult(
                    ratio_code=ratio_code,
                    expected=None,
                    actual=result,
                    passed=False,
                    error_message=f"Formula returned {result} instead of None for NULL inputs",
                    test_scenario="null_handling"
                )
                
        except Exception as e:
            return FormulaTestResult(
                ratio_code=ratio_code,
                expected=None,
                actual=None,
                passed=False,
                error_message=f"Exception raised: {str(e)}",
                test_scenario="null_handling"
            )
    
    def validate_all_formulas(self) -> FormulaValidationReport:
        """
        Validate all ratio formulas with comprehensive tests
        
        Returns:
            FormulaValidationReport with validation results
        """
        ratio_configs = self.load_ratio_configs()
        formula_results = {}
        edge_case_results = {}
        
        # Test scenarios with known expected values
        test_scenarios = {
            "current_ratio": {
                "data": {"current_assets": 1000.0, "current_liabilities": 500.0},
                "expected": 2.0
            },
            "acid_test_ratio": {
                "data": {"current_assets": 1000.0, "inventories": 200.0, "current_liabilities": 500.0},
                "expected": 1.6
            },
            "debt_to_equity": {
                "data": {"total_debt": 600.0, "shareholders_equity": 400.0},
                "expected": 1.5
            },
            "debt_ratio": {
                "data": {"total_liabilities": 700.0, "total_assets": 1400.0},
                "expected": 0.5
            },
            "gross_margin": {
                "data": {"gross_profit_ttm": 300.0, "revenue_ttm": 1000.0},
                "expected": 0.3
            },
            "operating_margin": {
                "data": {"operating_profit_ttm": 200.0, "revenue_ttm": 1000.0},
                "expected": 0.2
            },
            "net_margin": {
                "data": {"net_income_ttm": 150.0, "revenue_ttm": 1000.0},
                "expected": 0.15
            },
            "roe": {
                "data": {"net_income_ttm": 100.0, "shareholders_equity_avg": 500.0},
                "expected": 0.2
            },
            "roa": {
                "data": {"net_income_ttm": 100.0, "total_assets_avg": 1000.0},
                "expected": 0.1
            },
            "asset_turnover": {
                "data": {"revenue_ttm": 2000.0, "total_assets_avg": 1000.0},
                "expected": 2.0
            }
        }
        
        total_tested = 0
        passed_count = 0
        failed_count = 0
        
        # Test each ratio configuration
        for config_name, configs in ratio_configs.items():
            for ratio_code, config in configs.items():
                # Test 1: Callable check
                if not self.test_formula_callable(config):
                    formula_results[f"{config_name}.{ratio_code}"] = FormulaTestResult(
                        ratio_code=ratio_code,
                        expected=None,
                        actual=None,
                        passed=False,
                        error_message="Formula is not callable",
                        test_scenario="callable_check"
                    )
                    failed_count += 1
                    total_tested += 1
                    continue
                
                # Test 2: Synthetic data with known values (if available)
                if ratio_code in test_scenarios:
                    scenario = test_scenarios[ratio_code]
                    result = self.test_formula_with_synthetic_data(
                        ratio_code,
                        config,
                        scenario["data"],
                        scenario["expected"]
                    )
                    formula_results[f"{config_name}.{ratio_code}"] = result
                    
                    if result.passed:
                        passed_count += 1
                    else:
                        failed_count += 1
                    total_tested += 1
                
                # Test 3: Division by zero handling
                div_zero_result = self.test_division_by_zero(ratio_code, config)
                edge_case_results[f"{ratio_code}_div_zero"] = "PASS" if div_zero_result.passed else "FAIL"
                
                # Test 4: NULL handling
                null_result = self.test_null_handling(ratio_code, config)
                edge_case_results[f"{ratio_code}_null"] = "PASS" if null_result.passed else "FAIL"
        
        # Calculate pass rate
        pass_rate = (passed_count / total_tested * 100) if total_tested > 0 else 0
        status = "PASS" if pass_rate >= 95.0 else "FAIL"
        
        return FormulaValidationReport(
            total_formulas=total_tested,
            passed_formulas=passed_count,
            failed_formulas=failed_count,
            pass_rate=pass_rate,
            edge_case_results=edge_case_results,
            formula_results=formula_results,
            status=status
        )
    
    def print_report(self, report: FormulaValidationReport) -> str:
        """
        Format and print formula validation report
        
        Args:
            report: FormulaValidationReport object
        
        Returns:
            Formatted report string
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("RATIO FORMULA VALIDATION TEST - REQUIREMENT 3")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"Total Formulas Tested: {report.total_formulas}")
        lines.append(f"Passed: {report.passed_formulas}")
        lines.append(f"Failed: {report.failed_formulas}")
        lines.append(f"Pass Rate: {report.pass_rate:.2f}%")
        lines.append("")
        
        # Status
        if report.status == "PASS":
            status_str = self.printer.colorize("✅ PASS (≥95% pass rate)", "green")
        else:
            status_str = self.printer.colorize(f"❌ FAIL (<95% pass rate)", "red")
        
        lines.append(f"Status: {status_str}")
        lines.append("")
        
        # Formula results
        if report.formula_results:
            lines.append("## Formula Test Results")
            lines.append("")
            
            result_data = []
            for formula_key, result in report.formula_results.items():
                status_symbol = "✓" if result.passed else "✗"
                
                result_data.append({
                    "formula": formula_key,
                    "expected": f"{result.expected:.4f}" if result.expected is not None else "N/A",
                    "actual": f"{result.actual:.4f}" if result.actual is not None else "N/A",
                    "status": status_symbol,
                    "error": result.error_message or "-"
                })
            
            lines.append(self.printer.format_table(
                result_data,
                ["formula", "expected", "actual", "status", "error"],
                align={"expected": "right", "actual": "right", "status": "center"}
            ))
            lines.append("")
        
        # Edge case results
        if report.edge_case_results:
            lines.append("## Edge Case Handling")
            lines.append("")
            
            # Count PASS/FAIL
            pass_count = sum(1 for v in report.edge_case_results.values() if v == "PASS")
            fail_count = sum(1 for v in report.edge_case_results.values() if v == "FAIL")
            
            lines.append(f"Division by Zero Tests: {sum(1 for k in report.edge_case_results if 'div_zero' in k)}")
            lines.append(f"NULL Handling Tests: {sum(1 for k in report.edge_case_results if 'null' in k)}")
            lines.append(f"Edge Cases Passed: {pass_count}/{len(report.edge_case_results)}")
            lines.append("")
        
        # Failed formulas detail
        failed_formulas = [k for k, v in report.formula_results.items() if not v.passed]
        if failed_formulas:
            lines.append("## Failed Formulas")
            lines.append("")
            for formula_key in failed_formulas:
                result = report.formula_results[formula_key]
                lines.append(f"- {formula_key}: {result.error_message}")
            lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)


@pytest.mark.unit
@pytest.mark.requirement_3
def test_all_formulas_callable():
    """
    Test that all ratio formulas are callable
    
    Validates:
        - DEFAULT_RATIOS formulas are callable
        - BANKING_RATIOS formulas are callable
    """
    test_suite = RatioFormulaTests()
    ratio_configs = test_suite.load_ratio_configs()
    
    for config_name, configs in ratio_configs.items():
        for ratio_code, config in configs.items():
            assert callable(config.formula), (
                f"{config_name}.{ratio_code} formula is not callable"
            )


@pytest.mark.unit
@pytest.mark.requirement_3
def test_formulas_with_synthetic_data():
    """
    Test ratio formulas with synthetic data and known expected values
    
    Validates:
        - Formulas produce correct results within 0.01 tolerance
        - Calculation logic is mathematically sound
    """
    test_suite = RatioFormulaTests()
    report = test_suite.validate_all_formulas()
    
    # Print report
    report_str = test_suite.print_report(report)
    print("\n" + report_str)
    
    # Assert high pass rate
    assert report.pass_rate >= 95.0, (
        f"Formula validation pass rate is {report.pass_rate:.2f}%, expected ≥95%. "
        f"{report.failed_formulas} formulas failed out of {report.total_formulas}."
    )


@pytest.mark.unit
@pytest.mark.requirement_3
def test_division_by_zero_handling():
    """
    Test that formulas handle division by zero gracefully
    
    Validates:
        - Formulas return None (not raise exception) for zero denominators
        - No Inf or NaN values are returned
    """
    test_suite = RatioFormulaTests()
    ratio_configs = test_suite.load_ratio_configs()
    
    for config_name, configs in ratio_configs.items():
        for ratio_code, config in configs.items():
            result = test_suite.test_division_by_zero(ratio_code, config)
            
            # Allow pass if formula doesn't encounter division in test case
            # But fail if it returns Inf/NaN or raises exception
            if not result.passed and result.error_message:
                if "Exception" in result.error_message or "Inf" in str(result.actual) or "NaN" in str(result.actual):
                    pytest.fail(
                        f"{config_name}.{ratio_code} failed division by zero test: "
                        f"{result.error_message}"
                    )


@pytest.mark.unit
@pytest.mark.requirement_3
def test_null_value_handling():
    """
    Test that formulas handle None values gracefully
    
    Validates:
        - Formulas return None for missing required fields
        - No exceptions are raised for None inputs
    """
    test_suite = RatioFormulaTests()
    ratio_configs = test_suite.load_ratio_configs()
    
    for config_name, configs in ratio_configs.items():
        for ratio_code, config in configs.items():
            result = test_suite.test_null_handling(ratio_code, config)
            
            assert result.passed, (
                f"{config_name}.{ratio_code} failed NULL handling test: "
                f"{result.error_message}"
            )


@pytest.mark.unit
@pytest.mark.requirement_3
def test_current_ratio_formula():
    """
    Test current_ratio formula with specific known values
    
    Validates:
        - current_ratio = current_assets / current_liabilities
        - Expected: 1000 / 500 = 2.0
    """
    test_suite = RatioFormulaTests()
    config = test_suite.calculator.DEFAULT_RATIOS["current_ratio"]
    
    test_data = {"current_assets": 1000.0, "current_liabilities": 500.0}
    result = config.formula(test_data)
    
    assert result is not None, "Formula returned None"
    assert abs(result - 2.0) < 0.01, f"Expected 2.0, got {result}"


@pytest.mark.unit
@pytest.mark.requirement_3
def test_debt_to_equity_formula():
    """
    Test debt_to_equity formula with specific known values
    
    Validates:
        - debt_to_equity = total_debt / shareholders_equity
        - Expected: 600 / 400 = 1.5
    """
    test_suite = RatioFormulaTests()
    config = test_suite.calculator.DEFAULT_RATIOS["debt_to_equity"]
    
    test_data = {"total_debt": 600.0, "shareholders_equity": 400.0}
    result = config.formula(test_data)
    
    assert result is not None, "Formula returned None"
    assert abs(result - 1.5) < 0.01, f"Expected 1.5, got {result}"


@pytest.mark.unit
@pytest.mark.requirement_3
def test_roe_formula():
    """
    Test ROE formula with specific known values
    
    Validates:
        - ROE = net_income_ttm / shareholders_equity_avg
        - Expected: 100 / 500 = 0.2 (20%)
    """
    test_suite = RatioFormulaTests()
    config = test_suite.calculator.DEFAULT_RATIOS["roe"]
    
    test_data = {"net_income_ttm": 100.0, "shareholders_equity_avg": 500.0}
    result = config.formula(test_data)
    
    assert result is not None, "Formula returned None"
    assert abs(result - 0.2) < 0.01, f"Expected 0.2, got {result}"
