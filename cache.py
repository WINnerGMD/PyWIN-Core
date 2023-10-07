from cashews import cache

from config import redis

cache.setup(f"redis://127.0.0.1:{redis.port}")


