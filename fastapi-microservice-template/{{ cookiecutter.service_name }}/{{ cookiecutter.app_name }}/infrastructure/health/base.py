"""Модуль базового интерфейса healthchecker-а."""
from abc import ABC, abstractmethod
from typing import Tuple


class HealthChecker(ABC):
    """Базовый интерфейс healthchecker-а."""

    @abstractmethod
    async def __call__(self) -> Tuple[bool, str]:
        """Возвращает кортеж (ok, name)."""
        ...
