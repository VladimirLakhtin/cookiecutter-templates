"""Модуль конфигурации сервиса"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from {{ cookiecutter.app_name }}.infrastructure.config.logging_config import LoggingConfig
{%- if cookiecutter.add_postgresql == "yes" %}
from {{ cookiecutter.app_name }}.infrastructure.config.db_config import PostgreSQLConfig
{%- endif %}
{%- if cookiecutter.add_redis == "yes" %}
from {{ cookiecutter.app_name }}.infrastructure.config.redis_config import RedisConfig
{%- endif %}
from {{ cookiecutter.app_name }}.infrastructure.config.run_config import RunConfig


class ServiceConfig(BaseSettings):
    """Конфигурация сервиса дерева документов.

    Наследует базовые настройки сервиса и добавляет специфичные для дерева документов.

    Attributes:
        log (LoggingConfig): Конфигурация логирования.
        {%- if cookiecutter.add_postgresql == "yes" %}
        db (PostgreSQLConfig): Конфигурация подключения к БД PostgreSQL.
        {%- endif %}
        {%- if cookiecutter.add_redis == "yes" %}
        redis (RedisConfig): Конфигурация подключения к Redis.
        {%- endif %}
        run (RunConfig): Конфигурация запуска приложения.
    """
    log: LoggingConfig = LoggingConfig()
    {%- if cookiecutter.add_postgresql == "yes" %}
    db: PostgreSQLConfig = PostgreSQLConfig()
    {%- endif %}
    {%- if cookiecutter.add_redis == "yes" %}
    redis: RedisConfig = RedisConfig()
    {%- endif %}
    run: RunConfig = RunConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )


# Экземпляр конфигурации сервиса
settings = ServiceConfig(
    _env_prefix="{{ cookiecutter.prefix.upper() }}__",
    _env_file=Path(__file__).parents[4] / ".env",
)
