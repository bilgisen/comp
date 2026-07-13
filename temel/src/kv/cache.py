import json
from typing import Optional, Any

class KVCache:
    def __init__(self, kv):
        self.kv = kv

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self.kv.get(key)
            if value is not None:
                return json.loads(value)
            return None
        except Exception:
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        try:
            await self.kv.put(key, json.dumps(value), expiration_ttl=ttl)
        except Exception:
            pass

    async def delete(self, key: str):
        try:
            await self.kv.delete(key)
        except Exception:
            pass

    async def delete_by_prefix(self, prefix: str):
        try:
            keys = await self.kv.list(prefix=prefix)
            for key in keys.get("keys", []):
                await self.kv.delete(key["name"])
        except Exception:
            pass

    async def get_or_set(self, key: str, fetch_fn, ttl: int = 3600) -> Any:
        cached = await self.get(key)
        if cached is not None:
            return cached
        value = await fetch_fn()
        if value is not None:
            await self.set(key, value, ttl)
        return value
