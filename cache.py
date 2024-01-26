from cashews import cache

from src.config import redis

cache.setup(f"redis://localhost:{redis.port}")
