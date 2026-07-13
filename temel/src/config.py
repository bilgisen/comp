from typing import Optional

class Settings:
    def __init__(self, env):
        self.ENVIRONMENT = env.ENVIRONMENT if hasattr(env, "ENVIRONMENT") else "development"
        self.ISYATIRIM_BASE_URL = env.ISYATIRIM_BASE_URL if hasattr(env, "ISYATIRIM_BASE_URL") else "https://www.isyatirim.com.tr"
        self.ISYATIRIM_TIMEOUT = int(env.ISYATIRIM_TIMEOUT) if hasattr(env, "ISYATIRIM_TIMEOUT") else 30
        self.ISYATIRIM_RATE_LIMIT = int(env.ISYATIRIM_RATE_LIMIT) if hasattr(env, "ISYATIRIM_RATE_LIMIT") else 20
        self.ISYATIRIM_DELAY = float(env.ISYATIRIM_DELAY) if hasattr(env, "ISYATIRIM_DELAY") else 3.0
        self.CACHE_TTL_RATIOS = int(env.CACHE_TTL_RATIOS) if hasattr(env, "CACHE_TTL_RATIOS") else 3600
        self.CACHE_TTL_COMPANY = int(env.CACHE_TTL_COMPANY) if hasattr(env, "CACHE_TTL_COMPANY") else 21600
        self.CACHE_TTL_AI_CONTEXT = int(env.CACHE_TTL_AI_CONTEXT) if hasattr(env, "CACHE_TTL_AI_CONTEXT") else 1800

settings: Optional[Settings] = None

def init_settings(env):
    global settings
    settings = Settings(env)
    return settings
