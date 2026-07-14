"""
Financial statements and ratio models
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, Boolean, 
    Text, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship

from core.database import Base


class FetchLog(Base):
    """Audit log for data fetching operations"""
    
    __tablename__ = "fetch_logs"
    
    ticker = Column(String(10), ForeignKey("companies.ticker"), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)  # '2026Q1', '2025Q4'
    
    # Fetch metadata
    fetched_at = Column(DateTime(timezone=True), nullable=False, index=True)
    http_status = Column(Integer, nullable=True)
    response_size = Column(Integer, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    
    # Diff detection  
    checksum_md5 = Column(String(32), nullable=True, index=True)
    is_new_data = Column(Boolean, nullable=False, default=False, index=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="fetch_logs")
    
    __table_args__ = (
        Index("idx_fetch_logs_ticker_period", "ticker", "period_key"),
        Index("idx_fetch_logs_new_data", "is_new_data", "fetched_at"),
    )
    
    def __repr__(self):
        return f"<FetchLog {self.ticker} {self.period_key}: {self.is_new_data}>"


class FinancialStatementRaw(Base):
    """Raw financial statement data from İş Yatırım API"""
    
    __tablename__ = "financial_statements_raw"
    
    ticker = Column(String(10), ForeignKey("companies.ticker"), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)  # '2025Q3'
    
    # Period details
    year = Column(Integer, nullable=False, index=True)
    period = Column(Integer, nullable=False, index=True)  # 3,6,9,12
    financial_group = Column(String(20), nullable=False, index=True)  # 'UFRS_K', 'XI_29'
    
    # Item details  
    item_code = Column(String(20), nullable=False, index=True)
    item_desc_tr = Column(String(500), nullable=True)
    item_desc_en = Column(String(500), nullable=True)
    
    # Values
    value_try = Column(Numeric(20, 2), nullable=True)
    
    # Metadata
    fetched_at = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="financial_statements")
    
    __table_args__ = (
        UniqueConstraint("ticker", "period_key", "item_code", name="uq_statements_ticker_period_item"),
        Index("idx_statements_ticker_period", "ticker", "period_key"),
        Index("idx_statements_item_code", "item_code"),
    )
    
    def __repr__(self):
        return f"<FinancialStatementRaw {self.ticker} {self.period_key} {self.item_code}>"


class CompanyRatio(Base):
    """Calculated financial ratios"""
    
    __tablename__ = "company_ratios"
    
    ticker = Column(String(10), ForeignKey("companies.ticker"), nullable=False, index=True)
    period_key = Column(String(20), nullable=False, index=True)
    
    # Ratio details
    ratio_code = Column(String(50), nullable=False, index=True)  # 'current_ratio', 'roe'
    ratio_value = Column(Numeric(12, 6), nullable=True)
    
    # Calculation metadata
    is_ttm = Column(Boolean, default=False, nullable=False)  # TTM calculation?
    calculation_method = Column(String(100), nullable=True)   # Description of calculation
    data_quality_score = Column(Numeric(3, 2), nullable=True)  # 0.0-1.0
    
    # Computation timestamp
    computed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Relationships
    company = relationship("Company", back_populates="ratios")
    
    __table_args__ = (
        UniqueConstraint("ticker", "period_key", "ratio_code", name="uq_ratios_ticker_period_code"),
        Index("idx_ratios_ticker_code", "ticker", "ratio_code"),
        Index("idx_ratios_period_code", "period_key", "ratio_code"),
    )
    
    def __repr__(self):
        return f"<CompanyRatio {self.ticker} {self.ratio_code}: {self.ratio_value}>"


class ItemCodeMapping(Base):
    """Mapping İş Yatırım item codes to semantic names"""
    
    __tablename__ = "item_code_mappings"
    
    # Source details
    financial_group = Column(String(20), nullable=False, index=True)  # 'UFRS_K', 'XI_29'
    item_code = Column(String(20), nullable=False, index=True)
    
    # Semantic mapping
    semantic_name = Column(String(100), nullable=False, index=True)  # 'total_assets', 'net_income'
    description_tr = Column(String(500), nullable=True)
    description_en = Column(String(500), nullable=True)
    
    # Classification
    statement_type = Column(String(20), nullable=False, index=True)  # 'balance_sheet', 'income_statement'
    category = Column(String(20), nullable=False, index=True)  # 'asset', 'liability', 'revenue', 'expense'
    
    # Usage
    is_primary = Column(Boolean, default=True, nullable=False)  # Primary vs derived items
    priority = Column(Integer, default=1000, nullable=False)   # Lower = higher priority
    
    __table_args__ = (
        UniqueConstraint("financial_group", "item_code", name="uq_mappings_group_code"),
        UniqueConstraint("financial_group", "semantic_name", name="uq_mappings_group_semantic"),
        Index("idx_mappings_semantic", "semantic_name"),
    )
    
    def __repr__(self):
        return f"<ItemCodeMapping {self.financial_group} {self.item_code} -> {self.semantic_name}>"