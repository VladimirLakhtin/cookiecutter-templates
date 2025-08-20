"""Модуль содержит конфигурацию dependency injection для Infrastructure-слоя приложения"""
from dishka import Provider, provide, Scope
{%- if cookiecutter.add_redis == "yes" %}
import redis.asyncio as aioredis
{%- endif %}
{%- if cookiecutter.add_postgresql == "yes" %}
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
{%- endif %}

from {{ cookiecutter.app_name }}.infrastructure.config import ServiceConfig
from {{ cookiecutter.app_name }}.infrastructure import health as health_checkers


class InfrastructureProvider(Provider):
    """
    Провайдер зависимостей слоя Infrastructure.

    Регистрирует технические реализации портов (адаптеры) инфраструктурного слоя.
    Управляет созданием и конфигурацией внешних подключений и сервисов.

    Provides:
        list[HealthChecker]: Список проверяющих компонентов здоровья системы
        {%- if cookiecutter.add_redis == "yes" %}
        aioredis.Redis: Клиент Redis для кеширования и хранения токенов
        {%- endif %}
    """
    {%- if cookiecutter.add_postgresql == "yes" %}

    @provide(scope=Scope.APP)
    def provide_engine(self, settings: ServiceConfig) -> AsyncEngine:
        """Создание engine для SQLAlchemy"""
        return create_async_engine(
            url=settings.db.dsn,
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    def provide_session(self, engine: AsyncEngine) -> AsyncSession:
        """Фабрика сессий"""
        return async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )()
    {%- endif %}
    {%- if cookiecutter.add_redis == "yes" %}

    @provide(scope=Scope.APP)
    def provide_redis_service(self, settings: ServiceConfig) -> aioredis.Redis:
        """Redis-клиент"""
        return aioredis.from_url(settings.redis.url)
    {%- endif %}

    @provide(scope=Scope.APP)
    def get_health_checkers(
        self,
        {%- if cookiecutter.add_redis == "yes" %}
        redis: aioredis.Redis,
        {%- endif %}
        {%- if cookiecutter.add_postgresql == "yes" %}
        engine: AsyncEngine,
        {%- endif %}
    ) -> list[health_checkers.HealthChecker]:
        """Список проверяющих компонентов здоровья системы"""
        return [
            health_checkers.CoreHealthChecker(),
            {%- if cookiecutter.add_redis == "yes" %}
            health_checkers.RedisHealthChecker(redis),
            {%- endif %}
            {%- if cookiecutter.add_postgresql == "yes" %}
            health_checkers.PostgresHealthChecker(engine),
            {%- endif %}
        ]
