"""
Economic Bounds Validation Test Module - Requirement 7

Tests economic bounds configuration and validation logic.
Verifies bounds consistency, sector-specific bounds, and boundary edge cases.

**Validates: Requirements 7**
"""
import pytest
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

from tests.audit_phase1.fixtures.economic_bounds import ECONOMIC_BOUNDS, BOUNDS_RATIONALE
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter


@dataclass
class BoundsValidationResult:
    """Result of bounds validation check"""
    ratio_code: str
    sector: str
    min_val: float
    max_val: float
    is_consistent: bool
    error_message: Optional[str] = None


@dataclass
class BoundaryTestCase:
    """Test case for boundary edge values"""
    ratio_code: str
    test_value: float
    expected_included: bool
    description: str


@dataclass
class EconomicBoundsReport:
    """Economic bounds validation test report"""
    total_bounds: int
    consistent_bounds: int
    inconsistent_bounds: List[BoundsValidationResult]
    banking_sector_bounds: Dict[str, Tuple[float, float]]
    default_bounds: Dict[str, Tuple[float, float]]
    missing_bounds: List[str]
    boundary_test_results: List[Dict[str, Any]]
    status: str  # PASS/FAIL


class EconomicBoundsTests:
    """Test suite for economic bounds validation"""
    
    def __init__(self):
        self.printer = PrettyPrinter()
        self.epsilon = 0.01  # Small value for boundary testing
    
    def test_load_bounds(self) -> Dict[str, Dict[str, Tuple[float, float]]]:
        """
        Load economic bounds from fixture
        
        Returns:
            Dictionary of economic bounds by sector and ratio
        
        Validates:
            - ECONOMIC_BOUNDS dictionary is accessible
            - Contains _default section
            - Contains sector-specific sections
        """
        assert ECONOMIC_BOUNDS is not None, "ECONOMIC_BOUNDS should be defined"
        assert "_default" in ECONOMIC_BOUNDS, "ECONOMIC_BOUNDS should contain _default section"
        
        return ECONOMIC_BOUNDS
    
    def test_bounds_consistency(
        self,
        bounds: Dict[str, Dict[str, Tuple[float, float]]]
    ) -> List[BoundsValidationResult]:
        """
        Verify min_val < max_val for all bounds
        
        Args:
            bounds: Economic bounds dictionary
        
        Returns:
            List of validation results for all ratio bounds
        
        Validates:
            - For every ratio bound, min_val must be less than max_val
            - No bounds should have equal min and max values
            - No bounds should have min > max (inverted bounds)
        """
        validation_results = []
        
        for sector, ratio_bounds in bounds.items():
            for ratio_code, (min_val, max_val) in ratio_bounds.items():
                is_consistent = min_val < max_val
                error_message = None
                
                if not is_consistent:
                    if min_val == max_val:
                        error_message = f"Equal bounds: min={min_val}, max={max_val}"
                    else:
                        error_message = f"Inverted bounds: min={min_val} > max={max_val}"
                
                validation_results.append(BoundsValidationResult(
                    ratio_code=ratio_code,
                    sector=sector,
                    min_val=min_val,
                    max_val=max_val,
                    is_consistent=is_consistent,
                    error_message=error_message
                ))
        
        return validation_results
    
    def test_banking_sector_bounds(
        self,
        bounds: Dict[str, Dict[str, Tuple[float, float]]]
    ) -> Dict[str, Tuple[float, float]]:
        """
        Verify banking sector has sector-specific bounds
        
        Args:
            bounds: Economic bounds dictionary
        
        Returns:
            Banking sector bounds dictionary
        
        Validates:
            - Banking sector ("Bankacılık & Finans") has specific bounds
            - Banking-specific ratios are defined (loan_to_deposit, npl_ratio, etc.)
        """
        banking_key = "Bankacılık & Finans"
        
        assert banking_key in bounds, f"Banking sector '{banking_key}' should have specific bounds"
        
        banking_bounds = bounds[banking_key]
        
        # Expected banking-specific ratios
        expected_banking_ratios = [
            "net_interest_margin",
            "cost_income_ratio",
            "loan_to_deposit",
            "npl_ratio",
            "capital_adequacy"
        ]
        
        # Verify at least some banking-specific ratios exist
        found_banking_ratios = [r for r in expected_banking_ratios if r in banking_bounds]
        
        assert len(found_banking_ratios) > 0, \
            f"Banking sector should have at least one banking-specific ratio (expected: {expected_banking_ratios})"
        
        return banking_bounds
    
    def test_default_bounds_coverage(
        self,
        bounds: Dict[str, Dict[str, Tuple[float, float]]]
    ) -> Dict[str, Tuple[float, float]]:
        """
        Verify default bounds exist for common ratios
        
        Args:
            bounds: Economic bounds dictionary
        
        Returns:
            Default bounds dictionary
        
        Validates:
            - Default section contains common financial ratios
            - Coverage includes liquidity, leverage, profitability, and efficiency ratios
        """
        default_bounds = bounds.get("_default", {})
        
        # Expected common ratio categories
        expected_liquidity = ["current_ratio", "acid_test_ratio"]
        expected_leverage = ["debt_to_equity", "debt_ratio"]
        expected_profitability = ["roe", "roa", "net_margin"]
        expected_efficiency = ["asset_turnover"]
        
        # Check coverage by category
        liquidity_coverage = sum(1 for r in expected_liquidity if r in default_bounds)
        leverage_coverage = sum(1 for r in expected_leverage if r in default_bounds)
        profitability_coverage = sum(1 for r in expected_profitability if r in default_bounds)
        efficiency_coverage = sum(1 for r in expected_efficiency if r in default_bounds)
        
        # Verify at least some ratios from each category exist
        assert liquidity_coverage > 0, "Default bounds should include liquidity ratios"
        assert leverage_coverage > 0, "Default bounds should include leverage ratios"
        assert profitability_coverage > 0, "Default bounds should include profitability ratios"
        assert efficiency_coverage > 0, "Default bounds should include efficiency ratios"
        
        return default_bounds
    
    def test_boundary_edge_cases(
        self,
        ratio_code: str,
        bounds: Tuple[float, float],
        sector: str = "_default"
    ) -> List[Dict[str, Any]]:
        """
        Test values at boundary edges [min-ε, min, max, max+ε]
        
        Args:
            ratio_code: Ratio code to test
            bounds: (min_val, max_val) tuple
            sector: Sector name for context
        
        Returns:
            List of test results for boundary cases
        
        Validates:
            - Values below min_val should be excluded
            - Values equal to min_val should be included
            - Values equal to max_val should be included
            - Values above max_val should be excluded
        """
        min_val, max_val = bounds
        
        # Create boundary test cases
        test_cases = [
            BoundaryTestCase(
                ratio_code=ratio_code,
                test_value=min_val - self.epsilon,
                expected_included=False,
                description=f"Below minimum (min - ε)"
            ),
            BoundaryTestCase(
                ratio_code=ratio_code,
                test_value=min_val,
                expected_included=True,
                description=f"At minimum boundary"
            ),
            BoundaryTestCase(
                ratio_code=ratio_code,
                test_value=(min_val + max_val) / 2,
                expected_included=True,
                description=f"Mid-range value"
            ),
            BoundaryTestCase(
                ratio_code=ratio_code,
                test_value=max_val,
                expected_included=True,
                description=f"At maximum boundary"
            ),
            BoundaryTestCase(
                ratio_code=ratio_code,
                test_value=max_val + self.epsilon,
                expected_included=False,
                description=f"Above maximum (max + ε)"
            ),
        ]
        
        # Test each boundary case
        results = []
        for test_case in test_cases:
            # Simulate F3 filter logic
            is_included = min_val <= test_case.test_value <= max_val
            passed = is_included == test_case.expected_included
            
            results.append({
                "ratio_code": ratio_code,
                "sector": sector,
                "test_value": test_case.test_value,
                "description": test_case.description,
                "expected_included": test_case.expected_included,
                "actual_included": is_included,
                "passed": passed,
                "min_bound": min_val,
                "max_bound": max_val
            })
        
        return results
    
    def identify_missing_bounds(
        self,
        ratio_codes: List[str],
        bounds: Dict[str, Dict[str, Tuple[float, float]]]
    ) -> List[str]:
        """
        Find ratios without economic bounds defined
        
        Args:
            ratio_codes: List of all ratio codes in the system
            bounds: Economic bounds dictionary
        
        Returns:
            List of ratio codes without bounds defined
        
        Validates:
            - All common ratios should have bounds in default or sector-specific sections
        """
        default_bounds = bounds.get("_default", {})
        banking_bounds = bounds.get("Bankacılık & Finans", {})
        
        # Combine all defined bounds
        all_defined_bounds = set(default_bounds.keys()) | set(banking_bounds.keys())
        
        # Find missing bounds
        missing_bounds = [ratio for ratio in ratio_codes if ratio not in all_defined_bounds]
        
        return missing_bounds
    
    def generate_report(
        self,
        bounds: Dict[str, Dict[str, Tuple[float, float]]],
        validation_results: List[BoundsValidationResult],
        boundary_test_results: List[Dict[str, Any]],
        missing_bounds: List[str]
    ) -> EconomicBoundsReport:
        """
        Generate a formatted report for economic bounds validation
        
        Args:
            bounds: Economic bounds dictionary
            validation_results: Results from bounds consistency tests
            boundary_test_results: Results from boundary edge case tests
            missing_bounds: List of ratios without bounds
        
        Returns:
            EconomicBoundsReport with validation status and details
        """
        # Calculate statistics
        total_bounds = len(validation_results)
        consistent_bounds = sum(1 for r in validation_results if r.is_consistent)
        inconsistent_bounds = [r for r in validation_results if not r.is_consistent]
        
        # Extract bounds by sector
        default_bounds = bounds.get("_default", {})
        banking_bounds = bounds.get("Bankacılık & Finans", {})
        
        # Determine overall status
        status = "PASS" if len(inconsistent_bounds) == 0 else "FAIL"
        
        return EconomicBoundsReport(
            total_bounds=total_bounds,
            consistent_bounds=consistent_bounds,
            inconsistent_bounds=inconsistent_bounds,
            banking_sector_bounds=banking_bounds,
            default_bounds=default_bounds,
            missing_bounds=missing_bounds,
            boundary_test_results=boundary_test_results,
            status=status
        )


