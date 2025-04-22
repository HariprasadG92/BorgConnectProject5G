# core/redis_client.py
import redis
from django.conf import settings

# Initialize Redis client
def get_redis_client():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True  # This ensures the data returned from Redis is decoded to UTF-8 strings
    )

redis_client = get_redis_client()
