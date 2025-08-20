"""Конфигурация запуска приложения"""
from pydantic import BaseModel


class RunConfig(BaseModel):
    """
    Конфигурация запуска приложения

    Attributes:
        host (str): Хост приложения.
        port (int): Порт приложения. По умолчанию 8000.
    """
    host: str = "0.0.0.0"
    port: int = 8000
