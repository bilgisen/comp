"""
Database configuration and session management (Dual Sync/Async version)
"""

import logging
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from core.config import settings

logger = logging.getLogger(__name__)

# Synchronous DB URL (replace asyncpg)
sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
async_db_url = settings.database_url

logger.info("Initializing Dual Sync/Async Database Engines")

# 1. Create Synchronous Engine & Session
engine = create_engine(
    sync_db_url,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DEBUG,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 2. Create Asynchronous Engine & Session
async_engine = create_async_engine(
    async_db_url,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DEBUG,
    future=True
)
AsyncSessionLocal = async_sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base model class with common fields"""
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


def get_db() -> Generator[Session, None, None]:
    """Dependency to get synchronous database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get asynchronous database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables and cache connection"""
    try:
        # Import all models to ensure they're registered
        from models import company, financial, benchmark  # noqa
        
        # Create all tables synchronously using sync engine
        Base.metadata.create_all(bind=engine)
            
        logger.info("✅ Database tables created/updated successfully")
        
        # Initialize cache connection
        from core.cache import redis_client
        await redis_client.connect()
        
        logger.info("✅ Database and cache initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def close_db():
    """Close database and cache connections"""
    try:
        # Close cache connection
        from core.cache import redis_client
        await redis_client.disconnect()
    except Exception as e:
        logger.warning(f"Cache disconnect warning: {e}")
    
    engine.dispose()
    await async_engine.dispose()
    logger.info("✅ Database and cache connections closed")
