"""
Synthetic Data Generator - Generate controlled test data

Provides functions to generate synthetic financial data, peer data,
and boundary test cases for property-based and unit testing.
"""
from typing import Dict, List, Any, Optional
import random
import math


def generate_financial_data(
    current_assets: Optional[float] = None,
    current_liabilities: Optional[float] = None,
    total_assets: Optional[float] = None,
    shareholders_equity: Optional[float] = None,
    revenue_ttm: Optional[float] = None,
    net_income_ttm: Optional[float] = None,
    seed: Optional[int] = None
) -> Dict[str, float]:
    """
    Generate synthetic financial data with known relationships
    
    Args:
        current_assets: Current assets (if None, generated randomly)
        current_liabilities: Current liabilities
        total_assets: Total assets
        shareholders_equity: Shareholders equity
        revenue_ttm: Revenue TTM
        net_income_ttm: Net income TTM
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary of financial data
    
    Example:
        >>> data = generate_financial_data(
        ...     current_assets=1000.0,
        ...     current_liabilities=500.0
        ... )
        >>> data["current_ratio"]
        2.0
    """
    if seed is not None:
        random.seed(seed)
    
    # Generate base values if not provided
    if current_assets is None:
        current_assets = random.uniform(100000, 10000000)
    if current_liabilities is None:
        current_liabilities = random.uniform(50000, current_assets * 0.8)
    if total_assets is None:
        total_assets = current_assets * random.uniform(1.5, 3.0)
    if shareholders_equity is None:
        shareholders_equity = total_assets * random.uniform(0.3, 0.6)
    if revenue_ttm is None:
        revenue_ttm = total_assets * random.uniform(0.5, 2.0)
    if net_income_ttm is None:
        net_income_ttm = revenue_ttm * random.uniform(0.05, 0.25)
    
    # Calculate derived values
    total_liabilities = total_assets - shareholders_equity
    total_debt = current_liabilities * random.uniform(1.2, 2.0)
    cash_and_equivalents = current_assets * random.uniform(0.1, 0.3)
    inventories = current_assets * random.uniform(0.2, 0.4)
    
    gross_profit_ttm = revenue_ttm * random.uniform(0.2, 0.4)
    operating_income_ttm = gross_profit_ttm * random.uniform(0.6, 0.9)
    ebitda_ttm = operating_income_ttm * random.uniform(1.1, 1.3)
    
    # Averages (for ROE, ROA calculations)
    total_assets_avg = total_assets * random.uniform(0.95, 1.05)
    shareholders_equity_avg = shareholders_equity * random.uniform(0.95, 1.05)
    
    # Market data
    market_cap = shareholders_equity * random.uniform(1.5, 5.0)
    
    return {
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "shareholders_equity": shareholders_equity,
        "total_debt": total_debt,
        "cash_and_equivalents": cash_and_equivalents,
        "inventories": inventories,
        "revenue_ttm": revenue_ttm,
        "gross_profit_ttm": gross_profit_ttm,
        "operating_income_ttm": operating_income_ttm,
        "ebitda_ttm": ebitda_ttm,
        "net_income_ttm": net_income_ttm,
        "total_assets_avg": total_assets_avg,
        "shareholders_equity_avg": shareholders_equity_avg,
        "market_cap": market_cap,
        "net_debt": total_debt - cash_and_equivalents,
        # Calculated ratios for verification
        "current_ratio": current_assets / current_liabilities if current_liabilities != 0 else None,
        "debt_to_equity": total_debt / shareholders_equity if shareholders_equity != 0 else None,
        "roe": net_income_ttm / shareholders_equity_avg if shareholders_equity_avg != 0 else None,
        "roa": net_income_ttm / total_assets_avg if total_assets_avg != 0 else None,
    }


