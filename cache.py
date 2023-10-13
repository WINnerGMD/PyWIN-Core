from cashews import cache

from config import redis

cache.setup(f"redis://redis:{redis.port}")


