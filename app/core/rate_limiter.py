import time

import redis
from fastapi import HTTPException, Request

from app.db.redis import redis_client

RATE_LIMIT = 10
WINDOW_SECONDS = 60

INCREMENT_SCRIPT = """
local count = redis.call('INCR', KEYS[1])

if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

return count
"""


def rate_limit(request: Request) -> None:
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    current_time = int(time.time())
    window_id = current_time // WINDOW_SECONDS

    key = f"rate-limit:{client_ip}:{window_id}"

    try:
        count = redis_client.eval(
            INCREMENT_SCRIPT,
            1,
            key,
            WINDOW_SECONDS * 2,
        )
    except redis.RedisError as exc:
        raise HTTPException(
            status_code=503,
            detail="Rate limiter temporarily unavailable",
        ) from exc

    if count > RATE_LIMIT:
        retry_after = WINDOW_SECONDS - (
            current_time % WINDOW_SECONDS
        )

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
            headers={"Retry-After": str(retry_after)},
        )