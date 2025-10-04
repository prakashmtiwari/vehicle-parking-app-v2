# vpa/beserver/utils/cache_manager.py
from functools import wraps
from flask import request
from vpa import cache  

def cached_response(timeout=300, key_prefix=None):
    """
    Decorator to cache API responses automatically.

    Args:
        timeout (int): Cache lifetime in seconds.
        key_prefix (str): Custom prefix for cache key (optional).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on path and parameters
            cache_key = key_prefix or f"{request.path}:{str(request.args)}"

            # Try to get cached value
            cached_data = cache.get(cache_key)
            if cached_data:
                print(f"✅ Cache hit: {cache_key}")
                return cached_data

            # Run actual function
            print(f"🚀 Cache miss: {cache_key}")
            response = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, response, timeout=timeout)
            return response
        return wrapper
    return decorator


def clear_cache(prefix=None):
    """Delete cached responses manually by key prefix."""
    if prefix:
        cache.delete(prefix)
        print(f"🧹 Cleared cache for prefix: {prefix}")
