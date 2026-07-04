"""
Filter Pipeline Test Module - Requirement 6

Tests the F1-F5 filter pipeline for benchmark peer validation.
Verifies each filter stage correctly validates peer data using synthetic test cases.

**Validates: Requirements 6**
"""
import pytest
import math
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass

from tests.audit_phase1.utilities.synthetic_data import generate_peer_data
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter
from tests.audit_phase1.fixtures.economic_bounds import ECONOMIC_BOUNDS


@dataclass
class FilterStageResult:
    """Result of a single filter stage"""
    stage: str
    peers_input: int
    peers_output: int
    excluded_count: int
    excluded_reasons: List[str]
    passed: bool


@dataclass 
class FilterPipelineReport:
    """F1-F5 filter pipeline test report"""
    total_peers_input: int
    f1_excluded: int
    f2_excluded: int
    f3_excluded: int
    f4_winsorized: int
    f5_rejected: int
    final_peers: int
    exclusion_rates: Dict[str, float]
    stage_results: List[FilterStageResult]
    status: str  # PASS/FAIL


class FilterPipelineTests:
    """Test suite for F1-F5 filter pipeline validation"""
    
    def __init__(self):
        self.printer = PrettyPrinter()
        self.min_periods = 3  # Minimum required periods for F2
        self.min_peers = 3    # Minimum required peers for F5

    def test_create_synthetic_peers(
        self,
        scenario: str = "valid",
        n_peers: int = 10,
        ratio_code: str = "current_ratio"
    ) -> List[Dict[str, Any]]:
        """
        Generate test scenarios with known characteristics
        
        Args:
            scenario: Test scenario ("valid", "with_nulls", "with_outliers", 
                     "insufficient_periods", "too_few")
            n_peers: Number of peer companies to generate
            ratio_code: Ratio code being tested
        
        Returns:
            List of peer data dictionaries
        
        Scenarios:
            - "valid": All valid data, should pass all filters
            - "with_nulls": Contains NULL and infinite values (F1 should exclude)
            - "with_outliers": Contains extreme outliers (F3 should exclude, F4 should winsorize)
            - "insufficient_periods": Some peers with < minimum periods (F2 should exclude)
            - "too_few": Fewer than 3 peers (F5 should reject)
        """
        return generate_peer_data(
            scenario=scenario,
            n_peers=n_peers,
            ratio_code=ratio_code,
            seed=42  # Fixed seed for reproducibility
        )
    
    def test_f1_null_filter(
        self,
        peers: List[Dict[str, Any]]
    ) -> FilterStageResult:
        """
        Verify NULL and infinite value exclusion
        
        F1 Filter Rules:
            - Exclude if value is None
            - Exclude if value is infinite (math.isinf)
            - Exclude if value is NaN (math.isnan)
        
        Args:
            peers: List of peer data dictionaries
        
        Returns:
            FilterStageResult with F1 validation status
        """
        included = []
        excluded = []
        
        for peer in peers:
            value = peer["ratio_value"]
            ticker = peer["ticker"]
            
            # F1: NULL / Infinite values
            if value is None or not math.isfinite(value):
                excluded.append({
                    "ticker": ticker,
                    "value": value,
                    "reason": "F1_NULL_OR_INFINITE"
                })
            else:
                included.append(peer)
        
        # Determine if test passed (depends on scenario)
        # For "with_nulls" scenario, we expect exclusions
        passed = True  # Will be evaluated by caller based on scenario
        
        return FilterStageResult(
            stage="F1_NULL_FILTER",
            peers_input=len(peers),
            peers_output=len(included),
            excluded_count=len(excluded),
            excluded_reasons=[e["reason"] for e in excluded],
            passed=passed
        )
    
    def test_f2_period_filter(
        self,
        peers: List[Dict[str, Any]],
        min_periods: int = 3
    ) -> FilterStageResult:
        """
        Verify insufficient period exclusion
        
        F2 Filter Rules:
            - Exclude if available_periods < min_periods
            - Default min_periods = 3 (requires at least 3 periods of data)
        
        Args:
            peers: List of peer data dictionaries
            min_periods: Minimum required periods
        
        Returns:
            FilterStageResult with F2 validation status
        """
        included = []
        excluded = []
        
        for peer in peers:
            ticker = peer["ticker"]
            value = peer["ratio_value"]
            available_periods = peer.get("available_periods", 0)
            
            # F2: Minimum reporting periods
            if available_periods < min_periods:
                excluded.append({
                    "ticker": ticker,
                    "value": value,
                    "reason": f"F2_INSUFFICIENT_PERIODS({available_periods}<{min_periods})"
                })
            else:
                included.append(peer)
        
        passed = True
        
        return FilterStageResult(
            stage="F2_PERIOD_FILTER",
            peers_input=len(peers),
            peers_output=len(included),
            excluded_count=len(excluded),
            excluded_reasons=[e["reason"] for e in excluded],
            passed=passed
        )
    
    def test_f3_economic_bounds(
        self,
        peers: List[Dict[str, Any]],
        ratio_code: str,
        sector_main: str = "Teknoloji & İletişim"
    ) -> FilterStageResult:
        """
        Verify bounds-based exclusion
        
        F3 Filter Rules:
            - Exclude if value < min_bound
            - Exclude if value > max_bound
            - Use sector-specific bounds if available, otherwise use default bounds
        
        Args:
            peers: List of peer data dictionaries
            ratio_code: Ratio code for bounds lookup
            sector_main: Sector name for sector-specific bounds
        
        Returns:
            FilterStageResult with F3 validation status
        """
        included = []
        excluded = []
        
        # Get bounds for this ratio and sector
        sector_bounds = ECONOMIC_BOUNDS.get(sector_main, {})
        default_bounds = ECONOMIC_BOUNDS.get("_default", {})
        
        bounds = sector_bounds.get(ratio_code) or default_bounds.get(ratio_code)
        
        if bounds is None:
            # No bounds defined for this ratio
            return FilterStageResult(
                stage="F3_ECONOMIC_BOUNDS",
                peers_input=len(peers),
                peers_output=0,
                excluded_count=len(peers),
                excluded_reasons=["F3_NO_BOUNDS_DEFINED"],
                passed=False
            )
        
        min_bound, max_bound = bounds
        
        for peer in peers:
            ticker = peer["ticker"]
            value = peer["ratio_value"]
            
            # F3: Economic validity
            if value < min_bound:
                excluded.append({
                    "ticker": ticker,
                    "value": value,
                    "reason": f"F3_BELOW_MIN({value:.2f}<{min_bound})"
                })
            elif value > max_bound:
                excluded.append({
                    "ticker": ticker,
                    "value": value,
                    "reason": f"F3_ABOVE_MAX({value:.2f}>{max_bound})"
                })
            else:
                included.append(peer)
        
        passed = True
        
        return FilterStageResult(
            stage="F3_ECONOMIC_BOUNDS",
            peers_input=len(peers),
            peers_output=len(included),
            excluded_count=len(excluded),
            excluded_reasons=[e["reason"] for e in excluded],
            passed=passed
        )
    
    def test_f4_winsorization(
        self,
        peers: List[Dict[str, Any]]
    ) -> FilterStageResult:
        """
        Verify P5-P95 winsorization (not exclusion)
        
        F4 Filter Rules:
            - Calculate P5 and P95 percentiles
            - Clip values below P5 to P5 (don't exclude)
            - Clip values above P95 to P95 (don't exclude)
            - Only apply if n_peers >= 5
        
        Args:
            peers: List of peer data dictionaries
        
        Returns:
            FilterStageResult with F4 validation status
        """
        winsorized_count = 0
        
        # F4 requires at least 5 peers
        if len(peers) < 5:
            return FilterStageResult(
                stage="F4_WINSORIZATION",
                peers_input=len(peers),
                peers_output=len(peers),
                excluded_count=0,
                excluded_reasons=[],
                passed=True
            )
        
        # Calculate P5 and P95
        import numpy as np
        values = [p["ratio_value"] for p in peers]
        p5 = np.percentile(values, 5)
        p95 = np.percentile(values, 95)
        
        # Apply winsorization
        for peer in peers:
            original_value = peer["ratio_value"]
            
            if peer["ratio_value"] < p5:
                peer["ratio_value"] = p5
                peer["winsorized"] = "P5"
                winsorized_count += 1
            elif peer["ratio_value"] > p95:
                peer["ratio_value"] = p95
                peer["winsorized"] = "P95"
                winsorized_count += 1
        
        passed = True
        
        return FilterStageResult(
            stage="F4_WINSORIZATION",
            peers_input=len(peers),
            peers_output=len(peers),  # No exclusions, only transformations
            excluded_count=0,  # Winsorization doesn't exclude
            excluded_reasons=[f"WINSORIZED_{winsorized_count}_VALUES"],
            passed=passed
        )
    
    def test_f5_peer_count(
        self,
        peers: List[Dict[str, Any]],
        min_peers: int = 3
    ) -> FilterStageResult:
        """
        Verify minimum peer count validation
        
        F5 Filter Rules:
            - Reject benchmark computation if len(peers) < min_peers
            - Default min_peers = 3
            - This is a validation step, not an exclusion step
        
        Args:
            peers: List of peer data dictionaries
            min_peers: Minimum required peer count
        
        Returns:
            FilterStageResult with F5 validation status
        """
        n_peers = len(peers)
        can_compute = n_peers >= min_peers
        
        passed = can_compute
        
        reason = "F5_PASS" if can_compute else f"F5_INSUFFICIENT_PEERS({n_peers}<{min_peers})"
        
        return FilterStageResult(
            stage="F5_PEER_COUNT",
            peers_input=n_peers,
            peers_output=n_peers if can_compute else 0,
            excluded_count=0,  # F5 doesn't exclude, it rejects entire computation
            excluded_reasons=[reason],
            passed=passed
        )
    
    def test_full_pipeline(
        self,
        peers: List[Dict[str, Any]],
        ratio_code: str = "current_ratio",
        sector_main: str = "Teknoloji & İletişim",
        min_periods: int = 3,
        min_peers: int = 3
    ) -> FilterPipelineReport:
        """
        Test complete F1-F5 execution
        
        Executes the full filter pipeline sequentially:
        1. F1: Exclude NULL/infinite values
        2. F2: Exclude insufficient periods
        3. F3: Exclude values outside economic bounds
        4. F4: Winsorize outliers (P5-P95)
        5. F5: Validate minimum peer count
        
        Args:
            peers: List of peer data dictionaries
            ratio_code: Ratio code for bounds lookup
            sector_main: Sector name for sector-specific bounds
            min_periods: Minimum required periods for F2
            min_peers: Minimum required peer count for F5
        
        Returns:
            FilterPipelineReport with complete pipeline results
        """
        stage_results = []
        total_input = len(peers)
        
        # F1: NULL filter
        f1_result = self.test_f1_null_filter(peers)
        stage_results.append(f1_result)
        peers = [p for p in peers if p["ratio_value"] is not None and math.isfinite(p["ratio_value"])]
        f1_excluded = f1_result.excluded_count
        
        # F2: Period filter
        f2_result = self.test_f2_period_filter(peers, min_periods)
        stage_results.append(f2_result)
        peers = [p for p in peers if p.get("available_periods", 0) >= min_periods]
        f2_excluded = f2_result.excluded_count
        
        # F3: Economic bounds filter
        f3_result = self.test_f3_economic_bounds(peers, ratio_code, sector_main)
        stage_results.append(f3_result)
        
        # Only continue if F3 has bounds defined
        if f3_result.passed and f3_result.peers_output > 0:
            # Filter peers based on economic bounds for next stages
            sector_bounds = ECONOMIC_BOUNDS.get(sector_main, {})
            default_bounds = ECONOMIC_BOUNDS.get("_default", {})
            bounds = sector_bounds.get(ratio_code) or default_bounds.get(ratio_code)
            
            if bounds:
                min_bound, max_bound = bounds
                peers = [p for p in peers if min_bound <= p["ratio_value"] <= max_bound]
            
            f3_excluded = f3_result.excluded_count
        else:
            f3_excluded = len(peers)
            peers = []
        
        # F4: Winsorization (doesn't exclude, transforms values)
        f4_winsorized = 0
        if len(peers) >= 5:
            f4_result = self.test_f4_winsorization(peers)
            stage_results.append(f4_result)
            # Count how many were winsorized
            f4_winsorized = sum(1 for p in peers if p.get("winsorized"))
        else:
            # Skip winsorization if fewer than 5 peers
            f4_result = FilterStageResult(
                stage="F4_WINSORIZATION",
                peers_input=len(peers),
                peers_output=len(peers),
                excluded_count=0,
                excluded_reasons=["SKIPPED_TOO_FEW_PEERS"],
                passed=True
            )
            stage_results.append(f4_result)
        
        # F5: Peer count validation
        f5_result = self.test_f5_peer_count(peers, min_peers)
        stage_results.append(f5_result)
        
        final_peers = len(peers)
        f5_rejected = 1 if not f5_result.passed else 0
        
        # Calculate exclusion rates
        exclusion_rates = {
            "F1_NULL": (f1_excluded / total_input * 100) if total_input > 0 else 0.0,
            "F2_PERIODS": (f2_excluded / total_input * 100) if total_input > 0 else 0.0,
            "F3_BOUNDS": (f3_excluded / total_input * 100) if total_input > 0 else 0.0,
            "F4_WINSORIZED": (f4_winsorized / total_input * 100) if total_input > 0 else 0.0,
        }
        
        # Overall status
        status = "PASS" if f5_result.passed else "FAIL"
        
        return FilterPipelineReport(
            total_peers_input=total_input,
            f1_excluded=f1_excluded,
            f2_excluded=f2_excluded,
            f3_excluded=f3_excluded,
            f4_winsorized=f4_winsorized,
            f5_rejected=f5_rejected,
            final_peers=final_peers,
            exclusion_rates=exclusion_rates,
            stage_results=stage_results,
            status=status
        )
    
    def generate_report(
        self,
        pipeline_report: FilterPipelineReport,
        scenario_name: str = "Test Scenario"
    ) -> str:
        """
        Generate a formatted report for filter pipeline test results
        
        Args:
            pipeline_report: FilterPipelineReport from test_full_pipeline
            scenario_name: Name of the test scenario
        
        Returns:
            Formatted Markdown report string
        """
        report = []
        report.append(f"# Filter Pipeline Test Report: {scenario_name}")
        report.append("")
        report.append(f"**Status**: {pipeline_report.status}")
        report.append("")
        
        # Overall statistics
        report.append("## Overall Statistics")
        report.append("")
        report.append(f"- **Total Peers Input**: {pipeline_report.total_peers_input}")
        report.append(f"- **F1 Excluded (NULL/Infinite)**: {pipeline_report.f1_excluded}")
        report.append(f"- **F2 Excluded (Insufficient Periods)**: {pipeline_report.f2_excluded}")
        report.append(f"- **F3 Excluded (Economic Bounds)**: {pipeline_report.f3_excluded}")
        report.append(f"- **F4 Winsorized (Outliers)**: {pipeline_report.f4_winsorized}")
        report.append(f"- **F5 Rejected (Peer Count)**: {pipeline_report.f5_rejected}")
        report.append(f"- **Final Peers**: {pipeline_report.final_peers}")
        report.append("")
        
        # Exclusion rates table
        report.append("## Exclusion Rates")
        report.append("")
        
        exclusion_data = [
            {
                "Filter": "F1 (NULL/Infinite)",
                "Excluded": pipeline_report.f1_excluded,
                "Rate (%)": f"{pipeline_report.exclusion_rates['F1_NULL']:.2f}"
            },
            {
                "Filter": "F2 (Insufficient Periods)",
                "Excluded": pipeline_report.f2_excluded,
                "Rate (%)": f"{pipeline_report.exclusion_rates['F2_PERIODS']:.2f}"
            },
            {
                "Filter": "F3 (Economic Bounds)",
                "Excluded": pipeline_report.f3_excluded,
                "Rate (%)": f"{pipeline_report.exclusion_rates['F3_BOUNDS']:.2f}"
            },
            {
                "Filter": "F4 (Winsorization)",
                "Excluded": pipeline_report.f4_winsorized,
                "Rate (%)": f"{pipeline_report.exclusion_rates['F4_WINSORIZED']:.2f}"
            }
        ]
        
        report.append(self.printer.format_table(
            data=exclusion_data,
            columns=["Filter", "Excluded", "Rate (%)"],
            align={"Filter": "left", "Excluded": "right", "Rate (%)": "right"}
        ))
        report.append("")
        
        # Stage-by-stage results
        report.append("## Filter Stage Details")
        report.append("")
        
        for stage in pipeline_report.stage_results:
            report.append(f"### {stage.stage}")
            report.append(f"- **Input Peers**: {stage.peers_input}")
            report.append(f"- **Output Peers**: {stage.peers_output}")
            report.append(f"- **Excluded/Modified**: {stage.excluded_count}")
            report.append(f"- **Status**: {'PASS' if stage.passed else 'FAIL'}")
            
            if stage.excluded_reasons:
                report.append(f"- **Reasons**: {', '.join(stage.excluded_reasons[:5])}")  # Show first 5
            
            report.append("")
        
        # Conclusion
        report.append("## Conclusion")
        report.append("")
        
        if pipeline_report.status == "PASS":
            report.append(f"✓ Filter pipeline executed successfully. {pipeline_report.final_peers} peers passed all filters.")
        else:
            report.append(f"✗ Filter pipeline rejected benchmark computation. Only {pipeline_report.final_peers} peers available (minimum required: 3).")
        
        report.append("")
        
        return "\n".join(report)


