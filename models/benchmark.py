"""
Sector benchmark and comparison models
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, Boolean, 
    Text, ForeignKey, UniqueConstraint, Index, BigInteger
)
from sqlalchemy.orm import relationship

from core.database import Base


class SectorBenchmark(Base):
    """Sector benchmark statistics for financial ratios"""
    
    __tablename__ = "sector_benchmarks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Sector and ratio identification
    sector_main = Column(String(50), nullable=False, index=True)
    ratio_code = Column(String(50), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)
    
    # Statistical measures
    median_ew = Column(Numeric(12, 6), nullable=True)     # Equal-weighted median
    median_wt = Column(Numeric(12, 6), nullable=True)     # Market-cap weighted median
    p25 = Column(Numeric(12, 6), nullable=True)           # 25th percentile
    p75 = Column(Numeric(12, 6), nullable=True)           # 75th percentile
    mean_value = Column(Numeric(12, 6), nullable=True)    # Arithmetic mean
    std_dev = Column(Numeric(12, 6), nullable=True)       # Standard deviation
    
    # Sample characteristics
    n_peers = Column(Integer, nullable=False)             # Number of companies included
    n_excluded = Column(Integer, nullable=False)          # Number of companies excluded
    reliability = Column(String(20), nullable=False, index=True)  # 'HIGH','MEDIUM','LOW','INSUFFICIENT'
    
    # Quality metrics
    data_quality_score = Column(Numeric(3, 2), nullable=True)  # 0.0-1.0
    outlier_pct = Column(Numeric(5, 2), nullable=True)         # Percentage of outliers removed
    
    # Computation metadata
    computed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    is_stale = Column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    peers = relationship("SectorBenchmarkPeer", back_populates="benchmark", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("sector_main", "ratio_code", "period_key", name="uq_benchmarks_sector_ratio_period"),
        Index("idx_benchmarks_sector_period", "sector_main", "period_key"),
        Index("idx_benchmarks_reliability", "reliability", "computed_at"),
    )
    
    def __repr__(self):
        return f"<SectorBenchmark {self.sector_main} {self.ratio_code}: {self.median_ew}>"


class SectorBenchmarkPeer(Base):
    """Companies included/excluded from sector benchmarks (audit trail)"""
    
    __tablename__ = "sector_benchmark_peers"
    
    benchmark_id = Column(Integer, ForeignKey("sector_benchmarks.id"), nullable=False, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    
    # Company's ratio data
    ratio_value = Column(Numeric(12, 6), nullable=True)
    market_cap = Column(BigInteger, nullable=True)  # For weighting
    
    # Inclusion status
    is_included = Column(Boolean, nullable=False, index=True)
    exclusion_reason = Column(String(100), nullable=True)  # F1-F5 filter reason
    
    # Filter pipeline details
    filter_stage = Column(String(20), nullable=True)  # 'F1', 'F2', 'F3', 'F4', 'F5'
    filter_details = Column(Text, nullable=True)      # JSON with filter specifics
    
    # Relationships
    benchmark = relationship("SectorBenchmark", back_populates="peers")
    
    __table_args__ = (
        UniqueConstraint("benchmark_id", "ticker", name="uq_benchmark_peers_id_ticker"),
        Index("idx_benchmark_peers_included", "is_included"),
        Index("idx_benchmark_peers_ticker", "ticker"),
    )
    
    def __repr__(self):
        status = "included" if self.is_included else "excluded"
        return f"<SectorBenchmarkPeer {self.ticker}: {status}>"


class ComparisonResult(Base):
    """Pre-computed comparison results for performance"""
    
    __tablename__ = "comparison_results"
    
    # Comparison identification
    ticker = Column(String(10), ForeignKey("companies.ticker"), nullable=False, index=True)
    comparison_type = Column(String(20), nullable=False, index=True)  # 'sector', 'peers', 'index'
    comparison_target = Column(String(50), nullable=False)  # sector name, peer ticker, index code
    period_key = Column(String(20), nullable=False, index=True)
    
    # Comparison metrics (stored as JSON for flexibility)
    comparison_data = Column(Text, nullable=False)  # JSON with detailed comparison
    
    # Summary metrics
    overall_score = Column(Numeric(5, 2), nullable=True)      # 0-100 overall comparison score
    percentile_rank = Column(Numeric(5, 2), nullable=True)    # Percentile in comparison group
    
    # Metadata
    computed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)
    
    __table_args__ = (
        UniqueConstraint(
            "ticker", "comparison_type", "comparison_target", "period_key", 
            name="uq_comparisons_ticker_type_target_period"
        ),
        Index("idx_comparisons_type_target", "comparison_type", "comparison_target"),
        Index("idx_comparisons_expires", "expires_at"),
    )
    
    def __repr__(self):
        return f"<ComparisonResult {self.ticker} vs {self.comparison_target}: {self.overall_score}>"


class AIContextCache(Base):
    """Cache for AI-generated financial analysis contexts"""
    
    __tablename__ = "ai_context_cache"
    
    # Cache identification
    cache_type = Column(String(50), nullable=False, index=True)  # 'company_fundamental', 'sector_comparison'
    cache_key = Column(String(200), nullable=False, index=True)  # 'THYAO_2026Q1', 'Banking_2026Q1'
    
    # Context data
    context_data = Column(Text, nullable=False)  # The generated context text
    context_metadata = Column(Text, nullable=True)  # JSON with generation metadata
    
    # Cache management
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)
    hit_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        UniqueConstraint("cache_type", "cache_key", name="uq_ai_cache_type_key"),
        Index("idx_ai_cache_expires", "expires_at"),
        Index("idx_ai_cache_accessed", "last_accessed"),
    )
    
    def __repr__(self):
        return f"<AIContextCache {self.cache_type}:{self.cache_key}>"