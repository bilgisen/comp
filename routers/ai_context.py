"""
AI Context API endpoints  
"""

import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.cache import redis_client

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/context/{ticker}")
async def build_ai_context(
    ticker: str,
    context_type: str = Query("comprehensive", description="Context type: 'basic', 'comprehensive', 'comparison'"),
    force_refresh: bool = Query(False, description="Force refresh cached context"),
    db: Session = Depends(get_db)
):
    """
    Build AI context for financial analysis chatbot
    
    Returns formatted context optimized for Gemini AI consumption.
    """
    ticker = ticker.upper()
    
    try:
        from services.ai_context_builder import AIContextBuilder
        
        # Check cache first (unless force refresh)
        if not force_refresh:
            cached_context = await redis_client.get_ai_context(ticker, context_type)
            if cached_context:
                return {
                    "ticker": ticker,
                    "context_type": context_type,
                    "context": cached_context,
                    "cache_hit": True,
                    "generated_at": datetime.utcnow().isoformat()
                }
        
        # Build fresh context
        context_builder = AIContextBuilder(db)
        context = await context_builder.build_context(ticker, context_type)
        
        # Cache the result
        await redis_client.set_ai_context(ticker, context_type, context)
        
        return {
            "ticker": ticker,
            "context_type": context_type,  
            "context": context,
            "cache_hit": False,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error building AI context for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/context/{ticker}/invalidate")
async def invalidate_ai_context(
    ticker: str,
    context_type: Optional[str] = Query(None, description="Specific context type to invalidate"),
    db: Session = Depends(get_db)
):
    """
    Invalidate cached AI context for a company
    
    Admin endpoint to force context regeneration.
    """
    ticker = ticker.upper()
    
    try:
        if context_type:
            # Invalidate specific context type
            cache_key = f"ai_context:{ticker}:{context_type}"
            deleted = await redis_client.delete(cache_key)
        else:
            # Invalidate all context types for this ticker
            pattern = f"ai_context:{ticker}:*"
            deleted = await redis_client.delete_pattern(pattern)
        
        return {
            "ticker": ticker,
            "context_type": context_type,
            "invalidated_entries": deleted,
            "invalidated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error invalidating context for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")