# ============================================================================
# Pytest Test Functions
# ============================================================================

def test_f1_null_filter_with_valid_data():
    """Test F1 filter with all valid data - should pass all peers"""
    pipeline = FilterPipelineTests()
    
    # Generate valid peer data
    peers = pipeline.test_create_synthetic_peers(scenario="valid", n_peers=10)
    
    # Test F1 filter
    result = pipeline.test_f1_null_filter(peers)
    
    # All peers should pass (no NULL or infinite values)
    assert result.excluded_count == 0, "F1 should not exclude any valid peers"
    assert result.peers_output == 10, "F1 should output all 10 valid peers"


def test_f1_null_filter_with_nulls():
    """Test F1 filter with NULL values - should exclude NULL peers"""
    pipeline = FilterPipelineTests()
    
    # Generate peer data with NULLs
    peers = pipeline.test_create_synthetic_peers(scenario="with_nulls", n_peers=10)
    
    # Test F1 filter
    result = pipeline.test_f1_null_filter(peers)
    
    # Some peers should be excluded
    assert result.excluded_count > 0, "F1 should exclude peers with NULL/infinite values"
    assert result.peers_output < 10, "F1 should output fewer than 10 peers"


def test_f2_period_filter_sufficient_periods():
    """Test F2 filter with sufficient periods - should pass all peers"""
    pipeline = FilterPipelineTests()
    
    # Generate valid peer data (all have sufficient periods)
    peers = pipeline.test_create_synthetic_peers(scenario="valid", n_peers=10)
    
    # Test F2 filter
    result = pipeline.test_f2_period_filter(peers, min_periods=3)
    
    # All peers should pass (all have sufficient periods)
    assert result.excluded_count == 0, "F2 should not exclude peers with sufficient periods"
    assert result.peers_output == 10, "F2 should output all 10 peers"


