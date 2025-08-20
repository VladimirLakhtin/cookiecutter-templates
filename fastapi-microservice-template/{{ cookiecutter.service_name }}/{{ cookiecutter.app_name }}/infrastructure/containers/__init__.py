"""DI-контейнеры сервиса"""
from {{ cookiecutter.app_name }}.infrastructure.containers.application import ApplicationProvider
from {{ cookiecutter.app_name }}.infrastructure.containers.infrastructure import InfrastructureProvider

__all__ = (
    ApplicationProvider,
    InfrastructureProvider,
)