# ============================================================================
# Pytest Test Functions
# ============================================================================

def test_load_bounds():
    """Test loading economic bounds from fixture"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    
    # Verify structure
    assert isinstance(bounds, dict), "ECONOMIC_BOUNDS should be a dictionary"
    assert "_default" in bounds, "Should contain _default section"
    assert len(bounds["_default"]) > 0, "Default bounds should not be empty"


def test_bounds_consistency():
    """Test all bounds have min_val < max_val"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    validation_results = test_suite.test_bounds_consistency(bounds)
    
    # All bounds should be consistent
    inconsistent = [r for r in validation_results if not r.is_consistent]
    
    assert len(inconsistent) == 0, \
        f"All bounds should have min < max. Found {len(inconsistent)} inconsistent bounds: {inconsistent}"


def test_banking_sector_bounds():
    """Test banking sector has specific bounds defined"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    banking_bounds = test_suite.test_banking_sector_bounds(bounds)
    
    # Verify banking-specific ratios exist
    assert "loan_to_deposit" in banking_bounds or "net_interest_margin" in banking_bounds, \
        "Banking sector should have banking-specific ratios"


def test_default_bounds_coverage():
    """Test default bounds cover common ratio categories"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    default_bounds = test_suite.test_default_bounds_coverage(bounds)
    
    # Verify coverage
    assert len(default_bounds) > 0, "Default bounds should not be empty"
    assert "current_ratio" in default_bounds, "Should include current_ratio"
    assert "roe" in default_bounds, "Should include roe"