def test_f2_period_filter_insufficient_periods():
    """Test F2 filter with insufficient periods - should exclude some peers"""
    pipeline = FilterPipelineTests()
    
    # Generate peer data with insufficient periods
    peers = pipeline.test_create_synthetic_peers(scenario="insufficient_periods", n_peers=10)
    
    # Test F2 filter
    result = pipeline.test_f2_period_filter(peers, min_periods=3)
    
    # Some peers should be excluded
    assert result.excluded_count > 0, "F2 should exclude peers with insufficient periods"
    assert result.peers_output < 10, "F2 should output fewer than 10 peers"


def test_f3_economic_bounds_within_bounds():
    """Test F3 filter with values within bounds - should pass all peers"""
    pipeline = FilterPipelineTests()
    
    # Generate valid peer data (within economic bounds)
    peers = pipeline.test_create_synthetic_peers(scenario="valid", n_peers=10, ratio_code="current_ratio")
    
    # Test F3 filter
    result = pipeline.test_f3_economic_bounds(peers, ratio_code="current_ratio")
    
    # All peers should pass (within bounds)
    assert result.excluded_count == 0, "F3 should not exclude peers within economic bounds"
    assert result.peers_output == 10, "F3 should output all 10 peers"


def test_f3_economic_bounds_with_outliers():
    """Test F3 filter with outliers beyond bounds - should exclude outliers"""
    pipeline = FilterPipelineTests()
    
    # Generate peer data with outliers
    peers = pipeline.test_create_synthetic_peers(scenario="with_outliers", n_peers=10, ratio_code="current_ratio")
    
    # Test F3 filter
    result = pipeline.test_f3_economic_bounds(peers, ratio_code="current_ratio")
    
    # Some peers should be excluded (outliers beyond bounds)
    assert result.excluded_count > 0, "F3 should exclude peers beyond economic bounds"


