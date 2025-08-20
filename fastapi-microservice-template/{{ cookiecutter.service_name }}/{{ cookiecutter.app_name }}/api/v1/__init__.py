"""API сервиса V1"""
from {{ cookiecutter.app_name }}.api.v1.healthcheck import router as health_router

__all__ = (
    health_router,
)
