"""
HissePro Trend Analysis Service
Analyzes historical financial ratio trends and patterns

Author: Kiro AI Assistant
"""

import logging
import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import numpy as np
from scipy import stats
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, text, func
from sqlalchemy.orm import selectinload

from models.company import Company
from models.financial import CompanyRatio
from core.cache import redis_client

logger = logging.getLogger(__name__)


class TrendDirection(Enum):
    """Trend direction classification"""
    STRONGLY_IMPROVING = "strongly_improving"
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    STRONGLY_DECLINING = "strongly_declining"
    VOLATILE = "volatile"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass
class TrendMetric:
    """Single ratio trend analysis result"""
    ratio_code: str
    periods: List[str]
    values: List[float]
    direction: TrendDirection
    slope: float
    r_squared: float
    volatility: float
    latest_value: float
    change_1q: Optional[float]  # Quarter-over-quarter
    change_1y: Optional[float]  # Year-over-year
    change_cagr: Optional[float]  # Compound Annual Growth Rate
    significance: str  # 'high' | 'medium' | 'low'
    
    
@dataclass
class TrendSummary:
    """Overall company trend summary"""
    total_ratios: int
    improving_count: int
    declining_count: int
    stable_count: int
    overall_momentum: str  # 'positive' | 'negative' | 'neutral'
    momentum_score: float  # -100 to +100
    key_improvements: List[str]
    key_deteriorations: List[str]

