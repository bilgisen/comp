"""
Company Score Models
Rating system with sector and general scores
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, Boolean, 
    Text, ForeignKey, UniqueConstraint, Index, BigInteger
)
from sqlalchemy.orm import relationship

from core.database import Base


class CompanyScore(Base):
    """
    Company rating scores (0-100 scale)
    
    Two independent scores:
    - score_sektor: Position within sector peers
    - score_genel: Position across all BIST companies
    """
    
    __tablename__ = "company_scores"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Company identification
    ticker = Column(String(10), ForeignKey("companies.ticker"), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)  # '2026Q1', '2025Q4'
    
    # Composite scores (0-100)
    score_sektor = Column(Numeric(5, 2), nullable=True)  # Sector-relative score
    score_genel = Column(Numeric(5, 2), nullable=True)   # Market-wide score
    
    # Pillar scores (sector-normalized, components of score_sektor)
    score_karlilik = Column(Numeric(5, 2), nullable=True)   # Profitability
    score_finansal = Column(Numeric(5, 2), nullable=True)   # Financial Health
    score_verimlilik = Column(Numeric(5, 2), nullable=True) # Efficiency
    score_degerleme = Column(Numeric(5, 2), nullable=True)  # Valuation (if data available)
    
    # Reliability indicators
    reliability_sektor = Column(String(20), nullable=True, index=True)  # HIGH, MEDIUM, LOW, INSUFFICIENT
    reliability_genel = Column(String(20), nullable=True, index=True)
    n_peers_sektor = Column(Integer, nullable=True)  # Number of sector peers
    n_peers_genel = Column(Integer, nullable=True)   # Number of all BIST peers
    
    # Data quality
    pillar_coverage = Column(Numeric(3, 2), nullable=True)  # 0.0-1.0, how many pillars available
    data_quality_score = Column(Numeric(3, 2), nullable=True)
    
    # Metadata
    computed_at = Column(DateTime(timezone=True), nullable=False, index=True, default=datetime.utcnow)
    is_stale = Column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    details = relationship("CompanyScoreDetail", back_populates="score", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("ticker", "period_key", name="uq_company_scores_ticker_period"),
        Index("idx_company_scores_sektor", "score_sektor"),
        Index("idx_company_scores_genel", "score_genel"),
        Index("idx_company_scores_period", "period_key"),
    )
    
    def __repr__(self):
        return f"<CompanyScore {self.ticker} {self.period_key}: S={self.score_sektor} G={self.score_genel}>"


class CompanyScoreDetail(Base):
    """
    Detailed ratio-level scores for explainability
    
    Stores the breakdown of how each ratio contributed to the final score
    """
    
    __tablename__ = "company_score_details"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Link to main score
    score_id = Column(BigInteger, ForeignKey("company_scores.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Company identification (for easier querying)
    ticker = Column(String(10), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)
    
    # Ratio identification
    ratio_code = Column(String(50), nullable=False, index=True)  # 'gross_margin', 'roe', etc.
    
    # Values
    ratio_value = Column(Numeric(12, 6), nullable=True)   # Raw ratio value
    peer_median = Column(Numeric(12, 6), nullable=True)   # Sector median
    peer_p25 = Column(Numeric(12, 6), nullable=True)      # 25th percentile
    peer_p75 = Column(Numeric(12, 6), nullable=True)      # 75th percentile
    
    # Score (0-100)
    ratio_score = Column(Numeric(5, 2), nullable=True)      # Final score (after dampening)
    ratio_score_raw = Column(Numeric(5, 2), nullable=True)  # Raw score (before dampening)
    
    # Classification
    pillar = Column(String(20), nullable=False, index=True)  # 'karlilik', 'finansal', 'verimlilik', 'degerleme'
    scope = Column(String(20), nullable=False, index=True)   # 'sektor' or 'genel'
    higher_is_better = Column(Boolean, nullable=False, default=True)
    
    # Reliability
    reliability = Column(String(20), nullable=True)  # Reliability of this ratio's benchmark
    
    # Metadata
    computed_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    # Relationships
    score = relationship("CompanyScore", back_populates="details")
    
    __table_args__ = (
        UniqueConstraint("score_id", "ratio_code", "scope", name="uq_score_details_ratio_scope"),
        Index("idx_score_details_ticker_period", "ticker", "period_key"),
        Index("idx_score_details_pillar", "pillar"),
    )
    
    def __repr__(self):
        return f"<CompanyScoreDetail {self.ticker} {self.ratio_code}: {self.ratio_score}>"


class GlobalBenchmark(Base):
    """
    Market-wide benchmarks for score_genel calculation
    
    Similar to sector_benchmarks but for all BIST companies
    """
    
    __tablename__ = "global_benchmarks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Ratio identification
    ratio_code = Column(String(50), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)
    
    # Statistical measures (all BIST companies)
    median_ew = Column(Numeric(12, 6), nullable=True)     # Equal-weighted median
    median_wt = Column(Numeric(12, 6), nullable=True)     # Market-cap weighted median
    p25 = Column(Numeric(12, 6), nullable=True)           # 25th percentile
    p75 = Column(Numeric(12, 6), nullable=True)           # 75th percentile
    mean_value = Column(Numeric(12, 6), nullable=True)    # Arithmetic mean
    std_dev = Column(Numeric(12, 6), nullable=True)       # Standard deviation
    
    # Sample characteristics
    n_peers = Column(Integer, nullable=False)             # Total companies
    n_excluded = Column(Integer, nullable=False)          # Excluded companies
    reliability = Column(String(20), nullable=False, index=True)  # HIGH, MEDIUM, LOW
    
    # Quality metrics
    data_quality_score = Column(Numeric(3, 2), nullable=True)
    outlier_pct = Column(Numeric(5, 2), nullable=True)
    
    # Computation metadata
    computed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    is_stale = Column(Boolean, default=False, nullable=False, index=True)
    
    __table_args__ = (
        UniqueConstraint("ratio_code", "period_key", name="uq_global_benchmarks_ratio_period"),
        Index("idx_global_benchmarks_period", "period_key"),
    )
    
    def __repr__(self):
        return f"<GlobalBenchmark {self.ratio_code} {self.period_key}: median={self.median_ew}>"
