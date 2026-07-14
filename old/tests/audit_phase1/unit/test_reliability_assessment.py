"""
Reliability Assessment Test Module - Requirement 9

Tests benchmark reliability classification based on peer count.
Verifies reliability tiers (INSUFFICIENT, LOW, MEDIUM, HIGH) and can_compute flag.

**Validates: Requirements 9**
"""
import pytest
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

from tests.audit_phase1.utilities.validation_algorithms import assess_reliability
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter


@dataclass
class ReliabilityResult:
    """Result of reliability assessment for a given peer count"""
    n_peers: int
    reliability_level: str
    can_compute: bool
    expected_reliability: str
    expected_can_compute: bool
    passed: bool


@dataclass
class ReliabilityReport:
    """Reliability assessment test report"""
    test_cases: List[ReliabilityResult]
    total_tests: int
    passed_tests: int
    failed_tests: int
    distribution_stats: Dict[str, int]  # reliability_level -> count
    status: str  # PASS/FAIL


class ReliabilityAssessmentTests:
    """Test suite for benchmark reliability assessment validation"""
    
    def __init__(self):
        self.printer = PrettyPrinter()
        self.test_results: List[ReliabilityResult] = []
    
    def test_create_peer_sets(self, sizes: List[int]) -> List[List[Dict[str, Any]]]:
        """
        Generate peer sets of varying sizes for testing
        
        Args:
            sizes: List of peer set sizes to generate (e.g., [2, 3, 5, 10, 15])
        
        Returns:
            List of peer data lists, one for each size
        
        Example:
            >>> tests = ReliabilityAssessmentTests()
            >>> peer_sets = tests.test_create_peer_sets([2, 3, 5])
            >>> len(peer_sets)
            3
            >>> len(peer_sets[0])
            2
            >>> len(peer_sets[1])
            3
        """
        peer_sets = []
        
        for n in sizes:
            # Generate n peer companies with mock data
            peers = []
            for i in range(n):
                peer = {
                    "ticker": f"PEER{i+1:03d}",
                    "ratio_value": 1.5 + (i * 0.1),  # Simple sequential values
                    "market_cap": 1000000 + (i * 100000),
                    "available_periods": 4
                }
                peers.append(peer)
            
            peer_sets.append(peers)
        
        return peer_sets
    
    def test_insufficient_reliability(self, n_peers: int = 2) -> ReliabilityResult:
        """
        Verify n < 3 → INSUFFICIENT + can_compute=False
        
        Rule: If peer count is less than 3, reliability is INSUFFICIENT
              and benchmark cannot be computed (can_compute = False)
        
        Args:
            n_peers: Number of peers to test (default 2)
        
        Returns:
            ReliabilityResult with test outcome
        
        Test Case:
            - n_peers = 2 → INSUFFICIENT, can_compute = False
        """
        reliability, can_compute = assess_reliability(n_peers)
        
        expected_reliability = "INSUFFICIENT"
        expected_can_compute = False
        
        passed = (
            reliability == expected_reliability and 
            can_compute == expected_can_compute
        )
        
        result = ReliabilityResult(
            n_peers=n_peers,
            reliability_level=reliability,
            can_compute=can_compute,
            expected_reliability=expected_reliability,
            expected_can_compute=expected_can_compute,
            passed=passed
        )
        
        self.test_results.append(result)
        return result
    
    def test_low_reliability(self, n_peers: int = 3) -> ReliabilityResult:
        """
        Verify 3 ≤ n ≤ 4 → LOW
        
        Rule: If peer count is 3 or 4, reliability is LOW
              and benchmark can be computed (can_compute = True)
        
        Args:
            n_peers: Number of peers to test (default 3)
        
        Returns:
            ReliabilityResult with test outcome
        
        Test Cases:
            - n_peers = 3 → LOW, can_compute = True
            - n_peers = 4 → LOW, can_compute = True
        """
        reliability, can_compute = assess_reliability(n_peers)
        
        expected_reliability = "LOW"
        expected_can_compute = True
        
        passed = (
            reliability == expected_reliability and 
            can_compute == expected_can_compute
        )
        
        result = ReliabilityResult(
            n_peers=n_peers,
            reliability_level=reliability,
            can_compute=can_compute,
            expected_reliability=expected_reliability,
            expected_can_compute=expected_can_compute,
            passed=passed
        )
        
        self.test_results.append(result)
        return result
    
    def test_medium_reliability(self, n_peers: int = 7) -> ReliabilityResult:
        """
        Verify 5 ≤ n ≤ 9 → MEDIUM
        
        Rule: If peer count is between 5 and 9 (inclusive), 
              reliability is MEDIUM and benchmark can be computed
        
        Args:
            n_peers: Number of peers to test (default 7)
        
        Returns:
            ReliabilityResult with test outcome
        
        Test Cases:
            - n_peers = 5 → MEDIUM, can_compute = True
            - n_peers = 7 → MEDIUM, can_compute = True
            - n_peers = 9 → MEDIUM, can_compute = True
        """
        reliability, can_compute = assess_reliability(n_peers)
        
        expected_reliability = "MEDIUM"
        expected_can_compute = True
        
        passed = (
            reliability == expected_reliability and 
            can_compute == expected_can_compute
        )
        
        result = ReliabilityResult(
            n_peers=n_peers,
            reliability_level=reliability,
            can_compute=can_compute,
            expected_reliability=expected_reliability,
            expected_can_compute=expected_can_compute,
            passed=passed
        )
        
        self.test_results.append(result)
        return result
    
    def test_high_reliability(self, n_peers: int = 15) -> ReliabilityResult:
        """
        Verify n ≥ 10 → HIGH
        
        Rule: If peer count is 10 or more, reliability is HIGH
              and benchmark can be computed
        
        Args:
            n_peers: Number of peers to test (default 15)
        
        Returns:
            ReliabilityResult with test outcome
        
        Test Cases:
            - n_peers = 10 → HIGH, can_compute = True
            - n_peers = 15 → HIGH, can_compute = True
            - n_peers = 50 → HIGH, can_compute = True
        """
        reliability, can_compute = assess_reliability(n_peers)
        
        expected_reliability = "HIGH"
        expected_can_compute = True
        
        passed = (
            reliability == expected_reliability and 
            can_compute == expected_can_compute
        )
        
        result = ReliabilityResult(
            n_peers=n_peers,
            reliability_level=reliability,
            can_compute=can_compute,
            expected_reliability=expected_reliability,
            expected_can_compute=expected_can_compute,
            passed=passed
        )
        
        self.test_results.append(result)
        return result
    
    def test_benchmark_rejection(self, n_peers: int) -> bool:
        """
        Verify INSUFFICIENT benchmarks are rejected (cannot be computed)
        
        Rule: If reliability is INSUFFICIENT (n < 3), then can_compute = False
              and the benchmark should not be saved to the database
        
        Args:
            n_peers: Number of peers to test
        
        Returns:
            True if benchmark is correctly rejected, False otherwise
        
        Test Logic:
            - If n_peers < 3, benchmark should be rejected (can_compute = False)
            - If n_peers >= 3, benchmark should be accepted (can_compute = True)
        """
        reliability, can_compute = assess_reliability(n_peers)
        
        # Benchmark should be rejected if n_peers < 3
        should_reject = n_peers < 3
        is_rejected = not can_compute
        
        # Test passes if rejection matches expectation
        return should_reject == is_rejected
    
    def generate_report(self) -> ReliabilityReport:
        """
        Generate a comprehensive reliability assessment test report
        
        Returns:
            ReliabilityReport with test results and distribution statistics
        
        Report includes:
            - Test case results for all peer count scenarios
            - Pass/fail counts
            - Distribution of reliability classifications
            - Overall status
        """
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.passed)
        failed_tests = total_tests - passed_tests
        
        # Calculate distribution statistics
        distribution_stats = {
            "INSUFFICIENT": 0,
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0
        }
        
        for result in self.test_results:
            if result.reliability_level in distribution_stats:
                distribution_stats[result.reliability_level] += 1
        
        # Overall status
        status = "PASS" if failed_tests == 0 else "FAIL"
        
        return ReliabilityReport(
            test_cases=self.test_results,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            distribution_stats=distribution_stats,
            status=status
        )
    
    def generate_report_text(self, report: ReliabilityReport) -> str:
        """
        Generate a formatted text report for reliability assessment results
        
        Args:
            report: ReliabilityReport from generate_report()
        
        Returns:
            Formatted Markdown report string
        """
        lines = []
        lines.append("# Reliability Assessment Test Report")
        lines.append("")
        lines.append(f"**Status**: {report.status}")
        lines.append(f"**Total Tests**: {report.total_tests}")
        lines.append(f"**Passed**: {report.passed_tests}")
        lines.append(f"**Failed**: {report.failed_tests}")
        lines.append("")
        
        # Test Results Table
        lines.append("## Test Results")
        lines.append("")
        
        test_data = []
        for result in report.test_cases:
            test_data.append({
                "Peer Count": result.n_peers,
                "Reliability": result.reliability_level,
                "Can Compute": "Yes" if result.can_compute else "No",
                "Expected": result.expected_reliability,
                "Status": "PASS" if result.passed else "FAIL"
            })
        
        lines.append(self.printer.format_table(
            data=test_data,
            columns=["Peer Count", "Reliability", "Can Compute", "Expected", "Status"],
            align={
                "Peer Count": "right",
                "Reliability": "left",
                "Can Compute": "center",
                "Expected": "left",
                "Status": "center"
            }
        ))
        lines.append("")
        
        # Distribution Statistics
        lines.append("## Reliability Distribution")
        lines.append("")
        
        dist_data = []
        for level in ["INSUFFICIENT", "LOW", "MEDIUM", "HIGH"]:
            count = report.distribution_stats[level]
            percentage = (count / report.total_tests * 100) if report.total_tests > 0 else 0.0
            dist_data.append({
                "Reliability Level": level,
                "Test Count": count,
                "Percentage": f"{percentage:.1f}%"
            })
        
        lines.append(self.printer.format_table(
            data=dist_data,
            columns=["Reliability Level", "Test Count", "Percentage"],
            align={
                "Reliability Level": "left",
                "Test Count": "right",
                "Percentage": "right"
            }
        ))
        lines.append("")
        
        # Key Findings
        lines.append("## Key Findings")
        lines.append("")
        
        if report.status == "PASS":
            lines.append("✓ All reliability classification tests passed.")
            lines.append("")
            lines.append("- INSUFFICIENT classification correctly applied for n < 3")
            lines.append("- LOW classification correctly applied for 3 ≤ n ≤ 4")
            lines.append("- MEDIUM classification correctly applied for 5 ≤ n ≤ 9")
            lines.append("- HIGH classification correctly applied for n ≥ 10")
            lines.append("- can_compute flag correctly set for all scenarios")
        else:
            lines.append("✗ Some reliability classification tests failed.")
            lines.append("")
            lines.append(f"- {report.failed_tests} test(s) did not match expected reliability classification")
            lines.append("- Review failed test cases above for details")
        
        lines.append("")
        
        # Conclusion
        lines.append("## Conclusion")
        lines.append("")
        
        if report.status == "PASS":
            lines.append("The reliability assessment algorithm correctly classifies ")
            lines.append("benchmark reliability based on peer count thresholds. ")
            lines.append("All test cases passed validation.")
        else:
            lines.append("The reliability assessment algorithm has classification errors. ")
            lines.append("Review the implementation to ensure correct threshold logic.")
        
        lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# Pytest Test Functions
