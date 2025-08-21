"""Приложение сервиса"""
from pathlib import Path

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from {{ cookiecutter.app_name }}.api.v1 import health_router
from {{ cookiecutter.app_name }}.infrastructure.config import ServiceConfig, configure_logging
from {{ cookiecutter.app_name }}.infrastructure.containers import InfrastructureProvider, ApplicationProvider

def create_app() -> FastAPI:
    settings = ServiceConfig(
        _env_prefix="{{ cookiecutter.prefix.upper() }}__",
        _env_file=Path(__file__).parents[1] / ".env",
    )

    configure_logging(settings.log.level)

    app = FastAPI(title="{{ cookiecutter.description }}")
    app.include_router(health_router, prefix="/health")

    container = make_async_container(
        InfrastructureProvider(),
        ApplicationProvider(),
        context={ServiceConfig: settings},
    )

    setup_dishka(container, app)

    return app

app = create_app()
