"""Модуль API-роута для healthcheck."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from {{ cookiecutter.app_name }}.application.services.health import HealthService

router = APIRouter(route_class=DishkaRoute)

@router.get("", include_in_schema=False)
async def health(service: FromDishka[HealthService]):
    """
    Эндпоинт для проверки состояния здоровья (healthcheck) приложения.

    Проверяет доступность всех критических зависимостей приложения:
    базы данных, кеша, внешних сервисов и других компонентов.
    Не включается в автоматическую документацию OpenAPI/Swagger.

    Args:
        service (HealthService): Сервис проверки здоровья.

    Returns:
        JSONResponse: Ответ с результатами проверки всех компонентов системы.
            - status_code: 200 если все компоненты здоровы, 500 при наличии ошибок
            - content: Детализированный отчет о состоянии каждого компонента
    """
    result = await service.check_all()
    return JSONResponse(
        status_code=200 if result["status"] == "ok" else 500,
        content=result
    )
