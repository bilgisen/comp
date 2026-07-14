"""
Economic Bounds Configuration - Fixture Data

Defines economic validity bounds for ratio values by sector.
Used in F3 filter for benchmark calculations.
"""
from typing import Dict, Tuple

# Economic bounds: (min_value, max_value)
ECONOMIC_BOUNDS: Dict[str, Dict[str, Tuple[float, float]]] = {
    # Default bounds for industrial companies
    "_default": {
        # Liquidity Ratios
        "current_ratio": (0.1, 15.0),
        "acid_test_ratio": (0.05, 12.0),
        
        # Leverage Ratios
        "debt_to_equity": (-2.0, 25.0),  # Negative possible during restructuring
        "debt_ratio": (0.0, 15.0),
        "net_debt_to_equity": (-5.0, 30.0),
        
        # Profitability Margins
        "gross_margin": (-0.50, 0.95),
        "operating_margin": (-0.50, 0.80),
        "net_margin": (-2.00, 0.60),
        "ebitda_margin": (-0.50, 0.80),
        
        # Return Ratios
        "roe": (-1.00, 1.50),  # -100% to +150%
        "roa": (-0.30, 0.40),  # -30% to +40%
        
        # Valuation Ratios
        "pe_ratio": (0.0, 150.0),
        "pb_ratio": (0.0, 20.0),
        "ev_ebitda": (0.0, 60.0),
        
        # Efficiency Ratios
        "asset_turnover": (0.0, 5.0),
        "inventory_turnover": (0.0, 50.0),
        "receivables_turnover": (0.0, 50.0),
    },
    
    # Banking sector specific bounds
    "Bankacılık & Finans": {
        # Banking Profitability
        "net_interest_margin": (-0.02, 0.12),  # -2% to +12%
        "cost_income_ratio": (0.0, 1.5),
        
        # Banking Asset Quality
        "loan_to_deposit": (0.30, 2.50),  # 30% to 250%
        "npl_ratio": (0.0, 0.25),  # 0% to 25%
        
        # Banking Capital
        "capital_adequacy": (0.08, 0.40),  # 8% to 40%
        
        # Banking Returns
        "roe": (-0.30, 0.50),  # -30% to +50%
        "roa": (-0.05, 0.08),  # -5% to +8%
        
        # Banking Valuation
        "pe_ratio": (0.0, 25.0),  # Lower than industrial
        "pb_ratio": (0.0, 5.0),   # Lower than industrial
    },
}

# Rationale for Economic Bounds
BOUNDS_RATIONALE = {
    "current_ratio": "Below 0.1 indicates severe liquidity crisis. Above 15 suggests inefficient capital allocation or data error.",
    "debt_to_equity": "Negative values possible during restructuring (negative equity). Above 25 indicates extreme leverage or error.",
    "roe": "Negative during losses. Above 150% suggests unsustainable returns or accounting issues.",
    "loan_to_deposit": "Banking-specific. Below 0.3 indicates excess deposits. Above 2.5 indicates aggressive lending.",
    "npl_ratio": "Non-performing loan ratio. Above 25% indicates systemic asset quality issues.",
    "capital_adequacy": "Banking capital requirement. Minimum 8% by regulation. Above 40% unusual.",
}
