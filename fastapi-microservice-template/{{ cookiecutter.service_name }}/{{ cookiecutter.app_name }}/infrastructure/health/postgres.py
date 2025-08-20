"""Модуль healthchecker-а БД."""
from typing import Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from .base import HealthChecker


class PostgresHealthChecker(HealthChecker):
    """Проверка подключения к Postgres."""

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def __call__(self) -> Tuple[bool, str]:
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True, "postgres"
        except Exception:
            return False, "postgres"
