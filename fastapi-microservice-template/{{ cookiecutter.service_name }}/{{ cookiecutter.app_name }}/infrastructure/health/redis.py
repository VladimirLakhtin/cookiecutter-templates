"""Модуль healthchecker-а Redis."""
from typing import Tuple

import redis.asyncio as aioredis

from .base import HealthChecker


class RedisHealthChecker(HealthChecker):
    """Проверка доступности Redis."""

    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def __call__(self) -> Tuple[bool, str]:
        try:
            pong = await self.redis.ping()
            return pong, "redis"
        except Exception:
            return False, "redis"
