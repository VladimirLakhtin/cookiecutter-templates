"""Проверяющие компоненты здоровья системы"""
from {{ cookiecutter.app_name }}.infrastructure.health.base import HealthChecker
from {{ cookiecutter.app_name }}.infrastructure.health.core import CoreHealthChecker
{%- if cookiecutter.add_postgresql == "yes" %}
from {{ cookiecutter.app_name }}.infrastructure.health.postgres import PostgresHealthChecker
{%- endif %}
{%- if cookiecutter.add_redis == "yes" %}
from {{ cookiecutter.app_name }}.infrastructure.health.redis import RedisHealthChecker
{%- endif %}

__all__ = (
    HealthChecker,
    CoreHealthChecker,
    {%- if cookiecutter.add_postgresql == "yes" %}
    PostgresHealthChecker,
    {%- endif %}
    {%- if cookiecutter.add_redis == "yes" %}
    RedisHealthChecker,
    {%- endif %}
)
