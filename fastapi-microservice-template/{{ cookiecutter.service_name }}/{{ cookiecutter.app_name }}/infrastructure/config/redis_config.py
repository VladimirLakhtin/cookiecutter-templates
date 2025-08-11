"""Настройки Redis."""
from pydantic import BaseModel, computed_field


class RedisConfig(BaseModel):
    """Конфигурация подключения к Redis."""
    host: str = "redis"
    port: str = "6379"
    timeout: int = 30
    password: str = "super_password"

    @computed_field
    @property
    def url(self) -> str:
        """URL подключения к sdm"""
        return f"redis://:{self.password}@{self.host}:{self.port}"