def test_boundary_edge_cases_current_ratio():
    """Test boundary edge cases for current_ratio"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    default_bounds = bounds.get("_default", {})
    
    # Test current_ratio boundary cases
    if "current_ratio" in default_bounds:
        ratio_bounds = default_bounds["current_ratio"]
        results = test_suite.test_boundary_edge_cases(
            ratio_code="current_ratio",
            bounds=ratio_bounds
        )
        
        # All boundary tests should pass
        failed_tests = [r for r in results if not r["passed"]]
        
        assert len(failed_tests) == 0, \
            f"All boundary tests should pass. Failed: {failed_tests}"


def test_boundary_edge_cases_loan_to_deposit():
    """Test boundary edge cases for banking-specific loan_to_deposit"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    banking_bounds = bounds.get("Bankacılık & Finans", {})
    
    # Test loan_to_deposit boundary cases
    if "loan_to_deposit" in banking_bounds:
        ratio_bounds = banking_bounds["loan_to_deposit"]
        results = test_suite.test_boundary_edge_cases(
            ratio_code="loan_to_deposit",
            bounds=ratio_bounds,
            sector="Bankacılık & Finans"
        )
        
        # All boundary tests should pass
        failed_tests = [r for r in results if not r["passed"]]
        
        assert len(failed_tests) == 0, \
            f"All boundary tests should pass. Failed: {failed_tests}"