def generate_peer_data(
    scenario: str = "valid",
    n_peers: int = 10,
    ratio_code: str = "current_ratio",
    seed: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Generate synthetic peer data for filter pipeline testing
    
    Args:
        scenario: Test scenario ("valid", "with_nulls", "with_outliers", "insufficient_periods")
        n_peers: Number of peer companies to generate
        ratio_code: Ratio code being tested
        seed: Random seed for reproducibility
    
    Returns:
        List of peer data dictionaries
    
    Scenarios:
        - "valid": All valid data, no issues
        - "with_nulls": Some NULL and infinite values (for F1 filter)
        - "with_outliers": Extreme outliers outside bounds (for F3/F4 filters)
        - "insufficient_periods": Some peers with < minimum periods (for F2 filter)
        - "too_few": Fewer than 3 peers (for F5 filter)
    
    Example:
        >>> peers = generate_peer_data(scenario="valid", n_peers=10)
        >>> len(peers)
        10
        >>> all(peer["ratio_value"] is not None for peer in peers)
        True
    """
    if seed is not None:
        random.seed(seed)
    
    peers = []
    
    if scenario == "valid":
        # All valid data
        for i in range(n_peers):
            peers.append({
                "ticker": f"COMP{i:03d}",
                "ratio_value": random.uniform(0.5, 3.0),
                "market_cap": random.uniform(1e8, 1e11),
                "available_periods": random.randint(4, 12)
            })
    
    elif scenario == "with_nulls":
        # Mix of valid, NULL, and infinite values
        for i in range(n_peers):
            if i % 3 == 0:
                value = None  # NULL
            elif i % 7 == 0:
                value = float('inf')  # Infinite
            else:
                value = random.uniform(0.5, 3.0)
            
            peers.append({
                "ticker": f"COMP{i:03d}",
                "ratio_value": value,
                "market_cap": random.uniform(1e8, 1e11),
                "available_periods": random.randint(4, 12)
            })
    
    elif scenario == "with_outliers":
        # Valid data with extreme outliers
        for i in range(n_peers):
            if i % 5 == 0:
                # Extreme outlier
                value = random.uniform(50.0, 100.0)
            else:
                # Normal range
                value = random.uniform(0.5, 3.0)
            
            peers.append({
                "ticker": f"COMP{i:03d}",
                "ratio_value": value,
                "market_cap": random.uniform(1e8, 1e11),
                "available_periods": random.randint(4, 12)
            })
    
    elif scenario == "insufficient_periods":
        # Some peers with insufficient historical periods
        for i in range(n_peers):
            if i % 4 == 0:
                periods = random.randint(0, 2)  # Insufficient
            else:
                periods = random.randint(4, 12)  # Sufficient
            
            peers.append({
                "ticker": f"COMP{i:03d}",
                "ratio_value": random.uniform(0.5, 3.0),
                "market_cap": random.uniform(1e8, 1e11),
                "available_periods": periods
            })
    
    elif scenario == "too_few":
        # Fewer than 3 peers (F5 filter should reject)
        n_peers = 2
        for i in range(n_peers):
            peers.append({
                "ticker": f"COMP{i:03d}",
                "ratio_value": random.uniform(0.5, 3.0),
                "market_cap": random.uniform(1e8, 1e11),
                "available_periods": random.randint(4, 12)
            })
    
    return peers


def generate_boundary_test_cases(
    ratio_code: str,
    min_bound: float,
    max_bound: float,
    epsilon: float = 0.01
) -> List[Dict[str, Any]]:
    """
    Generate boundary test cases for economic bounds testing
    
    Args:
        ratio_code: Ratio code to test
        min_bound: Minimum bound
        max_bound: Maximum bound
        epsilon: Small value for edge testing
    
    Returns:
        List of test cases with values at boundary edges
    
    Test cases generated:
        - min_bound - epsilon (should be excluded)
        - min_bound (should be included)
        - (min_bound + max_bound) / 2 (middle, should be included)
        - max_bound (should be included)
        - max_bound + epsilon (should be excluded)
    
    Example:
        >>> cases = generate_boundary_test_cases("current_ratio", 0.1, 15.0)
        >>> len(cases)
        5
        >>> cases[0]["expected_result"]
        "EXCLUDE"
    """
    test_cases = []
    
    # Below minimum
    test_cases.append({
        "ratio_code": ratio_code,
        "value": min_bound - epsilon,
        "expected_result": "EXCLUDE",
        "reason": "BELOW_MIN"
    })
    
    # At minimum (inclusive)
    test_cases.append({
        "ratio_code": ratio_code,
        "value": min_bound,
        "expected_result": "INCLUDE",
        "reason": "AT_MIN"
    })
    
    # Middle of range
    test_cases.append({
        "ratio_code": ratio_code,
        "value": (min_bound + max_bound) / 2,
        "expected_result": "INCLUDE",
        "reason": "WITHIN_RANGE"
    })
    
    # At maximum (inclusive)
    test_cases.append({
        "ratio_code": ratio_code,
        "value": max_bound,
        "expected_result": "INCLUDE",
        "reason": "AT_MAX"
    })
    
    # Above maximum
    test_cases.append({
        "ratio_code": ratio_code,
        "value": max_bound + epsilon,
        "expected_result": "EXCLUDE",
        "reason": "ABOVE_MAX"
    })
    
    return test_cases


def generate_outlier_scenarios(
    base_values: List[float],
    outlier_factor: float = 3.0
) -> List[float]:
    """
    Generate dataset with statistical outliers
    
    Args:
        base_values: Base distribution of values
        outlier_factor: Multiplier for creating outliers
    
    Returns:
        List of values including outliers
    
    Example:
        >>> base = [1.0, 1.5, 2.0, 2.5, 3.0]
        >>> with_outliers = generate_outlier_scenarios(base, outlier_factor=3.0)
        >>> max(with_outliers) > max(base) * 2
        True
    """
    if not base_values:
        return []
    
    values = base_values.copy()
    
    # Calculate mean and std
    mean = sum(base_values) / len(base_values)
    variance = sum((x - mean) ** 2 for x in base_values) / len(base_values)
    std = math.sqrt(variance)
    
    # Add outliers (values beyond mean ± outlier_factor * std)
    n_outliers = max(2, len(base_values) // 10)
    
    for _ in range(n_outliers):
        if random.random() < 0.5:
            # Upper outlier
            outlier = mean + outlier_factor * std * random.uniform(1.5, 3.0)
        else:
            # Lower outlier
            outlier = mean - outlier_factor * std * random.uniform(1.5, 3.0)
        
        values.append(outlier)
    
    return values


def generate_quarterly_data(
    annual_value: float,
    n_quarters: int = 4,
    seasonality: bool = True,
    seed: Optional[int] = None
) -> List[float]:
    """
    Generate quarterly data that sums to annual value
    
    Args:
        annual_value: Total annual value
        n_quarters: Number of quarters (default: 4)
        seasonality: Whether to apply seasonal variation
        seed: Random seed for reproducibility
    
    Returns:
        List of quarterly values
    
    Example:
        >>> quarterly = generate_quarterly_data(1000.0, n_quarters=4)
        >>> abs(sum(quarterly) - 1000.0) < 0.01
        True
    """
    if seed is not None:
        random.seed(seed)
    
    if not seasonality:
        # Equal distribution
        q_value = annual_value / n_quarters
        return [q_value] * n_quarters
    
    # Generate seasonal factors (sum to 1.0)
    factors = [random.uniform(0.15, 0.35) for _ in range(n_quarters)]
    factor_sum = sum(factors)
    factors = [f / factor_sum for f in factors]
    
    # Apply factors to get quarterly values
    quarterly_values = [annual_value * f for f in factors]
    
    # Adjust last quarter to ensure exact sum
    adjustment = annual_value - sum(quarterly_values)
    quarterly_values[-1] += adjustment
    
    return quarterly_values


def generate_company_record(
    ticker: str,
    sector_main: str,
    financial_group: str,
    is_active: bool = True
) -> Dict[str, Any]:
    """
    Generate synthetic company record
    
    Args:
        ticker: Company ticker symbol
        sector_main: Sector name
        financial_group: Financial group code
        is_active: Whether company is active
    
    Returns:
        Company record dictionary
    
    Example:
        >>> company = generate_company_record(
        ...     "TEST", 
        ...     "Teknoloji & İletişim", 
        ...     "XI_29"
        ... )
        >>> company["ticker"]
        "TEST"
    """
    return {
        "ticker": ticker,
        "company_name": f"{ticker} A.Ş.",
        "sector_main": sector_main,
        "financial_group": financial_group,
        "market_cap": random.uniform(1e8, 1e11),
        "is_active": is_active
    }
