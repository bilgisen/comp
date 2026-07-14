"""
Validation Algorithms - Reusable validation logic

Provides validation functions for bounds checking, tolerance verification,
duplicate detection, and reliability assessment.
"""
from typing import Tuple, Optional, List, Dict, Any
import math


def validate_bounds(
    value: float,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None
) -> Tuple[bool, Optional[str]]:
    """
    Check if value is within specified bounds
    
    Args:
        value: Value to check
        min_val: Minimum bound (inclusive)
        max_val: Maximum bound (inclusive)
    
    Returns:
        Tuple of (is_valid, reason)
        - is_valid: True if within bounds
        - reason: Explanation if invalid (None if valid)
    
    Example:
        >>> validate_bounds(5.0, min_val=0.0, max_val=10.0)
        (True, None)
        >>> validate_bounds(15.0, min_val=0.0, max_val=10.0)
        (False, "ABOVE_MAX(10.0)")
    """
    if not math.isfinite(value):
        return (False, "NON_FINITE_VALUE")
    
    if min_val is not None and value < min_val:
        return (False, f"BELOW_MIN({min_val})")
    
    if max_val is not None and value > max_val:
        return (False, f"ABOVE_MAX({max_val})")
    
    return (True, None)


def calculate_percentage_difference(
    expected: float,
    actual: float
) -> float:
    """
    Calculate percentage difference between expected and actual values
    
    Args:
        expected: Expected value
        actual: Actual value
    
    Returns:
        Percentage difference (absolute value)
    
    Formula:
        |actual - expected| / expected * 100
    
    Example:
        >>> calculate_percentage_difference(100.0, 102.0)
        2.0
        >>> calculate_percentage_difference(2.0, 2.03)
        1.5
    """
    if expected == 0:
        return float('inf') if actual != 0 else 0.0
    
    return abs(actual - expected) / abs(expected) * 100


def check_tolerance(
    expected: float,
    actual: float,
    tolerance_percentage: float
) -> Tuple[bool, float]:
    """
    Check if actual value is within tolerance of expected value
    
    Args:
        expected: Expected value
        actual: Actual value
        tolerance_percentage: Tolerance threshold (percentage)
    
    Returns:
        Tuple of (within_tolerance, percentage_diff)
    
    Example:
        >>> check_tolerance(100.0, 101.0, tolerance_percentage=2.0)
        (True, 1.0)
        >>> check_tolerance(100.0, 105.0, tolerance_percentage=2.0)
        (False, 5.0)
    """
    pct_diff = calculate_percentage_difference(expected, actual)
    within_tolerance = pct_diff <= tolerance_percentage
    
    return (within_tolerance, pct_diff)


def detect_duplicates(
    records: List[Dict[str, Any]],
    key_fields: List[str]
) -> List[Dict[str, Any]]:
    """
    Detect duplicate records based on key fields
    
    Args:
        records: List of record dictionaries
        key_fields: Fields that define uniqueness
    
    Returns:
        List of duplicate records with duplicate_count field
    
    Example:
        >>> records = [
        ...     {"ticker": "GARAN", "period": "2024Q3", "item_code": "1.1"},
        ...     {"ticker": "GARAN", "period": "2024Q3", "item_code": "1.1"},
        ...     {"ticker": "THYAO", "period": "2024Q3", "item_code": "1.1"},
        ... ]
        >>> duplicates = detect_duplicates(records, ["ticker", "period", "item_code"])
        >>> len(duplicates)
        1
    """
    # Build key → record list mapping
    key_map = {}
    
    for record in records:
        # Create composite key
        key_values = tuple(record.get(field) for field in key_fields)
        
        if key_values not in key_map:
            key_map[key_values] = []
        
        key_map[key_values].append(record)
    
    # Find duplicates (keys with more than one record)
    duplicates = []
    
    for key_values, record_list in key_map.items():
        if len(record_list) > 1:
            # Add duplicate info
            for record in record_list:
                duplicate_record = record.copy()
                duplicate_record["duplicate_count"] = len(record_list)
                duplicate_record["duplicate_key"] = str(key_values)
                duplicates.append(duplicate_record)
    
    return duplicates


def assess_reliability(n_peers: int) -> Tuple[str, bool]:
    """
    Assess benchmark reliability based on peer count
    
    Args:
        n_peers: Number of peer companies
    
    Returns:
        Tuple of (reliability_level, can_compute)
        - reliability_level: "INSUFFICIENT", "LOW", "MEDIUM", "HIGH"
        - can_compute: Whether benchmark can be computed (n >= 3)
    
    Thresholds:
        - n < 3: INSUFFICIENT (cannot compute)
        - 3 <= n <= 4: LOW
        - 5 <= n <= 9: MEDIUM
        - n >= 10: HIGH
    
    Example:
        >>> assess_reliability(2)
        ("INSUFFICIENT", False)
        >>> assess_reliability(5)
        ("MEDIUM", True)
        >>> assess_reliability(15)
        ("HIGH", True)
    """
    if n_peers < 3:
        return ("INSUFFICIENT", False)
    elif n_peers <= 4:
        return ("LOW", True)
    elif n_peers <= 9:
        return ("MEDIUM", True)
    else:  # n_peers >= 10
        return ("HIGH", True)


