"""
Configuration management using Pydantic Settings
"""

import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "HissePro COMP Engine"
    VERSION: str = "2.0.0"
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")
    HOST: str = Field(default="0.0.0.0", validation_alias="HOST") 
    PORT: int = Field(default=8000, validation_alias="PORT")
    
    # Database (PostgreSQL)
    DATABASE_URL: Optional[str] = Field(default=None, validation_alias="DATABASE_URL")
    OVH_DATABASE_URL: Optional[str] = Field(default=None, validation_alias="OVH_DATABASE_URL")
    OVH_SSL_CERT: Optional[str] = Field(default=None, validation_alias="OVH_SSL_CERT")
    DB_HOST: str = Field(default="localhost", validation_alias="DB_HOST")
    DB_PORT: int = Field(default=5432, validation_alias="DB_PORT") 
    DB_USER: str = Field(default="postgres", validation_alias="DB_USER")
    DB_PASSWORD: str = Field(default="", validation_alias="DB_PASSWORD")
    DB_NAME: str = Field(default="hissepro_comp", validation_alias="DB_NAME")
    DB_POOL_SIZE: int = Field(default=10, validation_alias="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=20, validation_alias="DB_MAX_OVERFLOW")
    
    # Redis/Valkey (Cache)
    REDIS_URL: Optional[str] = Field(default=None, validation_alias="REDIS_URL")
    REDIS_HOST: str = Field(default="localhost", validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, validation_alias="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(default=None, validation_alias="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, validation_alias="REDIS_DB")
    
    # İş Yatırım API
    ISYATIRIM_BASE_URL: str = "https://www.isyatirim.com.tr"
    ISYATIRIM_TIMEOUT: int = 30
    ISYATIRIM_RATE_LIMIT: int = 20  # requests per minute
    ISYATIRIM_DELAY: float = 3.0    # seconds between requests
    ISYATIRIM_BATCH_SIZE: int = 50  # companies per batch
    ISYATIRIM_SESSION_BREAK: int = 120  # seconds between batches
    
    # Scheduler
    ENABLE_SCHEDULER: bool = Field(default=True, validation_alias="ENABLE_SCHEDULER")
    SCHEDULER_TIMEZONE: str = "Europe/Istanbul"
    
    # Fetch Schedule
    DAILY_FETCH_TIME: str = "07:00"      # TSI
    WEEKLY_FETCH_TIME: str = "04:00"     # Pazar
    FETCH_LOOKBACK_DAYS: int = 75        # KAP raporlama penceresi
    
    # Cache TTL (seconds)
    RATIO_CACHE_TTL: int = 86400         # 24 hours
    BENCHMARK_CACHE_TTL: int = 43200     # 12 hours  
    AI_CONTEXT_CACHE_TTL: int = 21600    # 6 hours
    
    # Filter Pipeline
    MIN_PERIODS_REQUIRED: int = 3        # F2 filter
    MIN_PEERS_FOR_BENCHMARK: int = 3     # F5 filter
    WINSORIZATION_PERCENTILES: tuple = (5, 95)  # F4 filter
    
    # Security  
    SECRET_KEY: str = Field(default="dev-secret-key", validation_alias="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default=["*"], validation_alias="ALLOWED_ORIGINS")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, validation_alias="ENABLE_METRICS") 
    SENTRY_DSN: Optional[str] = Field(default=None, validation_alias="SENTRY_DSN")
    
    # Celery (Background Tasks)
    CELERY_BROKER_URL: Optional[str] = Field(default=None, validation_alias="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, validation_alias="CELERY_RESULT_BACKEND")
    
    # AI Integration
    GEMINI_API_KEY: Optional[str] = Field(default=None, validation_alias="GEMINI_API_KEY")
    HONO_BASE_URL: str = Field(default="http://localhost:8787", validation_alias="HONO_BASE_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        """Construct database URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    @property 
    def redis_url(self) -> str:
        """Construct Redis URL"""
        if self.REDIS_URL:
            return self.REDIS_URL
            
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


# Global settings instance
settings = Settings()