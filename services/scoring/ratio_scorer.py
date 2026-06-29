"""
Ratio Scorer Module
Sigmoid-based percentile scoring algorithm

Key features:
- Outlier-resistant (IQR-based normalization)
- Asymptotic 0/100 bounds (extremes never reach 0 or 100)
- Reliability dampening for small peer groups
"""

import math
import numpy as np
from typing import Optional, List

import logging

logger = logging.getLogger(__name__)


# Reliability dampening factors
# Lower reliability = score pulled closer to median (50)
RELIABILITY_DAMPENING = {
    "HIGH":         1.00,   # No dampening (n >= 10)
    "MEDIUM":       0.80,   # 20% toward median (n: 5-9)
    "LOW":          0.55,   # 45% toward median (n: 3-4)
    "INSUFFICIENT": None,   # Don't produce score
}


def compute_ratio_score(
    value: float,
    peer_values: List[float],
    higher_is_better: bool = True,
    sigmoid_steepness: float = 0.8,
) -> Optional[float]:
    """
    Compute sigmoid-normalized score (0-100) for a ratio within peer group.
    
    Algorithm:
      1. Calculate deviation from median (normalized by IQR for outlier resistance)
      2. Apply sigmoid function → S-curve with asymptotic 0/100
      3. Adjust direction (for ratios where lower is better)
    
    Characteristics:
      - Company at median → always 50 points
      - Excellent company → 85-95 range (never reaches 100)
      - Poor company → 5-15 range (never reaches 0)
      - Less than 3 peers → None (unreliable)
    
    Args:
        value: Target company's ratio value
        peer_values: Peer group's ratio values (target can be included or excluded)
        higher_is_better: True = higher value is good (like ROE)
                          False = lower value is good (like debt ratio)
        sigmoid_steepness: Steepness of S-curve (0.8 = balanced)
    
    Returns:
        0.0-100.0 float, or None if insufficient peers
    """
    if not peer_values or len(peer_values) < 3:
        return None
    
    if not math.isfinite(value):
        return None
    
    # Filter valid peer values
    peer_arr = np.array([v for v in peer_values if math.isfinite(v)], dtype=float)
    
    if len(peer_arr) < 3:
        return None
    
    # Calculate robust statistics
    median = float(np.median(peer_arr))
    q25 = float(np.percentile(peer_arr, 25))
    q75 = float(np.percentile(peer_arr, 75))
    iqr = q75 - q25
    
    # IQR = 0 case: all peers have same value
    if iqr < 1e-10:
        return 50.0
    
    # Robust Z-score: IQR/1.349 approximates std for normal distribution
    # 0.7413 = 1 / (2 * 0.6745): conversion factor
    robust_std = iqr / (2 * 0.6745)
    
    if robust_std < 1e-10:
        return 50.0
    
    z = (value - median) / robust_std
    
    # Direction adjustment
    if not higher_is_better:
        z = -z
    
    # Sigmoid transformation: f(z) = 100 / (1 + e^(-k*z))
    try:
        score = 100.0 / (1.0 + math.exp(-sigmoid_steepness * z))
    except OverflowError:
        # Handle extreme z values
        if z > 0:
            score = 99.99
        else:
            score = 0.01
    
    return round(float(np.clip(score, 0.01, 99.99)), 2)


def apply_reliability_dampening(
    raw_score: float,
    reliability: str,
) -> Optional[float]:
    """
    Apply reliability dampening to pull score toward median (50).
    
    When peer group is small (LOW/MEDIUM reliability), extreme scores
    are unreliable. This function pulls them toward 50.
    
    Example: raw_score=80, reliability=LOW
      deviation = 80 - 50 = 30
      dampened  = 50 + (30 * 0.55) = 50 + 16.5 = 66.5
    
    Args:
        raw_score: Score before dampening (0-100)
        reliability: Reliability level (HIGH, MEDIUM, LOW, INSUFFICIENT)
    
    Returns:
        Dampened score (0-100), or None if INSUFFICIENT
    """
    factor = RELIABILITY_DAMPENING.get(reliability)
    
    if factor is None:
        return None  # INSUFFICIENT → no score for this ratio
    
    deviation = raw_score - 50.0
    dampened = 50.0 + (deviation * factor)
    
    return round(float(np.clip(dampened, 0.0, 100.0)), 2)


def get_reliability_level(n_peers: int) -> str:
    """
    Determine reliability level based on number of peers.
    
    Args:
        n_peers: Number of companies in peer group
    
    Returns:
        Reliability level string
    """
    if n_peers >= 10:
        return "HIGH"
    elif n_peers >= 5:
        return "MEDIUM"
    elif n_peers >= 3:
        return "LOW"
    else:
        return "INSUFFICIENT"


def calculate_percentile_rank(
    value: float,
    peer_values: List[float],
) -> Optional[float]:
    """
    Calculate percentile rank of a value within peer group.
    
    Alternative to sigmoid scoring - simpler but less robust to outliers.
    
    Args:
        value: Target value
        peer_values: Peer group values
    
    Returns:
        Percentile rank (0-100), or None if insufficient data
    """
    if not peer_values or len(peer_values) < 2:
        return None
    
    if not math.isfinite(value):
        return None
    
    peer_arr = np.array([v for v in peer_values if math.isfinite(v)], dtype=float)
    
    if len(peer_arr) < 2:
        return None
    
    # Count values below target
    below = np.sum(peer_arr < value)
    equal = np.sum(peer_arr == value)
    
    # Percentile rank formula
    percentile = (below + 0.5 * equal) / len(peer_arr) * 100
    
    return round(float(percentile), 2)
