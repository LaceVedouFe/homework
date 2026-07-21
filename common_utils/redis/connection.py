import redis

_redis_connection = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True,
)


def redis_connection() -> redis.Redis:
    return _redis_connection
