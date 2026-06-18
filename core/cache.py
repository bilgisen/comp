"""
Redis/Valkey cache management
"""

import json
import logging
from typing import Any, Optional, Dict, Union
from datetime import datetime, timedelta

import redis.asyncio as aioredis
from redis.asyncio import Redis

from core.config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Redis/Valkey cache manager with async support"""
    
    def __init__(self):
        self.redis: Optional[Redis] = None
        self._connected = False
    
    async def connect(self):
        """Connect to Redis/Valkey"""
        try:
            self.redis = aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                max_connections=20
            )
            
            # Test connection
            await self.redis.ping()
            self._connected = True
            logger.info("✅ Connected to Redis/Valkey cache")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis/Valkey: {e}")
            self._connected = False
            # Don't raise - allow app to run without cache
    
    async def disconnect(self):
        """Disconnect from Redis/Valkey"""
        if self.redis:
            await self.redis.aclose()
            self._connected = False
            logger.info("✅ Disconnected from Redis/Valkey cache")
    
    def _serialize(self, value: Any) -> str:
        """Serialize value for storage"""
        if isinstance(value, (dict, list, tuple)):
            return json.dumps(value, default=str)
        return str(value)
    
    def _deserialize(self, value: str) -> Any:
        """Deserialize value from storage"""
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self._connected:
            return None
        
        try:
            value = await self.redis.get(key)
            if value is None:
                return None
            return self._deserialize(value)
            
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache with optional TTL"""
        if not self._connected:
            return False
        
        try:
            serialized = self._serialize(value)
            
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
                
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self._connected:
            return False
        
        try:
            result = await self.redis.delete(key)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self._connected:
            return 0
        
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                result = await self.redis.delete(*keys)
                return result
            return 0
            
        except Exception as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")
            return 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self._connected:
            return False
        
        try:
            result = await self.redis.exists(key)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def ttl(self, key: str) -> int:
        """Get TTL for key"""
        if not self._connected:
            return -1
        
        try:
            return await self.redis.ttl(key)
            
        except Exception as e:
            logger.error(f"Cache TTL error for key {key}: {e}")
            return -1
    
    async def setex(self, key: str, ttl: int, value: Any) -> bool:
        """Set value with expiration time (alias for set with ttl)"""
        return await self.set(key, value, ttl)
    
    async def keys(self, pattern: str) -> list:
        """Get keys matching pattern"""
        if not self._connected:
            return []
        
        try:
            return await self.redis.keys(pattern)
        except Exception as e:
            logger.error(f"Cache keys error for pattern {pattern}: {e}")
            return []
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment counter"""
        if not self._connected:
            return None
        
        try:
            return await self.redis.incrby(key, amount)
            
        except Exception as e:
            logger.error(f"Cache increment error for key {key}: {e}")
            return None

    # Context-specific cache methods
    
    async def get_company_ratios(self, ticker: str, period: str) -> Optional[Dict[str, Any]]:
        """Get cached company ratios"""
        key = f"ratios:{ticker}:{period}"
        return await self.get(key)
    
    async def set_company_ratios(
        self, 
        ticker: str, 
        period: str, 
        ratios: Dict[str, Any]
    ) -> bool:
        """Cache company ratios"""
        key = f"ratios:{ticker}:{period}"
        return await self.set(key, ratios, ttl=settings.RATIO_CACHE_TTL)
    
    async def get_sector_benchmark(
        self, 
        sector: str, 
        ratio_code: str, 
        period: str
    ) -> Optional[Dict[str, Any]]:
        """Get cached sector benchmark"""
        key = f"benchmark:{sector}:{ratio_code}:{period}"
        return await self.get(key)
    
    async def set_sector_benchmark(
        self,
        sector: str,
        ratio_code: str, 
        period: str,
        benchmark: Dict[str, Any]
    ) -> bool:
        """Cache sector benchmark"""
        key = f"benchmark:{sector}:{ratio_code}:{period}"
        return await self.set(key, benchmark, ttl=settings.BENCHMARK_CACHE_TTL)
    
    async def invalidate_sector_benchmarks(self, sector: str) -> int:
        """Invalidate all benchmarks for a sector"""
        pattern = f"benchmark:{sector}:*"
        return await self.delete_pattern(pattern)
    
    async def get_ai_context(self, ticker: str, context_type: str) -> Optional[str]:
        """Get cached AI context"""
        key = f"ai_context:{ticker}:{context_type}"
        return await self.get(key)
    
    async def set_ai_context(
        self, 
        ticker: str, 
        context_type: str, 
        context: str
    ) -> bool:
        """Cache AI context"""
        key = f"ai_context:{ticker}:{context_type}"
        return await self.set(key, context, ttl=settings.AI_CONTEXT_CACHE_TTL)


# Global cache instance
redis_client = CacheManager()