"""Конфигурации подключения к базам данных проекта."""
from pydantic import BaseModel, computed_field


class PostgreSQLConfig(BaseModel):
    """Конфигурация PostgreSQL с соглашениями об именовании и DSN."""

    host: str = "0.0.0.0"
    port: int = 5432
    database: str = "database_name"
    user: str = "super_user"
    password: str = "super_secret_password"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    @computed_field
    @property
    def dsn(self) -> str:
        """URL подключения к sdm"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
