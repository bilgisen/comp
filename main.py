"""
HissePro Financial Analysis Engine (COMP)
FastAPI backend for pro-level fundamental analysis

Author: Kiro AI Assistant
Version: 2.0.0
"""

import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from core.database import get_db, init_db
from routers import companies, sectors, admin, ai_context
from services.scheduler import SchedulerService

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting HissePro Financial Analysis Engine...")
    
    # Initialize database
    await init_db()
    logger.info("✅ Database initialized")
    
    # Start scheduler (if enabled)
    if settings.ENABLE_SCHEDULER:
        scheduler = SchedulerService()
        await scheduler.start()
        logger.info("✅ Scheduler started")
        app.state.scheduler = scheduler
    
    logger.info("🎯 COMP Engine ready for pro-level financial analysis!")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down COMP Engine...")
    if hasattr(app.state, 'scheduler'):
        await app.state.scheduler.stop()
        logger.info("✅ Scheduler stopped")
    
    # Close database and cache
    from core.database import close_db
    await close_db()


# FastAPI app
app = FastAPI(
    title="HissePro Financial Analysis Engine",
    description="Pro-level fundamental analysis API with sector benchmarks and AI context",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "hissepro-comp",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",  # TODO: Add actual DB health check
        "cache": "connected"      # TODO: Add actual cache health check
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "HissePro Financial Analysis Engine",
        "version": "2.0.0",
        "documentation": "/docs",
        "endpoints": {
            "companies": "/api/v1/companies/",
            "sectors": "/api/v1/sectors/", 
            "admin": "/api/v1/admin/",
            "ai_context": "/api/v1/ai/"
        },
        "features": [
            "Mali tablo çekimi (İş Yatırım API)",
            "50+ finansal rasyo hesaplama",
            "Sektör benchmark'ları (F1-F5 filtreli)",
            "AI context generation",
            "Real-time data updates"
        ]
    }

# Include routers
app.include_router(companies.router, prefix="/api/v1/companies", tags=["Companies"])
app.include_router(sectors.router, prefix="/api/v1/sectors", tags=["Sectors"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(ai_context.router, prefix="/api/v1/ai", tags=["AI Context"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )