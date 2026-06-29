"""
Scoring Engine Module
Main scoring engine that computes company scores from ratios and benchmarks

Flow:
1. Load company ratios and peer data
2. For each ratio: compute sigmoid score with reliability dampening
3. Aggregate ratio scores into pillar scores
4. Aggregate pillar scores into composite scores (sektor + genel)
"""

import math
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from .ratio_scorer import compute_ratio_score, apply_reliability_dampening, get_reliability_level
from .pillar_config import (
    PillarConfig,
    RatioWeight,
    get_pillar_config,
    GENEL_PILLARS,
)

logger = logging.getLogger(__name__)


@dataclass
class RatioScoreDetail:
    """Detailed score information for a single ratio"""
    ratio_code: str
    ratio_value: Optional[float]
    peer_median: Optional[float]
    peer_p25: Optional[float]
    peer_p75: Optional[float]
    ratio_score: Optional[float]          # Final score (after dampening)
    ratio_score_raw: Optional[float]      # Raw score (before dampening)
    pillar: str
    scope: str                            # 'sektor' or 'genel'
    higher_is_better: bool
    reliability: Optional[str]


@dataclass
class PillarScoreResult:
    """Score result for a single pillar"""
    pillar_name: str
    pillar_score: Optional[float]         # Weighted average (0-100)
    pillar_weight: float
    n_ratios_available: int
    n_ratios_total: int
    ratio_details: List[RatioScoreDetail] = field(default_factory=list)


@dataclass
class CompanyScoreResult:
    """Complete scoring result for a company"""
    ticker: str
    period_key: str
    sector_main: str
    
    # Composite scores
    score_sektor: Optional[float]
    score_genel: Optional[float]
    
    # Pillar scores (sector-relative)
    pillar_scores: List[PillarScoreResult]
    
    # Reliability
    reliability_sektor: str
    reliability_genel: str
    n_peers_sektor: int
    n_peers_genel: int
    
    # Quality metrics
    pillar_coverage: float
    data_quality_score: float
    
    # All details for DB storage
    score_details: List[RatioScoreDetail] = field(default_factory=list)


def compute_pillar_score(
    pillar: PillarConfig,
    company_ratios: Dict[str, float],
    peer_ratio_values: Dict[str, List[float]],
    median_data: Dict[str, Dict],
    scope: str = "sektor",
) -> PillarScoreResult:
    """
    Compute weighted average score for a single pillar.
    
    Weight normalization: Available ratios' weights are normalized
    so missing ratios don't bias the result.
    
    Args:
        pillar: Pillar configuration
        company_ratios: {ratio_code: value} for target company
        peer_ratio_values: {ratio_code: [peer values]} for peer group
        median_data: {ratio_code: {median_ew, p25, p75, reliability}}
        scope: 'sektor' or 'genel'
    
    Returns:
        PillarScoreResult with aggregated score and details
    """
    ratio_details: List[RatioScoreDetail] = []
    weighted_scores: List[tuple] = []
    total_available_weight = 0.0
    
    for ratio_cfg in pillar.ratios:
        ratio_code = ratio_cfg.ratio_code
        value = company_ratios.get(ratio_code)
        
        # Get peer data
        peers = peer_ratio_values.get(ratio_code, [])
        med_info = median_data.get(ratio_code, {})
        reliability = med_info.get("reliability", "INSUFFICIENT")
        
        # Create detail record
        detail = RatioScoreDetail(
            ratio_code=ratio_code,
            ratio_value=value,
            peer_median=med_info.get("median_ew"),
            peer_p25=med_info.get("p25"),
            peer_p75=med_info.get("p75"),
            ratio_score=None,
            ratio_score_raw=None,
            pillar=pillar.name,
            scope=scope,
            higher_is_better=ratio_cfg.higher_is_better,
            reliability=reliability,
        )
        
        # Check if we can compute score
        if value is None or not math.isfinite(value):
            ratio_details.append(detail)
            continue
        
        if len(peers) < 3:
            ratio_details.append(detail)
            continue
        
        # Compute raw sigmoid score
        raw_score = compute_ratio_score(
            value=value,
            peer_values=peers,
            higher_is_better=ratio_cfg.higher_is_better,
        )
        
        if raw_score is None:
            ratio_details.append(detail)
            continue
        
        # Apply reliability dampening
        final_score = apply_reliability_dampening(raw_score, reliability)
        
        detail.ratio_score_raw = raw_score
        detail.ratio_score = final_score
        ratio_details.append(detail)
        
        # Add to weighted sum
        if final_score is not None:
            weighted_scores.append((final_score, ratio_cfg.weight))
            total_available_weight += ratio_cfg.weight
    
    # Check minimum ratios
    n_available = sum(1 for d in ratio_details if d.ratio_score is not None)
    
    if n_available < pillar.min_ratios:
        return PillarScoreResult(
            pillar_name=pillar.name,
            pillar_score=None,
            pillar_weight=pillar.weight,
            n_ratios_available=n_available,
            n_ratios_total=len(pillar.ratios),
            ratio_details=ratio_details,
        )
    
    # Compute weighted average with normalized weights
    if total_available_weight == 0 or not weighted_scores:
        pillar_score = None
    else:
        pillar_score = sum(
            score * (w / total_available_weight)
            for score, w in weighted_scores
        )
        pillar_score = round(pillar_score, 2)
    
    return PillarScoreResult(
        pillar_name=pillar.name,
        pillar_score=pillar_score,
        pillar_weight=pillar.weight,
        n_ratios_available=n_available,
        n_ratios_total=len(pillar.ratios),
        ratio_details=ratio_details,
    )