# ============================================================================

def test_insufficient_reliability_n2():
    """Test insufficient reliability with n=2 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_insufficient_reliability(n_peers=2)
    
    assert result.reliability_level == "INSUFFICIENT", f"Expected INSUFFICIENT, got {result.reliability_level}"
    assert result.can_compute is False, f"Expected can_compute=False, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=2"


def test_insufficient_reliability_n1():
    """Test insufficient reliability with n=1 peer"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_insufficient_reliability(n_peers=1)
    
    assert result.reliability_level == "INSUFFICIENT", f"Expected INSUFFICIENT, got {result.reliability_level}"
    assert result.can_compute is False, f"Expected can_compute=False, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=1"


def test_insufficient_reliability_n0():
    """Test insufficient reliability with n=0 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_insufficient_reliability(n_peers=0)
    
    assert result.reliability_level == "INSUFFICIENT", f"Expected INSUFFICIENT, got {result.reliability_level}"
    assert result.can_compute is False, f"Expected can_compute=False, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=0"


def test_low_reliability_n3():
    """Test low reliability with n=3 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_low_reliability(n_peers=3)
    
    assert result.reliability_level == "LOW", f"Expected LOW, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=3"


def test_low_reliability_n4():
    """Test low reliability with n=4 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_low_reliability(n_peers=4)
    
    assert result.reliability_level == "LOW", f"Expected LOW, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=4"


def test_medium_reliability_n5():
    """Test medium reliability with n=5 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_medium_reliability(n_peers=5)
    
    assert result.reliability_level == "MEDIUM", f"Expected MEDIUM, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=5"


