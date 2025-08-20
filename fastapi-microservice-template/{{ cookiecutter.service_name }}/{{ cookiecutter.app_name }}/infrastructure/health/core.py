"""Модуль healthchecker-а приложения."""
from typing import Tuple

from .base import HealthChecker


class CoreHealthChecker(HealthChecker):
    """Проверка самого приложения."""

    async def __call__(self) -> Tuple[bool, str]:
        return True, "core"
