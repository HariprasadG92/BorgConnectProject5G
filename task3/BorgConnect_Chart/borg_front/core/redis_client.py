import redis
import json
from django.conf import settings

def get_redis_client():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )

def get_sampled_data():
    client = get_redis_client()
    keys = client.keys()
    data = {}
    for key in keys:
        data[key] = json.loads(client.get(key))
    return data