def compute_composite_score(
    pillar_results: List[PillarScoreResult],
) -> tuple[Optional[float], str, float]:
    """
    Aggregate pillar scores into composite score.
    
    Args:
        pillar_results: List of pillar score results
    
    Returns:
        (composite_score, reliability_label, pillar_coverage)
    """
    weighted_scores: List[tuple] = []
    total_available_weight = 0.0
    n_pillars_ok = 0
    
    for pr in pillar_results:
        if pr.pillar_score is not None:
            weighted_scores.append((pr.pillar_score, pr.pillar_weight))
            total_available_weight += pr.pillar_weight
            n_pillars_ok += 1
    
    total_pillars = len(pillar_results)
    
    # Calculate pillar coverage
    coverage = n_pillars_ok / total_pillars if total_pillars > 0 else 0
    
    # Determine reliability from coverage
    if coverage >= 0.875:       # 7/8 or 4/4 pillars
        reliability = "HIGH"
    elif coverage >= 0.625:     # 5/8 or 3/4 pillars
        reliability = "MEDIUM"
    elif coverage >= 0.375:     # 3/8 or 2/4 pillars
        reliability = "LOW"
    else:
        reliability = "INSUFFICIENT"
    
    # Check minimum weight coverage
    if total_available_weight < 0.50 or n_pillars_ok == 0:
        return None, "INSUFFICIENT", coverage
    
    # Compute weighted average
    composite = sum(
        score * (w / total_available_weight)
        for score, w in weighted_scores
    )
    
    return round(composite, 2), reliability, coverage


def compute_company_score(
    ticker: str,
    period_key: str,
    sector_main: str,
    company_ratios: Dict[str, float],
    sektor_peer_values: Dict[str, List[float]],
    sektor_median_data: Dict[str, Dict],
    n_peers_sektor: int,
    genel_peer_values: Dict[str, List[float]],
    genel_median_data: Dict[str, Dict],
    n_peers_genel: int,
) -> CompanyScoreResult:
    """
    Compute both sector and general scores for a company.
    
    This is the main entry point for scoring a single company.
    
    Args:
        ticker: Company ticker
        period_key: Period key (e.g., '2026Q1')
        sector_main: Main sector name
        company_ratios: {ratio_code: value} for target company
        sektor_peer_values: {ratio_code: [values]} for sector peers
        sektor_median_data: {ratio_code: {median, p25, p75, reliability}} for sector
        n_peers_sektor: Number of sector peers
        genel_peer_values: {ratio_code: [values]} for all BIST
        genel_median_data: {ratio_code: {median, p25, p75, reliability}} for all BIST
        n_peers_genel: Number of all BIST peers
    
    Returns:
        CompanyScoreResult with all scores and details
    """
    # Get pillar configuration for sector
    sektor_pillar_cfgs = get_pillar_config(sector_main)
    
    # ── SEKTOR SCORE ────────────────────────────────────────────────────────
    sektor_pillar_results: List[PillarScoreResult] = []
    for pillar_cfg in sektor_pillar_cfgs:
        result = compute_pillar_score(
            pillar=pillar_cfg,
            company_ratios=company_ratios,
            peer_ratio_values=sektor_peer_values,
            median_data=sektor_median_data,
            scope="sektor",
        )
        sektor_pillar_results.append(result)
    
    score_sektor, reliability_sektor, coverage_sektor = compute_composite_score(
        sektor_pillar_results
    )
    
    # ── GENEL SCORE ──────────────────────────────────────────────────────────
    genel_pillar_results: List[PillarScoreResult] = []
    for pillar_cfg in GENEL_PILLARS:
        result = compute_pillar_score(
            pillar=pillar_cfg,
            company_ratios=company_ratios,
            peer_ratio_values=genel_peer_values,
            median_data=genel_median_data,
            scope="genel",
        )
        genel_pillar_results.append(result)
    
    score_genel, reliability_genel, coverage_genel = compute_composite_score(
        genel_pillar_results
    )
    
    # Combine all details
    all_details: List[RatioScoreDetail] = []
    for pr in sektor_pillar_results + genel_pillar_results:
        all_details.extend(pr.ratio_details)
    
    # Calculate overall quality metrics
    pillar_coverage = coverage_sektor  # Use sector coverage as main metric
    data_quality_score = sum(
        1 for d in all_details 
        if d.ratio_score is not None
    ) / len(all_details) if all_details else 0
    
    return CompanyScoreResult(
        ticker=ticker,
        period_key=period_key,
        sector_main=sector_main,
        score_sektor=score_sektor,
        score_genel=score_genel,
        pillar_scores=sektor_pillar_results,
        reliability_sektor=reliability_sektor,
        reliability_genel=reliability_genel,
        n_peers_sektor=n_peers_sektor,
        n_peers_genel=n_peers_genel,
        pillar_coverage=pillar_coverage,
        data_quality_score=data_quality_score,
        score_details=all_details,
    )