def calculate_null_percentage(
    total_count: int,
    null_count: int
) -> float:
    """
    Calculate percentage of NULL values
    
    Args:
        total_count: Total number of values
        null_count: Number of NULL values
    
    Returns:
        Percentage of NULL values (0-100)
    
    Example:
        >>> calculate_null_percentage(100, 15)
        15.0
    """
    if total_count == 0:
        return 0.0
    
    return (null_count / total_count) * 100


def classify_data_quality_severity(null_percentage: float) -> str:
    """
    Classify data quality severity based on NULL percentage
    
    Args:
        null_percentage: Percentage of NULL values (0-100)
    
    Returns:
        Severity level: "OK", "WARNING", "CRITICAL"
    
    Thresholds:
        - < 10%: OK
        - 10-20%: WARNING
        - > 20%: CRITICAL
    
    Example:
        >>> classify_data_quality_severity(5.0)
        "OK"
        >>> classify_data_quality_severity(15.0)
        "WARNING"
        >>> classify_data_quality_severity(25.0)
        "CRITICAL"
    """
    if null_percentage < 10.0:
        return "OK"
    elif null_percentage <= 20.0:
        return "WARNING"
    else:
        return "CRITICAL"


def validate_sector_financial_group(
    sector_main: str,
    financial_group: str
) -> Tuple[bool, Optional[str]]:
    """
    Validate sector and financial_group combination
    
    Args:
        sector_main: Sector name
        financial_group: Financial group code
    
    Returns:
        Tuple of (is_valid, error_message)
    
    Rules:
        - Banking sector → UFRS_K, UFRS_F, or UFRS_S
        - Other sectors → XI_29
    
    Example:
        >>> validate_sector_financial_group("Bankacılık & Finans", "UFRS_K")
        (True, None)
        >>> validate_sector_financial_group("Teknoloji & İletişim", "XI_29")
        (True, None)
        >>> validate_sector_financial_group("Bankacılık & Finans", "XI_29")
        (False, "Banking sector should have UFRS_K/F/S")
    """
    BANKING_SECTOR = "Bankacılık & Finans"
    BANKING_GROUPS = {"UFRS_K", "UFRS_F", "UFRS_S"}
    INDUSTRIAL_GROUP = "XI_29"
    
    if sector_main == BANKING_SECTOR:
        if financial_group not in BANKING_GROUPS:
            return (False, f"Banking sector should have UFRS_K/F/S, got {financial_group}")
    else:
        if financial_group != INDUSTRIAL_GROUP:
            return (False, f"Industrial sector should have XI_29, got {financial_group}")
    
    return (True, None)


def calculate_coverage_percentage(
    mapped_count: int,
    total_count: int
) -> float:
    """
    Calculate mapping coverage percentage
    
    Args:
        mapped_count: Number of successfully mapped items
        total_count: Total number of items
    
    Returns:
        Coverage percentage (0-100)
    
    Example:
        >>> calculate_coverage_percentage(78, 100)
        78.0
    """
    if total_count == 0:
        return 0.0
    
    return (mapped_count / total_count) * 100


def compare_with_tolerance(
    expected: Dict[str, float],
    actual: Dict[str, float],
    tolerance: float = 2.0
) -> Dict[str, Dict[str, Any]]:
    """
    Compare multiple expected vs actual values with tolerance
    
    Args:
        expected: Dictionary of expected values
        actual: Dictionary of actual values
        tolerance: Tolerance percentage (default: 2%)
    
    Returns:
        Dictionary with comparison results for each key
    
    Example:
        >>> expected = {"current_ratio": 2.0, "debt_to_equity": 1.5}
        >>> actual = {"current_ratio": 2.03, "debt_to_equity": 1.48}
        >>> results = compare_with_tolerance(expected, actual, tolerance=2.0)
        >>> results["current_ratio"]["within_tolerance"]
        True
    """
    results = {}
    
    for key in expected.keys():
        exp_val = expected[key]
        act_val = actual.get(key)
        
        if act_val is not None:
            within_tolerance, pct_diff = check_tolerance(exp_val, act_val, tolerance)
            
            results[key] = {
                "expected": exp_val,
                "actual": act_val,
                "percentage_diff": pct_diff,
                "within_tolerance": within_tolerance,
                "tolerance": tolerance
            }
        else:
            results[key] = {
                "expected": exp_val,
                "actual": None,
                "percentage_diff": None,
                "within_tolerance": False,
                "tolerance": tolerance,
                "error": "MISSING_ACTUAL_VALUE"
            }
    
    return results


def validate_bounds_consistency(
    bounds: Dict[str, Tuple[float, float]]
) -> List[str]:
    """
    Validate that all bounds have min < max
    
    Args:
        bounds: Dictionary mapping ratio_code to (min_val, max_val)
    
    Returns:
        List of error messages for inconsistent bounds
    
    Example:
        >>> bounds = {"current_ratio": (0.1, 15.0), "bad_ratio": (10.0, 5.0)}
        >>> errors = validate_bounds_consistency(bounds)
        >>> len(errors)
        1
    """
    errors = []
    
    for ratio_code, (min_val, max_val) in bounds.items():
        if min_val >= max_val:
            errors.append(f"{ratio_code}: min ({min_val}) >= max ({max_val})")
    
    return errors