class TrendAnalysisService:
    """
    Analyzes historical financial ratio trends and patterns
    
    Capabilities:
    - Multi-period trend analysis with statistical significance
    - Quarter-over-quarter and year-over-year changes
    - Volatility and consistency metrics
    - Sector-relative trend comparisons
    - Leading indicator identification
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_company_trends(
        self, 
        ticker: str,
        periods: int = 8,  # Default: 2 years of quarterly data
        ratio_codes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive trend analysis for a company
        
        Args:
            ticker: Company ticker
            periods: Number of historical periods to analyze
            ratio_codes: Specific ratios to analyze, all if None
        """
        try:
            logger.info(f"📈 Analyzing trends for {ticker} ({periods} periods)")
            
            # Get company info
            company = await self._get_company_info(ticker)
            if not company:
                raise ValueError(f"Company {ticker} not found")
            
            # Get historical ratio data
            historical_data = await self._get_historical_ratios(
                ticker, periods, ratio_codes
            )
            
            if not historical_data:
                return {
                    "ticker": ticker,
                    "status": "no_data",
                    "message": "Insufficient historical data for trend analysis"
                }
            
            # Analyze trends for each ratio
            trend_metrics = []
            
            for ratio_code, ratio_data in historical_data.items():
                if len(ratio_data["values"]) >= 3:  # Minimum for trend analysis
                    metric = self._analyze_single_ratio_trend(
                        ratio_code, ratio_data["periods"], ratio_data["values"]
                    )
                    trend_metrics.append(metric)
            
            # Generate trend summary
            trend_summary = self._generate_trend_summary(trend_metrics)
            
            # Get sector trend context
            sector_trends = await self._get_sector_trend_context(
                company["sector_main"], periods, [m.ratio_code for m in trend_metrics]
            )
            
            response = {
                "ticker": ticker,
                "company_name": company["company_name"],
                "sector": company["sector_main"],
                "analysis_period": {
                    "periods_analyzed": periods,
                    "data_points": len(trend_metrics),
                    "date_range": self._get_date_range(historical_data)
                },
                "trend_summary": {
                    "total_ratios": trend_summary.total_ratios,
                    "improving_count": trend_summary.improving_count,
                    "declining_count": trend_summary.declining_count,
                    "stable_count": trend_summary.stable_count,
                    "overall_momentum": trend_summary.overall_momentum,
                    "momentum_score": trend_summary.momentum_score,
                    "key_improvements": trend_summary.key_improvements,
                    "key_deteriorations": trend_summary.key_deteriorations
                },
                "detailed_trends": [
                    {
                        "ratio_code": metric.ratio_code,
                        "ratio_name": self._get_ratio_display_name(metric.ratio_code),
                        "category": self._get_ratio_category(metric.ratio_code),
                        "direction": metric.direction.value,
                        "slope": round(metric.slope, 6) if metric.slope else None,
                        "r_squared": round(metric.r_squared, 3) if metric.r_squared else None,
                        "volatility": round(metric.volatility, 3) if metric.volatility else None,
                        "latest_value": metric.latest_value,
                        "change_1q": round(metric.change_1q, 3) if metric.change_1q else None,
                        "change_1y": round(metric.change_1y, 3) if metric.change_1y else None,
                        "change_cagr": round(metric.change_cagr, 3) if metric.change_cagr else None,
                        "significance": metric.significance,
                        "periods_count": len(metric.periods),
                        "trend_interpretation": self._interpret_trend(metric)
                    }
                    for metric in trend_metrics
                ],
                "sector_context": sector_trends
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Trend analysis failed for {ticker}: {e}", exc_info=True)
            raise
    async def compare_trends(
        self, 
        ticker1: str, 
        ticker2: str,
        periods: int = 8
    ) -> Dict[str, Any]:
        """
        Compare trend patterns between two companies
        
        Useful for peer analysis and relative performance assessment
        """
        try:
            logger.info(f"📊 Comparing trends: {ticker1} vs {ticker2}")
            
            # Get trend analysis for both companies
            trends1 = await self.analyze_company_trends(ticker1, periods)
            trends2 = await self.analyze_company_trends(ticker2, periods)
            
            if trends1.get("status") == "no_data" or trends2.get("status") == "no_data":
                raise ValueError("Insufficient data for one or both companies")
            
            # Find common ratios
            ratios1 = {t["ratio_code"]: t for t in trends1["detailed_trends"]}
            ratios2 = {t["ratio_code"]: t for t in trends2["detailed_trends"]}
            common_ratios = set(ratios1.keys()) & set(ratios2.keys())
            
            # Compare trends ratio by ratio
            trend_comparisons = []
            
            for ratio_code in common_ratios:
                t1 = ratios1[ratio_code]
                t2 = ratios2[ratio_code]
                
                comparison = {
                    "ratio_code": ratio_code,
                    "ratio_name": t1["ratio_name"],
                    "category": t1["category"],
                    "company1": {
                        "direction": t1["direction"],
                        "slope": t1["slope"],
                        "change_1y": t1["change_1y"],
                        "significance": t1["significance"]
                    },
                    "company2": {
                        "direction": t2["direction"],
                        "slope": t2["slope"],
                        "change_1y": t2["change_1y"],
                        "significance": t2["significance"]
                    },
                    "trend_advantage": self._determine_trend_advantage(t1, t2),
                    "divergence": self._calculate_trend_divergence(t1, t2)
                }
                
                trend_comparisons.append(comparison)
            
            # Generate comparison summary
            comparison_summary = self._generate_trend_comparison_summary(
                trends1, trends2, trend_comparisons
            )
            
            response = {
                "comparison_type": "trend_comparison",
                "company1": {
                    "ticker": ticker1,
                    "name": trends1["company_name"],
                    "sector": trends1["sector"]
                },
                "company2": {
                    "ticker": ticker2, 
                    "name": trends2["company_name"],
                    "sector": trends2["sector"]
                },
                "analysis_period": trends1["analysis_period"],
                "comparison_summary": comparison_summary,
                "detailed_comparisons": trend_comparisons
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Trend comparison failed: {e}", exc_info=True)
            raise
    async def _get_company_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get basic company information"""
        
        query = select(Company).where(Company.ticker == ticker)
        result = await self.db.execute(query)
        company = result.scalar_one_or_none()
        
        if not company:
            return None
            
        return {
            "company_name": company.company_name,
            "sector_main": company.sector_main,
            "is_active": company.is_active
        }

    async def _get_historical_ratios(
        self, 
        ticker: str, 
        periods: int,
        ratio_codes: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, List]]:
        """Get historical ratio data for trend analysis"""
        
        # Build query for historical ratios
        query = text("""
            SELECT ratio_code, period_key, ratio_value, created_at
            FROM company_ratios
            WHERE ticker = :ticker
              AND ratio_value IS NOT NULL
            ORDER BY created_at DESC
            LIMIT :limit
        """)
        
        # Multiply by estimated ratios per period (typically 15-20)
        limit = periods * 25
        
        result = await self.db.execute(query, {
            "ticker": ticker,
            "limit": limit
        })
        
        # Group by ratio code and sort by period
        ratio_data = {}
        
        for row in result.fetchall():
            ratio_code = row.ratio_code
            period_key = row.period_key
            ratio_value = float(row.ratio_value)
            
            # Filter by ratio codes if specified
            if ratio_codes and ratio_code not in ratio_codes:
                continue
            
            if ratio_code not in ratio_data:
                ratio_data[ratio_code] = {"periods": [], "values": []}
            
            # Avoid duplicates and limit to requested periods
            if (period_key not in ratio_data[ratio_code]["periods"] and 
                len(ratio_data[ratio_code]["periods"]) < periods):
                
                ratio_data[ratio_code]["periods"].append(period_key)
                ratio_data[ratio_code]["values"].append(ratio_value)
        
        # Sort each ratio's data by period (chronological order)
        for ratio_code in ratio_data:
            # Combine and sort by period_key (assuming YYYYQX format)
            combined = list(zip(
                ratio_data[ratio_code]["periods"],
                ratio_data[ratio_code]["values"]
            ))
            combined.sort(key=lambda x: x[0])
            
            ratio_data[ratio_code]["periods"] = [x[0] for x in combined]
            ratio_data[ratio_code]["values"] = [x[1] for x in combined]
        
        return ratio_data

    def _analyze_single_ratio_trend(
        self, 
        ratio_code: str,
        periods: List[str], 
        values: List[float]
    ) -> TrendMetric:
        """Analyze trend for a single ratio"""
        
        # Handle insufficient data
        if len(values) < 3:
            return TrendMetric(
                ratio_code=ratio_code,
                periods=periods,
                values=values,
                direction=TrendDirection.INSUFFICIENT_DATA,
                slope=None,
                r_squared=None,
                volatility=None,
                latest_value=values[-1] if values else None,
                change_1q=None,
                change_1y=None,
                change_cagr=None,
                significance="low"
            )
        
        # Clean data (remove any remaining None/NaN values)
        clean_data = [(i, v) for i, v in enumerate(values) if v is not None and math.isfinite(v)]
        
        if len(clean_data) < 3:
            return TrendMetric(
                ratio_code=ratio_code,
                periods=periods,
                values=values,
                direction=TrendDirection.INSUFFICIENT_DATA,
                slope=None,
                r_squared=None,
                volatility=None,
                latest_value=values[-1] if values else None,
                change_1q=None,
                change_1y=None,
                change_cagr=None,
                significance="low"
            )
        
        x_values = np.array([x[0] for x in clean_data])
        y_values = np.array([x[1] for x in clean_data])
        
        # Linear regression for trend
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
        r_squared = r_value ** 2
        
        # Calculate volatility (coefficient of variation)
        volatility = np.std(y_values) / np.mean(y_values) if np.mean(y_values) != 0 else 0
        
        # Calculate period changes
        latest_value = y_values[-1]
        
        # Quarter-over-quarter (if at least 2 periods)
        change_1q = None
        if len(y_values) >= 2:
            change_1q = (y_values[-1] - y_values[-2]) / abs(y_values[-2]) if y_values[-2] != 0 else None
        
        # Year-over-year (if at least 5 periods, assuming quarterly data)
        change_1y = None
        if len(y_values) >= 5:
            change_1y = (y_values[-1] - y_values[-5]) / abs(y_values[-5]) if y_values[-5] != 0 else None
        
        # CAGR (Compound Annual Growth Rate)
        change_cagr = None
        if len(y_values) >= 4:  # At least 1 year of quarterly data
            years = len(y_values) / 4.0  # Convert quarters to years
            if y_values[0] > 0 and years > 0:
                change_cagr = (y_values[-1] / y_values[0]) ** (1/years) - 1
        
        # Determine trend direction
        direction = self._classify_trend_direction(slope, r_squared, volatility)
        
        # Assess significance
        significance = self._assess_trend_significance(r_squared, p_value, len(y_values))
        
        return TrendMetric(
            ratio_code=ratio_code,
            periods=[periods[i] for i in range(len(periods)) if i < len(values)],
            values=y_values.tolist(),
            direction=direction,
            slope=slope,
            r_squared=r_squared,
            volatility=volatility,
            latest_value=latest_value,
            change_1q=change_1q,
            change_1y=change_1y,
            change_cagr=change_cagr,
            significance=significance
        )
    def _classify_trend_direction(
        self, 
        slope: float, 
        r_squared: float, 
        volatility: float
    ) -> TrendDirection:
        """Classify trend direction based on statistical measures"""
        
        # High volatility indicates unstable/volatile trend
        if volatility > 0.5:  # 50% coefficient of variation
            return TrendDirection.VOLATILE
        
        # Low R-squared indicates no clear trend (stable/noisy)
        if r_squared < 0.3:
            return TrendDirection.STABLE
        
        # Classify based on slope magnitude
        slope_abs = abs(slope)
        
        if slope > 0:  # Positive trend
            if slope_abs > 0.1:  # Strong positive trend
                return TrendDirection.STRONGLY_IMPROVING
            else:  # Moderate positive trend
                return TrendDirection.IMPROVING
        else:  # Negative trend
            if slope_abs > 0.1:  # Strong negative trend
                return TrendDirection.STRONGLY_DECLINING
            else:  # Moderate negative trend
                return TrendDirection.DECLINING

    def _assess_trend_significance(
        self, 
        r_squared: float, 
        p_value: float, 
        n_points: int
    ) -> str:
        """Assess statistical significance of trend"""
        
        # Multiple criteria for significance
        if r_squared >= 0.7 and p_value <= 0.05 and n_points >= 6:
            return "high"
        elif r_squared >= 0.4 and p_value <= 0.1 and n_points >= 4:
            return "medium"
        else:
            return "low"

    def _generate_trend_summary(self, trend_metrics: List[TrendMetric]) -> TrendSummary:
        """Generate overall trend summary for company"""
        
        if not trend_metrics:
            return TrendSummary(
                total_ratios=0,
                improving_count=0,
                declining_count=0,
                stable_count=0,
                overall_momentum="neutral",
                momentum_score=0.0,
                key_improvements=[],
                key_deteriorations=[]
            )
        
        # Count trend directions
        improving_count = len([m for m in trend_metrics 
                             if m.direction in [TrendDirection.IMPROVING, TrendDirection.STRONGLY_IMPROVING]])
        declining_count = len([m for m in trend_metrics
                             if m.direction in [TrendDirection.DECLINING, TrendDirection.STRONGLY_DECLINING]])
        stable_count = len([m for m in trend_metrics
                          if m.direction in [TrendDirection.STABLE, TrendDirection.VOLATILE]])
        
        # Calculate momentum score (-100 to +100)
        total_ratios = len(trend_metrics)
        momentum_score = ((improving_count - declining_count) / total_ratios) * 100
        
        # Determine overall momentum
        if momentum_score >= 20:
            overall_momentum = "positive"
        elif momentum_score <= -20:
            overall_momentum = "negative"
        else:
            overall_momentum = "neutral"
        
        # Identify key improvements and deteriorations (high significance only)
        key_improvements = [
            m.ratio_code for m in trend_metrics
            if (m.direction in [TrendDirection.STRONGLY_IMPROVING, TrendDirection.IMPROVING] and
                m.significance == "high")
        ]
        
        key_deteriorations = [
            m.ratio_code for m in trend_metrics
            if (m.direction in [TrendDirection.STRONGLY_DECLINING, TrendDirection.DECLINING] and
                m.significance == "high")
        ]
        
        return TrendSummary(
            total_ratios=total_ratios,
            improving_count=improving_count,
            declining_count=declining_count,
            stable_count=stable_count,
            overall_momentum=overall_momentum,
            momentum_score=momentum_score,
            key_improvements=key_improvements,
            key_deteriorations=key_deteriorations
        )

    async def _get_sector_trend_context(
        self, 
        sector_main: str,
        periods: int, 
        ratio_codes: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Get sector-wide trend context for comparison"""
        
        try:
            # This would require aggregating trends across sector companies
            # For now, return placeholder structure
            return {
                "sector_main": sector_main,
                "analysis_note": "Sector trend analysis requires broader implementation",
                "available": False
            }
        except Exception as e:
            logger.warning(f"Could not get sector trend context: {e}")
            return None

    def _get_date_range(self, historical_data: Dict[str, Dict[str, List]]) -> Dict[str, str]:
        """Extract date range from historical data"""
        
        all_periods = []
        for ratio_data in historical_data.values():
            all_periods.extend(ratio_data["periods"])
        
        if not all_periods:
            return {"start": None, "end": None}
        
        all_periods.sort()
        return {
            "start": all_periods[0],
            "end": all_periods[-1]
        }

    def _get_ratio_display_name(self, ratio_code: str) -> str:
        """Get user-friendly ratio name"""
        display_names = {
            "current_ratio": "Cari Oran",
            "acid_test_ratio": "Asit Test Oranı",
            "gross_margin": "Brüt Kar Marjı",
            "ebitda_margin": "FAVÖK Marjı",
            "net_margin": "Net Kar Marjı",
            "roe": "Özsermaye Karlılığı (ROE)",
            "roa": "Aktif Karlılığı (ROA)",
            "debt_ratio": "Borçlanma Oranı",
            "debt_to_equity": "Borç/Özsermaye",
            "pe_ratio": "F/K Oranı",
            "pb_ratio": "PD/DD Oranı"
        }
        return display_names.get(ratio_code, ratio_code.replace("_", " ").title())

    def _get_ratio_category(self, ratio_code: str) -> str:
        """Get ratio category for grouping"""
        liquidity_ratios = ["current_ratio", "acid_test_ratio", "cash_ratio"]
        profitability_ratios = ["gross_margin", "ebitda_margin", "net_margin", "roe", "roa"]
        leverage_ratios = ["debt_ratio", "debt_to_equity", "interest_coverage"]
        valuation_ratios = ["pe_ratio", "pb_ratio", "ev_ebitda", "price_to_sales"]
        
        if ratio_code in liquidity_ratios:
            return "liquidity"
        elif ratio_code in profitability_ratios:
            return "profitability"
        elif ratio_code in leverage_ratios:
            return "leverage"
        elif ratio_code in valuation_ratios:
            return "valuation"
        else:
            return "other"
    def _interpret_trend(self, metric: TrendMetric) -> str:
        """Generate human-readable trend interpretation"""
        
        if metric.direction == TrendDirection.INSUFFICIENT_DATA:
            return "Yetersiz veri - trend analizi yapılamıyor"
        
        direction_map = {
            TrendDirection.STRONGLY_IMPROVING: "Güçlü iyileşme trendi",
            TrendDirection.IMPROVING: "Olumlu trend",
            TrendDirection.STABLE: "Sabit/değişken trend", 
            TrendDirection.DECLINING: "Olumsuz trend",
            TrendDirection.STRONGLY_DECLINING: "Güçlü kötüleşme trendi",
            TrendDirection.VOLATILE: "Değişken/dengesiz trend"
        }
        
        base_interpretation = direction_map.get(metric.direction, "Belirsiz trend")
        
        # Add significance context
        if metric.significance == "high":
            base_interpretation += " (yüksek güvenilirlik)"
        elif metric.significance == "medium":
            base_interpretation += " (orta güvenilirlik)"
        else:
            base_interpretation += " (düşük güvenilirlik)"
        
        # Add recent change context
        if metric.change_1q and abs(metric.change_1q) > 0.1:  # 10%+ quarterly change
            change_text = "artış" if metric.change_1q > 0 else "azalış"
            base_interpretation += f", son çeyrekte %{abs(metric.change_1q)*100:.1f} {change_text}"
        
        return base_interpretation

    def _determine_trend_advantage(self, trend1: Dict, trend2: Dict) -> str:
        """Determine which company has better trend for this ratio"""
        
        # Get trend directions
        dir1 = trend1["direction"]
        dir2 = trend2["direction"] 
        
        # Simple comparison based on trend direction
        improving_trends = ["strongly_improving", "improving"]
        declining_trends = ["strongly_declining", "declining"]
        
        if dir1 in improving_trends and dir2 not in improving_trends:
            return "company1"
        elif dir2 in improving_trends and dir1 not in improving_trends:
            return "company2"
        elif dir1 in declining_trends and dir2 not in declining_trends:
            return "company2"
        elif dir2 in declining_trends and dir1 not in declining_trends:
            return "company1"
        else:
            # Compare slopes if both have similar directions
            slope1 = trend1.get("slope", 0) or 0
            slope2 = trend2.get("slope", 0) or 0
            
            if abs(slope1 - slope2) < 0.01:  # Very similar slopes
                return "neutral"
            elif slope1 > slope2:
                return "company1"
            else:
                return "company2"

    def _calculate_trend_divergence(self, trend1: Dict, trend2: Dict) -> Dict[str, Any]:
        """Calculate how much the trends are diverging"""
        
        slope1 = trend1.get("slope", 0) or 0
        slope2 = trend2.get("slope", 0) or 0
        
        slope_difference = abs(slope1 - slope2)
        
        # Categorize divergence
        if slope_difference < 0.02:
            divergence_level = "low"
        elif slope_difference < 0.05:
            divergence_level = "medium"
        else:
            divergence_level = "high"
        
        return {
            "slope_difference": round(slope_difference, 4),
            "level": divergence_level,
            "direction": "converging" if (slope1 > 0 and slope2 > 0) or (slope1 < 0 and slope2 < 0) else "diverging"
        }

    def _generate_trend_comparison_summary(
        self, 
        trends1: Dict,
        trends2: Dict, 
        comparisons: List[Dict]
    ) -> Dict[str, Any]:
        """Generate summary of trend comparison between two companies"""
        
        total_ratios = len(comparisons)
        
        # Count advantages
        company1_advantages = len([c for c in comparisons if c["trend_advantage"] == "company1"])
        company2_advantages = len([c for c in comparisons if c["trend_advantage"] == "company2"])
        neutral_count = len([c for c in comparisons if c["trend_advantage"] == "neutral"])
        
        # Overall trend momentum comparison
        momentum1 = trends1["trend_summary"]["momentum_score"]
        momentum2 = trends2["trend_summary"]["momentum_score"]
        
        momentum_advantage = "company1" if momentum1 > momentum2 else "company2"
        if abs(momentum1 - momentum2) < 10:  # Close momentum scores
            momentum_advantage = "neutral"
        
        return {
            "total_ratios_compared": total_ratios,
            "company1_advantages": company1_advantages,
            "company2_advantages": company2_advantages,
            "neutral_count": neutral_count,
            "momentum_comparison": {
                "company1_score": momentum1,
                "company2_score": momentum2,
                "advantage": momentum_advantage
            },
            "key_divergences": [
                comp["ratio_code"] for comp in comparisons
                if comp["divergence"]["level"] == "high"
            ]
        }