def test_medium_reliability_n7():
    """Test medium reliability with n=7 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_medium_reliability(n_peers=7)
    
    assert result.reliability_level == "MEDIUM", f"Expected MEDIUM, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=7"


def test_medium_reliability_n9():
    """Test medium reliability with n=9 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_medium_reliability(n_peers=9)
    
    assert result.reliability_level == "MEDIUM", f"Expected MEDIUM, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=9"


def test_high_reliability_n10():
    """Test high reliability with n=10 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_high_reliability(n_peers=10)
    
    assert result.reliability_level == "HIGH", f"Expected HIGH, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=10"


def test_high_reliability_n15():
    """Test high reliability with n=15 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_high_reliability(n_peers=15)
    
    assert result.reliability_level == "HIGH", f"Expected HIGH, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=15"


def test_high_reliability_n50():
    """Test high reliability with n=50 peers"""
    tests = ReliabilityAssessmentTests()
    result = tests.test_high_reliability(n_peers=50)
    
    assert result.reliability_level == "HIGH", f"Expected HIGH, got {result.reliability_level}"
    assert result.can_compute is True, f"Expected can_compute=True, got {result.can_compute}"
    assert result.passed is True, "Test should pass for n=50"


def test_benchmark_rejection_insufficient():
    """Test benchmark rejection with insufficient peers"""
    tests = ReliabilityAssessmentTests()
    
    # Test rejection for n < 3
    assert tests.test_benchmark_rejection(n_peers=0) is True, "Benchmark should be rejected for n=0"
    assert tests.test_benchmark_rejection(n_peers=1) is True, "Benchmark should be rejected for n=1"
    assert tests.test_benchmark_rejection(n_peers=2) is True, "Benchmark should be rejected for n=2"


