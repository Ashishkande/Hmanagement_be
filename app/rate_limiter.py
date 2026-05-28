from fastapi import HTTPException
from app.redis_client import redis_client


def check_rate_limit(
    key: str,
    limit: int,
    window: int
):

    current = redis_client.get(key)

    # first request
    if not current:

        redis_client.setex(
            key,
            window,
            1
        )

        return

    current = int(current)

    # limit exceeded
    if current >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )

    # increment count
    redis_client.incr(key)