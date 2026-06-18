"""
Company model and related entities
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Text, Index, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Company(Base):
    """Company/Şirket model"""
    
    __tablename__ = "companies"
    
    # Company identifiers
    ticker = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    
    # Sector classification
    sector_raw = Column(String(100), nullable=True)      # İş Yatırım'dan gelen orijinal
    sector_main = Column(String(50), nullable=False, index=True)  # 14 ana sektörden biri
    
    # Financial metadata
    financial_group = Column(String(20), nullable=False, index=True)  # UFRS_K, XI_29, etc.
    market_cap = Column(BigInteger, nullable=True)       # Güncel piyasa değeri (TRY)
    
    # Company details
    city = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    about = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    fetch_logs = relationship("FetchLog", back_populates="company")
    financial_statements = relationship("FinancialStatementRaw", back_populates="company")
    ratios = relationship("CompanyRatio", back_populates="company")
    
    __table_args__ = (
        Index("idx_companies_sector_active", "sector_main", "is_active"),
        Index("idx_companies_financial_group", "financial_group"),
    )
    
    def __repr__(self):
        return f"<Company {self.ticker}: {self.name}>"


class CompanyMetrics(Base):
    """Company market metrics (updated frequently)"""
    
    __tablename__ = "company_metrics"
    
    ticker = Column(String(10), ForeignKey("companies.ticker"), nullable=False, index=True)
    
    # Market data
    last_price = Column(Numeric(12, 4), nullable=True)
    market_cap = Column(BigInteger, nullable=True) 
    shares_outstanding = Column(BigInteger, nullable=True)
    free_float_pct = Column(Numeric(5, 2), nullable=True)
    
    # Trading metrics  
    volume_1d = Column(BigInteger, nullable=True)
    volume_avg_30d = Column(BigInteger, nullable=True)
    
    # Valuation multiples (live calculated)
    pe_ratio = Column(Numeric(8, 2), nullable=True)
    pb_ratio = Column(Numeric(8, 2), nullable=True)
    
    # Update frequency
    price_updated_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<CompanyMetrics {self.ticker}: {self.last_price} TRY>"