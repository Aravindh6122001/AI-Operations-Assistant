import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=50,
    socket_connect_timeout=2,
    socket_timeout=2,
    health_check_interval=30,
)
