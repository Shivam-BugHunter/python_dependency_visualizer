"""
Caching utility.
"""
from core.logger import Logger
from datetime import datetime, timedelta

logger = Logger(__name__)

class Cache:
    """Simple in-memory cache."""
    
    def __init__(self):
        self._cache = {}
        self._ttl = {}
        logger.info("Cache initialized")
    
    def get(self, key: str):
        """Get value from cache."""
        if key in self._cache:
            if key in self._ttl:
                if datetime.now() < self._ttl[key]:
                    logger.debug(f"Cache hit: {key}")
                    return self._cache[key]
                else:
                    # Expired
                    del self._cache[key]
                    del self._ttl[key]
                    logger.debug(f"Cache expired: {key}")
            else:
                logger.debug(f"Cache hit: {key}")
                return self._cache[key]
        
        logger.debug(f"Cache miss: {key}")
        return None
    
    def set(self, key: str, value, ttl_seconds: int = 300):
        """Set value in cache with TTL."""
        self._cache[key] = value
        self._ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
        logger.debug(f"Cache set: {key} (TTL: {ttl_seconds}s)")
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._ttl.clear()
        logger.info("Cache cleared")