def test_benchmark_rejection_sufficient():
    """Test benchmark acceptance with sufficient peers"""
    tests = ReliabilityAssessmentTests()
    
    # Test acceptance for n >= 3
    assert tests.test_benchmark_rejection(n_peers=3) is True, "Benchmark should be accepted for n=3"
    assert tests.test_benchmark_rejection(n_peers=5) is True, "Benchmark should be accepted for n=5"
    assert tests.test_benchmark_rejection(n_peers=10) is True, "Benchmark should be accepted for n=10"


def test_create_peer_sets():
    """Test peer set generation for varying sizes"""
    tests = ReliabilityAssessmentTests()
    
    sizes = [2, 3, 5, 10, 15]
    peer_sets = tests.test_create_peer_sets(sizes)
    
    # Verify correct number of peer sets
    assert len(peer_sets) == len(sizes), f"Expected {len(sizes)} peer sets, got {len(peer_sets)}"
    
    # Verify each peer set has correct size
    for i, expected_size in enumerate(sizes):
        actual_size = len(peer_sets[i])
        assert actual_size == expected_size, f"Peer set {i} should have {expected_size} peers, got {actual_size}"
    
    # Verify peer data structure
    for peer_set in peer_sets:
        for peer in peer_set:
            assert "ticker" in peer, "Peer should have 'ticker' field"
            assert "ratio_value" in peer, "Peer should have 'ratio_value' field"
            assert "market_cap" in peer, "Peer should have 'market_cap' field"
            assert "available_periods" in peer, "Peer should have 'available_periods' field"


def test_reliability_boundaries():
    """Test reliability classification at boundary values"""
    tests = ReliabilityAssessmentTests()
    
    # Test boundary between INSUFFICIENT and LOW (n=2 vs n=3)
    result_2 = tests.test_insufficient_reliability(n_peers=2)
    result_3 = tests.test_low_reliability(n_peers=3)
    
    assert result_2.reliability_level == "INSUFFICIENT", "n=2 should be INSUFFICIENT"
    assert result_2.can_compute is False, "n=2 should have can_compute=False"
    assert result_3.reliability_level == "LOW", "n=3 should be LOW"
    assert result_3.can_compute is True, "n=3 should have can_compute=True"
    
    # Test boundary between LOW and MEDIUM (n=4 vs n=5)
    result_4 = tests.test_low_reliability(n_peers=4)
    result_5 = tests.test_medium_reliability(n_peers=5)
    
    assert result_4.reliability_level == "LOW", "n=4 should be LOW"
    assert result_5.reliability_level == "MEDIUM", "n=5 should be MEDIUM"
    
    # Test boundary between MEDIUM and HIGH (n=9 vs n=10)
    result_9 = tests.test_medium_reliability(n_peers=9)
    result_10 = tests.test_high_reliability(n_peers=10)
    
    assert result_9.reliability_level == "MEDIUM", "n=9 should be MEDIUM"
    assert result_10.reliability_level == "HIGH", "n=10 should be HIGH"