def test_f4_winsorization():
    """Test F4 winsorization - should clip extreme values but not exclude"""
    pipeline = FilterPipelineTests()
    
    # Generate peer data with outliers
    peers = pipeline.test_create_synthetic_peers(scenario="with_outliers", n_peers=10)
    
    # Test F4 winsorization
    result = pipeline.test_f4_winsorization(peers)
    
    # No peers should be excluded (winsorization clips, doesn't exclude)
    assert result.excluded_count == 0, "F4 should not exclude any peers"
    assert result.peers_output == 10, "F4 should output all 10 peers"
    
    # Some values should be winsorized
    winsorized_count = sum(1 for p in peers if p.get("winsorized"))
    assert winsorized_count > 0, "F4 should winsorize extreme values"


def test_f5_peer_count_sufficient():
    """Test F5 validation with sufficient peers - should pass"""
    pipeline = FilterPipelineTests()
    
    # Generate sufficient peers
    peers = pipeline.test_create_synthetic_peers(scenario="valid", n_peers=10)
    
    # Test F5 validation
    result = pipeline.test_f5_peer_count(peers, min_peers=3)
    
    # Should pass with sufficient peers
    assert result.passed is True, "F5 should pass with 10 peers (>= 3 required)"
    assert result.peers_output == 10, "F5 should output all peers"


