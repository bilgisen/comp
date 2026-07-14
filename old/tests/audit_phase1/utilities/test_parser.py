"""
Test Result Parser - Extract test outcomes and metrics

Parses pytest output to extract test names, statuses, assertion failures,
and generates test summary reports.
"""
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class AssertionFailure:
    """Captured assertion failure from test output"""
    test_name: str
    requirement_id: int
    expected: Any
    actual: Any
    message: str
    traceback: str


@dataclass
class TestSummary:
    """Overall test execution summary"""
    total_tests: int
    passed: int
    failed: int
    warnings: int
    skipped: int
    pass_rate: float
    execution_time_seconds: float
    timestamp: datetime
    results_by_requirement: Dict[int, List[Dict[str, Any]]]


class TestResultParser:
    """Parse pytest output and extract test results"""
    
    def parse_test_output(self, output: str) -> TestSummary:
        """
        Parse pytest output and extract test summary
        
        Args:
            output: Raw pytest output string
        
        Returns:
            TestSummary with aggregated results
        """
        lines = output.split("\n")
        
        # Extract test names and statuses
        test_results = self.extract_test_statuses(output)
        
        # Calculate metrics
        total = len(test_results)
        passed = sum(1 for status in test_results.values() if status == "PASS")
        failed = sum(1 for status in test_results.values() if status == "FAIL")
        warnings = sum(1 for status in test_results.values() if status == "WARNING")
        skipped = sum(1 for status in test_results.values() if status == "SKIP")
        
        pass_rate = (passed / total * 100) if total > 0 else 0.0
        
        # Extract execution time
        execution_time = self._extract_execution_time(output)
        
        # Group by requirement
        results_by_req = self.group_by_requirement(test_results)
        
        return TestSummary(
            total_tests=total,
            passed=passed,
            failed=failed,
            warnings=warnings,
            skipped=skipped,
            pass_rate=pass_rate,
            execution_time_seconds=execution_time,
            timestamp=datetime.utcnow(),
            results_by_requirement=results_by_req
        )
    
    def extract_test_names(self, output: str) -> List[str]:
        """
        Extract all test names from pytest output
        
        Args:
            output: Pytest output string
        
        Returns:
            List of test function names
        """
        test_names = []
        
        # Pattern: test_module.py::test_function_name
        pattern = r"(test_\w+\.py::test_\w+)"
        
        for match in re.finditer(pattern, output):
            test_names.append(match.group(1))
        
        return test_names
    
    def extract_test_statuses(self, output: str) -> Dict[str, str]:
        """
        Extract test statuses (PASS/FAIL/SKIP) from pytest output
        
        Args:
            output: Pytest output string
        
        Returns:
            Dictionary mapping test name to status
        """
        statuses = {}
        
        # Pattern for pytest result line: test_name PASSED/FAILED/SKIPPED
        lines = output.split("\n")
        
        for line in lines:
            # Check for test result indicators
            if " PASSED" in line:
                test_name = self._extract_test_name_from_line(line)
                if test_name:
                    statuses[test_name] = "PASS"
            elif " FAILED" in line:
                test_name = self._extract_test_name_from_line(line)
                if test_name:
                    statuses[test_name] = "FAIL"
            elif " SKIPPED" in line:
                test_name = self._extract_test_name_from_line(line)
                if test_name:
                    statuses[test_name] = "SKIP"
            elif "WARNING" in line.upper():
                test_name = self._extract_test_name_from_line(line)
                if test_name:
                    statuses[test_name] = "WARNING"
        
        return statuses
    
    def extract_assertion_failures(self, output: str) -> List[AssertionFailure]:
        """
        Extract assertion failures with expected/actual values
        
        Args:
            output: Pytest output string
        
        Returns:
            List of AssertionFailure objects
        """
        failures = []
        
        # Pattern for assertion errors
        # AssertionError: expected X but got Y
        failure_pattern = r"AssertionError: (.+)"
        
        lines = output.split("\n")
        current_test = None
        current_traceback = []
        
        for i, line in enumerate(lines):
            # Detect test failure
            if " FAILED" in line:
                current_test = self._extract_test_name_from_line(line)
                current_traceback = []
            
            # Collect traceback
            if current_test and (line.startswith("  ") or line.startswith("\t")):
                current_traceback.append(line)
            
            # Extract assertion details
            if current_test and "AssertionError" in line:
                match = re.search(failure_pattern, line)
                if match:
                    message = match.group(1)
                    
                    # Try to extract expected and actual
                    expected, actual = self._parse_assertion_message(message)
                    
                    # Extract requirement ID from test name
                    req_id = self._extract_requirement_id(current_test)
                    
                    failure = AssertionFailure(
                        test_name=current_test,
                        requirement_id=req_id,
                        expected=expected,
                        actual=actual,
                        message=message,
                        traceback="\n".join(current_traceback)
                    )
                    failures.append(failure)
                    current_test = None
        
        return failures
    
    def calculate_pass_rate(self, results: Dict[str, str]) -> float:
        """
        Calculate overall pass rate
        
        Args:
            results: Dictionary mapping test name to status
        
        Returns:
            Pass rate as percentage (0-100)
        """
        if not results:
            return 0.0
        
        passed = sum(1 for status in results.values() if status == "PASS")
        total = len(results)
        
        return (passed / total * 100) if total > 0 else 0.0
    
    def group_by_requirement(self, results: Dict[str, str]) -> Dict[int, List[Dict[str, Any]]]:
        """
        Group test results by requirement ID
        
        Args:
            results: Dictionary mapping test name to status
        
        Returns:
            Dictionary mapping requirement ID to list of test results
        """
        grouped = {}
        
        for test_name, status in results.items():
            req_id = self._extract_requirement_id(test_name)
            
            if req_id not in grouped:
                grouped[req_id] = []
            
            grouped[req_id].append({
                "test_name": test_name,
                "status": status
            })
        
        return grouped
    
    def identify_critical_failures(self, failures: List[AssertionFailure]) -> List[AssertionFailure]:
        """
        Identify critical failures (high-priority requirements)
        
        Args:
            failures: List of all assertion failures
        
        Returns:
            List of critical failures only
        """
        # Critical requirements: 1, 3, 4, 6, 8
        critical_req_ids = {1, 3, 4, 6, 8}
        
        return [f for f in failures if f.requirement_id in critical_req_ids]
    
    def generate_test_summary_report(self, summary: TestSummary) -> str:
        """
        Generate Markdown test summary report
        
        Args:
            summary: TestSummary object
        
        Returns:
            Markdown formatted report string
        """
        lines = [
            "# Test Execution Summary",
            "",
            f"**Timestamp**: {summary.timestamp.isoformat()}",
            f"**Execution Time**: {summary.execution_time_seconds:.2f} seconds",
            "",
            "## Overall Results",
            "",
            f"- **Total Tests**: {summary.total_tests}",
            f"- **Passed**: {summary.passed} ✅",
            f"- **Failed**: {summary.failed} ❌",
            f"- **Warnings**: {summary.warnings} ⚠️",
            f"- **Skipped**: {summary.skipped} ⏭️",
            f"- **Pass Rate**: {summary.pass_rate:.1f}%",
            "",
            "## Results by Requirement",
            ""
        ]
        
        # Add requirement breakdown
        for req_id in sorted(summary.results_by_requirement.keys()):
            tests = summary.results_by_requirement[req_id]
            passed = sum(1 for t in tests if t["status"] == "PASS")
            total = len(tests)
            
            lines.append(f"### Requirement {req_id}")
            lines.append(f"- Tests: {total}")
            lines.append(f"- Passed: {passed}/{total}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _extract_test_name_from_line(self, line: str) -> Optional[str]:
        """Extract test name from pytest output line"""
        match = re.search(r"(test_\w+\.py::test_\w+)", line)
        return match.group(1) if match else None
    
    def _extract_requirement_id(self, test_name: str) -> int:
        """
        Extract requirement ID from test name
        
        Test names follow pattern: test_req1_something or test_requirement_1_something
        """
        # Try pattern: test_req<N>_
        match = re.search(r"req(?:uirement)?_?(\d+)", test_name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Default to 0 if not found
        return 0
    
    def _extract_execution_time(self, output: str) -> float:
        """Extract execution time from pytest output"""
        # Pattern: "====== 42 passed in 12.34s ======"
        match = re.search(r"in ([\d.]+)s", output)
        if match:
            return float(match.group(1))
        return 0.0
    
    def _parse_assertion_message(self, message: str) -> tuple:
        """
        Parse assertion message to extract expected and actual values
        
        Args:
            message: Assertion error message
        
        Returns:
            Tuple of (expected, actual)
        """
        # Try pattern: "expected X but got Y"
        match = re.search(r"expected (.+?) but got (.+)", message, re.IGNORECASE)
        if match:
            return (match.group(1), match.group(2))
        
        # Try pattern: "X != Y"
        match = re.search(r"(.+?) != (.+)", message)
        if match:
            return (match.group(1), match.group(2))
        
        # Could not parse
        return (None, None)
