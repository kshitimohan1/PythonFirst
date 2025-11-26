import redis
import json
from fastapi.encoders import jsonable_encoder

redis_client = redis.Redis(
    host="127.0.0.1",
    port=6382,
    password="kshiti@123",
    decode_responses=True
)

print(redis_client.ping())

# store cache
def set_cache(key, value, expiry_seconds=60):
    safe_value = jsonable_encoder(value)
    redis_client.set(key, json.dumps(safe_value), ex=expiry_seconds)

# retrieve cache
def get_cache(key):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

# delete cache
def delete_cache(key):
    redis_client.delete(key)
