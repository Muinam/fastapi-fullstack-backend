import redis
from redis.exceptions import RedisError

# Redis Client Instance (protocol=2 ensures maximum compatibility)
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
    protocol=2
)

def add_token_to_blacklist(jti: str, expire_seconds: int = 60 * 60 * 24 * 7) -> None:
    """Store token unique ID (jti) in Redis blacklist with expiration time."""
    redis_client.set(f"blacklist_{jti}", "true", ex=expire_seconds)

def is_token_blacklisted(jti: str) -> bool:
    """Check if token unique ID (jti) exists in Redis blacklist."""
    try:
        return bool(redis_client.exists(f"blacklist_{jti}"))
    except RedisError:
        return False