def test_comprehensive_reliability_suite():
    """Test comprehensive reliability assessment across all tiers"""
    tests = ReliabilityAssessmentTests()
    
    # Test all reliability tiers
    test_cases = [
        (0, "INSUFFICIENT"),
        (1, "INSUFFICIENT"),
        (2, "INSUFFICIENT"),
        (3, "LOW"),
        (4, "LOW"),
        (5, "MEDIUM"),
        (6, "MEDIUM"),
        (7, "MEDIUM"),
        (8, "MEDIUM"),
        (9, "MEDIUM"),
        (10, "HIGH"),
        (15, "HIGH"),
        (20, "HIGH"),
        (50, "HIGH"),
        (100, "HIGH")
    ]
    
    for n_peers, expected_reliability in test_cases:
        reliability, can_compute = assess_reliability(n_peers)
        assert reliability == expected_reliability, \
            f"For n={n_peers}, expected {expected_reliability}, got {reliability}"
        
        # Verify can_compute flag
        if n_peers < 3:
            assert can_compute is False, f"For n={n_peers}, can_compute should be False"
        else:
            assert can_compute is True, f"For n={n_peers}, can_compute should be True"


def test_generate_report():
    """Test report generation for reliability assessment"""
    tests = ReliabilityAssessmentTests()
    
    # Run all reliability tests
    tests.test_insufficient_reliability(n_peers=2)
    tests.test_low_reliability(n_peers=3)
    tests.test_low_reliability(n_peers=4)
    tests.test_medium_reliability(n_peers=5)
    tests.test_medium_reliability(n_peers=7)
    tests.test_medium_reliability(n_peers=9)
    tests.test_high_reliability(n_peers=10)
    tests.test_high_reliability(n_peers=15)
    
    # Generate report
    report = tests.generate_report()
    
    # Verify report structure
    assert report.total_tests == 8, f"Expected 8 tests, got {report.total_tests}"
    assert report.passed_tests >= 0, "Passed tests should be non-negative"
    assert report.failed_tests >= 0, "Failed tests should be non-negative"
    assert report.passed_tests + report.failed_tests == report.total_tests, \
        "Passed + Failed should equal Total"
    
    # Verify distribution statistics
    assert "INSUFFICIENT" in report.distribution_stats, "Distribution should include INSUFFICIENT"
    assert "LOW" in report.distribution_stats, "Distribution should include LOW"
    assert "MEDIUM" in report.distribution_stats, "Distribution should include MEDIUM"
    assert "HIGH" in report.distribution_stats, "Distribution should include HIGH"
    
    # Verify status
    assert report.status in ["PASS", "FAIL"], f"Status should be PASS or FAIL, got {report.status}"
    
    # Generate text report
    report_text = tests.generate_report_text(report)
    
    # Verify report contains expected sections
    assert "Reliability Assessment Test Report" in report_text
    assert "Test Results" in report_text
    assert "Reliability Distribution" in report_text
    assert "Key Findings" in report_text
    assert "Conclusion" in report_text


def test_generate_report_all_pass():
    """Test report generation when all tests pass"""
    tests = ReliabilityAssessmentTests()
    
    # Run tests that should all pass
    tests.test_insufficient_reliability(n_peers=2)
    tests.test_low_reliability(n_peers=3)
    tests.test_medium_reliability(n_peers=7)
    tests.test_high_reliability(n_peers=15)
    
    # Generate report
    report = tests.generate_report()
    
    # All tests should pass
    assert report.status == "PASS", "Report status should be PASS"
    assert report.passed_tests == report.total_tests, "All tests should pass"
    assert report.failed_tests == 0, "No tests should fail"


if __name__ == "__main__":
    # Run comprehensive test suite
    tests = ReliabilityAssessmentTests()
    
    print("Running Reliability Assessment Tests...")
    print("=" * 70)
    
    # Test all reliability tiers
    print("\n1. Testing INSUFFICIENT reliability (n < 3)...")
    tests.test_insufficient_reliability(n_peers=0)
    tests.test_insufficient_reliability(n_peers=1)
    tests.test_insufficient_reliability(n_peers=2)
    
    print("2. Testing LOW reliability (3 ≤ n ≤ 4)...")
    tests.test_low_reliability(n_peers=3)
    tests.test_low_reliability(n_peers=4)
    
    print("3. Testing MEDIUM reliability (5 ≤ n ≤ 9)...")
    tests.test_medium_reliability(n_peers=5)
    tests.test_medium_reliability(n_peers=7)
    tests.test_medium_reliability(n_peers=9)
    
    print("4. Testing HIGH reliability (n ≥ 10)...")
    tests.test_high_reliability(n_peers=10)
    tests.test_high_reliability(n_peers=15)
    tests.test_high_reliability(n_peers=50)
    
    # Generate and display report
    print("\n" + "=" * 70)
    print("Generating Report...")
    print("=" * 70 + "\n")
    
    report = tests.generate_report()
    report_text = tests.generate_report_text(report)
    print(report_text)