def test_f5_peer_count_insufficient():
    """Test F5 validation with insufficient peers - should reject"""
    pipeline = FilterPipelineTests()
    
    # Generate insufficient peers
    peers = pipeline.test_create_synthetic_peers(scenario="too_few", n_peers=2)
    
    # Test F5 validation
    result = pipeline.test_f5_peer_count(peers, min_peers=3)
    
    # Should reject with insufficient peers
    assert result.passed is False, "F5 should reject with 2 peers (< 3 required)"
    assert result.peers_output == 0, "F5 should output 0 when rejected"


def test_full_pipeline_valid_scenario():
    """Test complete pipeline with valid data - should pass all stages"""
    pipeline = FilterPipelineTests()
    
    # Generate valid peer data
    peers = pipeline.test_create_synthetic_peers(scenario="valid", n_peers=10)
    
    # Run full pipeline
    report = pipeline.test_full_pipeline(
        peers=peers,
        ratio_code="current_ratio",
        sector_main="Teknoloji & İletişim"
    )
    
    # Should pass with valid data
    assert report.status == "PASS", "Pipeline should pass with valid data"
    assert report.final_peers > 0, "Final peers should be greater than 0"
    assert report.f1_excluded == 0, "No peers should be excluded by F1 with valid data"
    assert report.f2_excluded == 0, "No peers should be excluded by F2 with valid data"


