"""
HissePro Comparison Service
Enables company-to-company and company-to-sector comparisons

Author: Kiro AI Assistant
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, text, func
from sqlalchemy.orm import selectinload

from models.company import Company
from models.financial import CompanyRatio
from services.sector_benchmarks import SectorBenchmarkService
from core.cache import redis_client

logger = logging.getLogger(__name__)


@dataclass
class ComparisonMetric:
    """Single ratio comparison result"""
    ratio_code: str
    company_value: Optional[float]
    peer_value: Optional[float] 
    difference: Optional[float]
    percentage_difference: Optional[float]
    advantage: str  # 'company' | 'peer' | 'neutral'
    significance: str  # 'high' | 'medium' | 'low'


@dataclass
class ComparisonSummary:
    """Overall comparison summary"""
    total_ratios: int
    company_advantages: int
    peer_advantages: int
    neutral_count: int
    overall_score: float  # -100 to +100, positive = company better
    strength_areas: List[str]
    weakness_areas: List[str]


class ComparisonService:
    """
    Provides comprehensive company comparison capabilities:
    - Company vs Company (peer comparison)
    - Company vs Sector (benchmark comparison)  
    - Multiple companies vs Sector
    - Historical trend comparisons
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.benchmark_service = SectorBenchmarkService(db)

    async def compare_companies(
        self, 
        company_ticker: str,
        peer_ticker: str, 
        period_key: Optional[str] = None,
        ratio_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare two companies across financial ratios
        
        Args:
            company_ticker: Primary company
            peer_ticker: Comparison company
            period_key: Specific period, latest if None
            ratio_categories: Filter by categories (liquidity, profitability, etc.)
        """
        try:
            logger.info(f"🔍 Comparing {company_ticker} vs {peer_ticker}")
            
            # Get company info
            companies = await self._get_companies_info([company_ticker, peer_ticker])
            if len(companies) != 2:
                raise ValueError("Both companies must exist")
            
            company = companies[company_ticker]
            peer = companies[peer_ticker]
            
            # Check if same sector (affects interpretation)
            same_sector = company["sector_main"] == peer["sector_main"]
            
            # Get latest period if not specified  
            if not period_key:
                period_key = await self._get_latest_period()
            
            # Get ratio data for both companies
            company_ratios = await self._get_company_ratios(company_ticker, period_key)
            peer_ratios = await self._get_company_ratios(peer_ticker, period_key)
            
            # Filter by categories if specified
            if ratio_categories:
                company_ratios = {k: v for k, v in company_ratios.items() 
                                if self._get_ratio_category(k) in ratio_categories}
                peer_ratios = {k: v for k, v in peer_ratios.items()
                             if self._get_ratio_category(k) in ratio_categories}
            
            # Perform ratio-by-ratio comparison
            comparisons = []
            common_ratios = set(company_ratios.keys()) & set(peer_ratios.keys())
            
            for ratio_code in common_ratios:
                comparison = self._compare_single_ratio(
                    ratio_code,
                    company_ratios[ratio_code],
                    peer_ratios[ratio_code]
                )
                comparisons.append(comparison)
            
            # Generate comparison summary
            summary = self._generate_comparison_summary(comparisons)
            
            # Get sector context if same sector
            sector_context = None
            if same_sector:
                sector_context = await self._get_sector_context(
                    company["sector_main"], period_key, list(common_ratios)
                )
            
            response = {
                "comparison_type": "company_vs_company",
                "company": {
                    "ticker": company_ticker,
                    "name": company["company_name"],
                    "sector": company["sector_main"]
                },
                "peer": {
                    "ticker": peer_ticker, 
                    "name": peer["company_name"],
                    "sector": peer["sector_main"]
                },
                "period_key": period_key,
                "same_sector": same_sector,
                "summary": {
                    "total_ratios": summary.total_ratios,
                    "company_advantages": summary.company_advantages,
                    "peer_advantages": summary.peer_advantages,
                    "overall_score": summary.overall_score,
                    "strength_areas": summary.strength_areas,
                    "weakness_areas": summary.weakness_areas
                },
                "detailed_comparisons": [
                    {
                        "ratio_code": comp.ratio_code,
                        "ratio_name": self._get_ratio_display_name(comp.ratio_code),
                        "category": self._get_ratio_category(comp.ratio_code),
                        "company_value": comp.company_value,
                        "peer_value": comp.peer_value,
                        "difference": comp.difference,
                        "percentage_difference": comp.percentage_difference,
                        "advantage": comp.advantage,
                        "significance": comp.significance
                    }
                    for comp in comparisons
                ],
                "sector_context": sector_context
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Company comparison failed: {e}", exc_info=True)
            raise

    async def compare_to_sector(
        self, 
        company_ticker: str,
        period_key: Optional[str] = None,
        ratio_codes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare company performance against sector benchmarks
        
        Returns percentile rankings and sector position analysis
        """
        try:
            logger.info(f"📊 Comparing {company_ticker} to sector")
            
            # Get company info
            companies = await self._get_companies_info([company_ticker])
            company = companies[company_ticker]
            
            # Get latest period if not specified
            if not period_key:
                period_key = await self._get_latest_period()
            
            # Get company ratios
            company_ratios = await self._get_company_ratios(company_ticker, period_key)
            
            # Filter ratios if specified
            if ratio_codes:
                company_ratios = {k: v for k, v in company_ratios.items() if k in ratio_codes}
            
            # Get sector benchmarks
            sector_benchmarks = await self.benchmark_service.get_sector_benchmarks(
                company["sector_main"], period_key, list(company_ratios.keys())
            )
            
            # Calculate percentiles and comparisons
            sector_comparisons = []
            
            for ratio_code, company_value in company_ratios.items():
                if ratio_code in sector_benchmarks["benchmarks"]:
                    # Get detailed percentile
                    percentile_data = await self.benchmark_service.get_company_percentile(
                        company_ticker, ratio_code, period_key
                    )
                    
                    if percentile_data:
                        benchmark = sector_benchmarks["benchmarks"][ratio_code]
                        
                        sector_comparisons.append({
                            "ratio_code": ratio_code,
                            "ratio_name": self._get_ratio_display_name(ratio_code),
                            "category": self._get_ratio_category(ratio_code),
                            "company_value": company_value,
                            "sector_median": benchmark["median_ew"],
                            "sector_p25": benchmark["p25"],
                            "sector_p75": benchmark["p75"],
                            "percentile": percentile_data["percentile"],
                            "vs_sector": percentile_data["vs_sector"],
                            "peer_count": percentile_data["peer_count"],
                            "reliability": benchmark["reliability"],
                            "quartile": self._get_quartile(percentile_data["percentile"]),
                            "interpretation": self._interpret_percentile(
                                percentile_data["percentile"], ratio_code
                            )
                        })
            
            # Generate sector analysis summary
            sector_analysis = self._analyze_sector_position(sector_comparisons)
            
            response = {
                "comparison_type": "company_vs_sector",
                "company": {
                    "ticker": company_ticker,
                    "name": company["company_name"],
                    "sector": company["sector_main"]
                },
                "period_key": period_key,
                "sector_analysis": sector_analysis,
                "detailed_comparisons": sector_comparisons,
                "benchmark_summary": {
                    "total_ratios": len(sector_comparisons),
                    "high_reliability": len([c for c in sector_comparisons if c["reliability"] == "HIGH"]),
                    "medium_reliability": len([c for c in sector_comparisons if c["reliability"] == "MEDIUM"]),
                    "low_reliability": len([c for c in sector_comparisons if c["reliability"] == "LOW"])
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Sector comparison failed: {e}", exc_info=True)
            raise

    async def multi_company_comparison(
        self, 
        tickers: List[str],
        period_key: Optional[str] = None,
        ratio_codes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple companies side-by-side with sector benchmarks
        
        Useful for screening and peer group analysis
        """
        try:
            logger.info(f"📊 Multi-company comparison: {len(tickers)} companies")
            
            if len(tickers) < 2:
                raise ValueError("At least 2 companies required for comparison")
            
            if len(tickers) > 20:
                raise ValueError("Maximum 20 companies allowed")
            
            # Get company info
            companies = await self._get_companies_info(tickers)
            
            # Get latest period if not specified
            if not period_key:
                period_key = await self._get_latest_period()
            
            # Get ratios for all companies
            all_ratios = {}
            for ticker in tickers:
                company_ratios = await self._get_company_ratios(ticker, period_key)
                if ratio_codes:
                    company_ratios = {k: v for k, v in company_ratios.items() if k in ratio_codes}
                all_ratios[ticker] = company_ratios
            
            # Find common ratios across all companies
            common_ratios = set.intersection(*[set(ratios.keys()) for ratios in all_ratios.values()])
            
            if not common_ratios:
                raise ValueError("No common ratios found across companies")
            
            # Group companies by sector for benchmark context
            sectors = {}
            for ticker in tickers:
                sector = companies[ticker]["sector_main"]
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append(ticker)
            
            # Get sector benchmarks for each sector
            sector_benchmarks = {}
            for sector in sectors.keys():
                benchmarks = await self.benchmark_service.get_sector_benchmarks(
                    sector, period_key, list(common_ratios)
                )
                sector_benchmarks[sector] = benchmarks["benchmarks"]
            
            # Build comparison matrix
            comparison_matrix = []
            
            for ratio_code in common_ratios:
                ratio_comparison = {
                    "ratio_code": ratio_code,
                    "ratio_name": self._get_ratio_display_name(ratio_code),
                    "category": self._get_ratio_category(ratio_code),
                    "companies": {},
                    "best_performer": None,
                    "worst_performer": None,
                    "sector_benchmarks": {}
                }
                
                # Add company values
                values = []
                for ticker in tickers:
                    value = all_ratios[ticker].get(ratio_code)
                    company_sector = companies[ticker]["sector_main"]
                    
                    ratio_comparison["companies"][ticker] = {
                        "value": value,
                        "sector": company_sector
                    }
                    
                    if value is not None:
                        values.append((ticker, value))
                
                # Determine best/worst performers (ratio-specific logic)
                if values:
                    is_higher_better = self._is_higher_better(ratio_code)
                    sorted_values = sorted(values, key=lambda x: x[1], reverse=is_higher_better)
                    
                    ratio_comparison["best_performer"] = sorted_values[0][0]
                    ratio_comparison["worst_performer"] = sorted_values[-1][0]
                
                # Add sector benchmarks
                for sector, benchmarks in sector_benchmarks.items():
                    if ratio_code in benchmarks:
                        ratio_comparison["sector_benchmarks"][sector] = {
                            "median": benchmarks[ratio_code]["median_ew"],
                            "p25": benchmarks[ratio_code]["p25"],
                            "p75": benchmarks[ratio_code]["p75"]
                        }
                
                comparison_matrix.append(ratio_comparison)
            
            # Generate rankings
            company_rankings = self._generate_multi_company_rankings(
                tickers, comparison_matrix, companies
            )
            
            response = {
                "comparison_type": "multi_company",
                "companies": [
                    {
                        "ticker": ticker,
                        "name": companies[ticker]["company_name"],
                        "sector": companies[ticker]["sector_main"]
                    }
                    for ticker in tickers
                ],
                "period_key": period_key,
                "sectors_involved": list(sectors.keys()),
                "comparison_matrix": comparison_matrix,
                "company_rankings": company_rankings,
                "summary": {
                    "total_companies": len(tickers),
                    "common_ratios": len(common_ratios),
                    "sectors_count": len(sectors)
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Multi-company comparison failed: {e}", exc_info=True)
            raise

    async def _get_companies_info(self, tickers: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get basic company information"""
        
        query = select(Company).where(Company.ticker.in_(tickers))
        result = await self.db.execute(query)
        companies = result.scalars().all()
        
        return {
            company.ticker: {
                "company_name": company.name,
                "sector_main": company.sector_main,
                "market_cap": float(company.market_cap) if company.market_cap else None,
                "is_active": company.is_active
            }
            for company in companies
        }

    async def _get_company_ratios(
        self, 
        ticker: str, 
        period_key: str
    ) -> Dict[str, float]:
        """Get all ratios for a company in specific period"""
        
        query = select(CompanyRatio).where(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.period_key == period_key
            )
        )
        result = await self.db.execute(query)
        ratios = result.scalars().all()
        
        return {
            ratio.ratio_code: float(ratio.ratio_value) if ratio.ratio_value else None
            for ratio in ratios
        }

    async def _get_latest_period(self) -> str:
        """Get the latest available period key"""
        
        query = text("""
            SELECT period_key 
            FROM company_ratios 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        result = await self.db.execute(query)
        row = result.fetchone()
        
        return row.period_key if row else "2026Q1"

    def _compare_single_ratio(
        self, 
        ratio_code: str,
        company_value: Optional[float], 
        peer_value: Optional[float]
    ) -> ComparisonMetric:
        """Compare single ratio between two companies"""
        
        if company_value is None or peer_value is None:
            return ComparisonMetric(
                ratio_code=ratio_code,
                company_value=company_value,
                peer_value=peer_value,
                difference=None,
                percentage_difference=None,
                advantage="neutral",
                significance="low"
            )
        
        # Calculate differences
        difference = company_value - peer_value
        percentage_difference = (difference / abs(peer_value)) * 100 if peer_value != 0 else None
        
        # Determine advantage (ratio-specific logic)
        is_higher_better = self._is_higher_better(ratio_code)
        
        if abs(percentage_difference or 0) < 5:  # Less than 5% difference
            advantage = "neutral"
        elif (difference > 0 and is_higher_better) or (difference < 0 and not is_higher_better):
            advantage = "company"
        else:
            advantage = "peer"
        
        # Assess significance
        abs_pct_diff = abs(percentage_difference or 0)
        if abs_pct_diff > 25:
            significance = "high"
        elif abs_pct_diff > 10:
            significance = "medium"
        else:
            significance = "low"
        
        return ComparisonMetric(
            ratio_code=ratio_code,
            company_value=company_value,
            peer_value=peer_value,
            difference=difference,
            percentage_difference=percentage_difference,
            advantage=advantage,
            significance=significance
        )

    def _generate_comparison_summary(self, comparisons: List[ComparisonMetric]) -> ComparisonSummary:
        """Generate overall comparison summary"""
        
        total_ratios = len(comparisons)
        company_advantages = len([c for c in comparisons if c.advantage == "company"])
        peer_advantages = len([c for c in comparisons if c.advantage == "peer"]) 
        neutral_count = len([c for c in comparisons if c.advantage == "neutral"])
        
        # Calculate overall score (-100 to +100)
        if total_ratios == 0:
            overall_score = 0.0
        else:
            score = ((company_advantages - peer_advantages) / total_ratios) * 100
            overall_score = max(-100, min(100, score))
        
        # Identify strength and weakness areas
        category_performance = {}
        for comp in comparisons:
            category = self._get_ratio_category(comp.ratio_code)
            if category not in category_performance:
                category_performance[category] = {"company": 0, "peer": 0, "total": 0}
            
            category_performance[category]["total"] += 1
            if comp.advantage == "company":
                category_performance[category]["company"] += 1
            elif comp.advantage == "peer":
                category_performance[category]["peer"] += 1
        
        strength_areas = []
        weakness_areas = []
        
        for category, perf in category_performance.items():
            if perf["total"] >= 2:  # Only consider categories with multiple ratios
                company_ratio = perf["company"] / perf["total"]
                if company_ratio >= 0.67:  # Company wins 2/3+ of ratios
                    strength_areas.append(category)
                elif company_ratio <= 0.33:  # Company wins 1/3- of ratios
                    weakness_areas.append(category)
        
        return ComparisonSummary(
            total_ratios=total_ratios,
            company_advantages=company_advantages,
            peer_advantages=peer_advantages,
            neutral_count=neutral_count,
            overall_score=overall_score,
            strength_areas=strength_areas,
            weakness_areas=weakness_areas
        )

    async def _get_sector_context(
        self, 
        sector_main: str, 
        period_key: str,
        ratio_codes: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Get sector benchmark context for comparison"""
        
        try:
            benchmarks = await self.benchmark_service.get_sector_benchmarks(
                sector_main, period_key, ratio_codes
            )
            return benchmarks
        except Exception as e:
            logger.warning(f"Could not get sector context: {e}")
            return None

    def _analyze_sector_position(self, sector_comparisons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze company's overall position within sector"""
        
        if not sector_comparisons:
            return {}
        
        percentiles = [comp["percentile"] for comp in sector_comparisons if comp["percentile"] is not None]
        
        if not percentiles:
            return {}
        
        avg_percentile = sum(percentiles) / len(percentiles)
        
        # Count quartile distribution
        q1_count = len([p for p in percentiles if p <= 25])
        q2_count = len([p for p in percentiles if 25 < p <= 50])
        q3_count = len([p for p in percentiles if 50 < p <= 75]) 
        q4_count = len([p for p in percentiles if p > 75])
        
        # Determine overall sector position
        if avg_percentile >= 75:
            position = "sector_leader"
        elif avg_percentile >= 60:
            position = "above_average"
        elif avg_percentile >= 40:
            position = "average"
        elif avg_percentile >= 25:
            position = "below_average"
        else:
            position = "underperformer"
        
        return {
            "average_percentile": round(avg_percentile, 1),
            "position": position,
            "quartile_distribution": {
                "q1": q1_count,  # Bottom quartile
                "q2": q2_count,
                "q3": q3_count,
                "q4": q4_count   # Top quartile
            },
            "strength_ratios": [
                comp["ratio_code"] for comp in sector_comparisons 
                if comp["percentile"] and comp["percentile"] >= 75
            ],
            "weakness_ratios": [
                comp["ratio_code"] for comp in sector_comparisons
                if comp["percentile"] and comp["percentile"] <= 25
            ]
        }

    def _generate_multi_company_rankings(
        self, 
        tickers: List[str],
        comparison_matrix: List[Dict[str, Any]],
        companies: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate overall rankings for multi-company comparison"""
        
        # Score each company based on ratio rankings
        company_scores = {ticker: 0 for ticker in tickers}
        
        for ratio_comparison in comparison_matrix:
            ratio_code = ratio_comparison["ratio_code"]
            is_higher_better = self._is_higher_better(ratio_code)
            
            # Get valid values for ranking
            valid_companies = []
            for ticker in tickers:
                value = ratio_comparison["companies"][ticker]["value"]
                if value is not None:
                    valid_companies.append((ticker, value))
            
            if len(valid_companies) < 2:
                continue
            
            # Sort and assign scores
            valid_companies.sort(key=lambda x: x[1], reverse=is_higher_better)
            
            for i, (ticker, _) in enumerate(valid_companies):
                # Award points: 1st place = n points, 2nd = n-1 points, etc.
                company_scores[ticker] += len(valid_companies) - i
        
        # Sort companies by total score
        ranked_companies = sorted(
            company_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Format rankings
        rankings = []
        for rank, (ticker, score) in enumerate(ranked_companies, 1):
            rankings.append({
                "rank": rank,
                "ticker": ticker,
                "company_name": companies[ticker]["company_name"],
                "sector": companies[ticker]["sector_main"],
                "total_score": score,
                "max_possible_score": len(comparison_matrix) * len(tickers)
            })
        
        return rankings

    def _get_ratio_category(self, ratio_code: str) -> str:
        """Get ratio category for grouping"""
        
        liquidity_ratios = ["current_ratio", "acid_test_ratio", "cash_ratio"]
        profitability_ratios = ["gross_margin", "ebitda_margin", "net_margin", "roe", "roa"]
        leverage_ratios = ["debt_ratio", "debt_to_equity", "interest_coverage"]
        valuation_ratios = ["pe_ratio", "pb_ratio", "ev_ebitda", "price_to_sales"]
        efficiency_ratios = ["asset_turnover", "inventory_turnover", "receivables_turnover"]
        banking_ratios = ["net_interest_margin", "loan_to_deposit", "npl_ratio", "capital_adequacy"]
        
        if ratio_code in liquidity_ratios:
            return "liquidity"
        elif ratio_code in profitability_ratios:
            return "profitability"
        elif ratio_code in leverage_ratios:
            return "leverage"
        elif ratio_code in valuation_ratios:
            return "valuation"
        elif ratio_code in efficiency_ratios:
            return "efficiency"
        elif ratio_code in banking_ratios:
            return "banking"
        else:
            return "other"

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
            "pb_ratio": "PD/DD Oranı",
            "ev_ebitda": "FD/FAVÖK",
            "net_interest_margin": "Net Faiz Marjı",
            "loan_to_deposit": "Kredi/Mevduat Oranı",
            "npl_ratio": "NPL Oranı"
        }
        
        return display_names.get(ratio_code, ratio_code.replace("_", " ").title())

    def _is_higher_better(self, ratio_code: str) -> bool:
        """Determine if higher values are better for this ratio"""
        
        higher_better = [
            "current_ratio", "acid_test_ratio", "gross_margin", "ebitda_margin", 
            "net_margin", "roe", "roa", "net_interest_margin", "asset_turnover",
            "inventory_turnover", "receivables_turnover", "capital_adequacy"
        ]
        
        lower_better = [
            "debt_ratio", "debt_to_equity", "pe_ratio", "pb_ratio", "ev_ebitda",
            "npl_ratio", "expense_ratio", "loss_ratio"
        ]
        
        if ratio_code in higher_better:
            return True
        elif ratio_code in lower_better:
            return False
        else:
            # Default: higher is better (most ratios)
            return True

    def _get_quartile(self, percentile: float) -> str:
        """Convert percentile to quartile label"""
        
        if percentile <= 25:
            return "Q1"  # Bottom quartile
        elif percentile <= 50:
            return "Q2"
        elif percentile <= 75:
            return "Q3" 
        else:
            return "Q4"  # Top quartile

    def _interpret_percentile(self, percentile: float, ratio_code: str) -> str:
        """Provide interpretation of percentile rank"""
        
        is_higher_better = self._is_higher_better(ratio_code)
        
        if percentile >= 90:
            return "exceptional" if is_higher_better else "concerning"
        elif percentile >= 75:
            return "strong" if is_higher_better else "weak"
        elif percentile >= 60:
            return "above_average" if is_higher_better else "below_average"
        elif percentile >= 40:
            return "average"
        elif percentile >= 25:
            return "below_average" if is_higher_better else "above_average"
        elif percentile >= 10:
            return "weak" if is_higher_better else "strong"
        else:
            return "concerning" if is_higher_better else "exceptional"