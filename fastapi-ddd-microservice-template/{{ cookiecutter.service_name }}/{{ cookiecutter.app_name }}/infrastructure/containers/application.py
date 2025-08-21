"""Модуль содержит конфигурацию dependency injection для Application-слоя приложения"""
from dishka import Provider, provide, Scope

from {{ cookiecutter.app_name }}.application.services.health import HealthService


class ApplicationProvider(Provider):
    """
    Провайдер зависимостей слоя Application.

    Регистрирует сервисы уровня приложения (Application Services)
    с областью видимости APP - singleton на все время жизни приложения.

    Provides:
        HealthService: Сервис проверки здоровья системы
    """

    hs = provide(HealthService, scope=Scope.APP)