def test_full_pipeline_with_nulls():
    """Test complete pipeline with NULL values - should filter NULLs"""
    pipeline = FilterPipelineTests()
    
    # Generate peer data with NULLs
    peers = pipeline.test_create_synthetic_peers(scenario="with_nulls", n_peers=10)
    
    # Run full pipeline
    report = pipeline.test_full_pipeline(
        peers=peers,
        ratio_code="current_ratio"
    )
    
    # F1 should exclude NULL values
    assert report.f1_excluded > 0, "F1 should exclude peers with NULL values"


def test_full_pipeline_insufficient_peers():
    """Test complete pipeline with too few peers - should reject at F5"""
    pipeline = FilterPipelineTests()
    
    # Generate insufficient peers
    peers = pipeline.test_create_synthetic_peers(scenario="too_few", n_peers=2)
    
    # Run full pipeline
    report = pipeline.test_full_pipeline(
        peers=peers,
        ratio_code="current_ratio"
    )
    
    # F5 should reject due to insufficient peer count
    assert report.status == "FAIL", "Pipeline should fail with too few peers"
    assert report.f5_rejected == 1, "F5 should reject computation"


def test_generate_report():
    """Test report generation for filter pipeline results"""
    pipeline = FilterPipelineTests()
    
    # Generate valid peer data and run pipeline
    peers = pipeline.test_create_synthetic_peers(scenario="valid", n_peers=10)
    pipeline_report = pipeline.test_full_pipeline(peers, ratio_code="current_ratio")
    
    # Generate report
    report_text = pipeline.generate_report(pipeline_report, scenario_name="Valid Data Test")
    
    # Verify report contains expected sections
    assert "Filter Pipeline Test Report" in report_text
    assert "Overall Statistics" in report_text
    assert "Exclusion Rates" in report_text
    assert "Filter Stage Details" in report_text
    assert "Conclusion" in report_text
    assert pipeline_report.status in report_text
