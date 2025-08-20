"""Конфигурации сервиса"""
from {{ cookiecutter.app_name }}.infrastructure.config.logging_config import configure_logging
from {{ cookiecutter.app_name }}.infrastructure.config.main_config import ServiceConfig

__all__ = (
    ServiceConfig,
    configure_logging,
)
