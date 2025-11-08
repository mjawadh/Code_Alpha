"""
cache package initializer.

Provides a sane import surface for cache operations.
"""
from . import db_handler

# Prefer the class-based handler if present, otherwise expose module-level functions
try:
    CacheDBHandler = db_handler.CacheDBHandler
except AttributeError:
    # fallback to function-style handlers if the other variant is present
    CacheDBHandler = None

# Expose commonly used functions (if they exist)
fetch_cached_translation = getattr(db_handler, "fetch_cached_translation", None)
store_translation = getattr(db_handler, "store_translation", None)
cleanup_cache = getattr(db_handler, "cleanup_cache", None)

__all__ = [
    "CacheDBHandler",
    "fetch_cached_translation",
    "store_translation",
    "cleanup_cache",
]