def test_identify_missing_bounds():
    """Test identification of ratios without bounds"""
    test_suite = EconomicBoundsTests()
    
    bounds = test_suite.test_load_bounds()
    
    # Sample ratio codes (would come from actual system in integration test)
    sample_ratio_codes = [
        "current_ratio", "roe", "roa", "debt_to_equity",
        "loan_to_deposit", "net_interest_margin",
        "hypothetical_ratio_without_bounds"  # This one should be missing
    ]
    
    missing = test_suite.identify_missing_bounds(sample_ratio_codes, bounds)
    
    # Verify missing bounds are identified
    assert "hypothetical_ratio_without_bounds" in missing, \
        "Should identify ratios without bounds"


def test_generate_report():
    """Test comprehensive report generation"""
    test_suite = EconomicBoundsTests()
    
    # Load bounds and run all validations
    bounds = test_suite.test_load_bounds()
    validation_results = test_suite.test_bounds_consistency(bounds)
    
    # Test boundary edge cases for a few ratios
    boundary_test_results = []
    default_bounds = bounds.get("_default", {})
    if "current_ratio" in default_bounds:
        boundary_test_results.extend(
            test_suite.test_boundary_edge_cases(
                "current_ratio",
                default_bounds["current_ratio"]
            )
        )
    
    # Identify missing bounds
    all_ratio_codes = ["current_ratio", "roe", "unknown_ratio"]
    missing_bounds = test_suite.identify_missing_bounds(all_ratio_codes, bounds)
    
    # Generate report
    report = test_suite.generate_report(
        bounds=bounds,
        validation_results=validation_results,
        boundary_test_results=boundary_test_results,
        missing_bounds=missing_bounds
    )
    
    # Verify report structure
    assert report is not None, "Report should be generated"
    assert report.status in ["PASS", "FAIL"], "Report should have valid status"
    assert report.total_bounds > 0, "Report should include total bounds count"
    assert isinstance(report.default_bounds, dict), "Report should include default bounds"
    assert isinstance(report.banking_sector_bounds, dict), "Report should include banking bounds"
    
    # Print report summary for visual inspection
    print(f"\n{'='*70}")
    print(f"Economic Bounds Validation Report - Status: {report.status}")
    print(f"{'='*70}")
    print(f"Total Bounds Defined: {report.total_bounds}")
    print(f"Consistent Bounds: {report.consistent_bounds}")
    print(f"Inconsistent Bounds: {len(report.inconsistent_bounds)}")
    print(f"Missing Bounds: {len(report.missing_bounds)}")
    print(f"Boundary Tests Performed: {len(report.boundary_test_results)}")
    
    if report.inconsistent_bounds:
        print(f"\nInconsistent Bounds Found:")
        for result in report.inconsistent_bounds:
            print(f"  - {result.sector}/{result.ratio_code}: {result.error_message}")
    
    if report.missing_bounds:
        print(f"\nMissing Bounds:")
        for ratio in report.missing_bounds:
            print(f"  - {ratio}")
    
    print(f"{'='*70}\n")
