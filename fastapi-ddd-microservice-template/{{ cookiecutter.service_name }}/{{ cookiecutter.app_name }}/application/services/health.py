"""
Сервис проверки работоспособности (healthcheck) микросервиса.

Реализует use case проверки здоровья системы.
Координирует выполнение проверок различных компонентов инфраструктуры
и агрегирует результаты в единый отчет о состоянии системы.
"""
from {{ cookiecutter.app_name }}.infrastructure.health import HealthChecker


class HealthService:
    """
    Сервис для комплексной проверки работоспособности всех компонентов системы.

    Оркестрирует выполнение проверок через набор HealthChecker'ов,
    агрегирует результаты и формирует общий статус здоровья приложения.
    Используется эндпоинтом /health для мониторинга и оркестрации контейнеров.

    Attributes:
        _checkers: Список проверяющих компонентов, реализующих контракт HealthChecker
    """

    def __init__(self, checkers: list[HealthChecker]):
        self._checkers = checkers

    async def check_all(self) -> dict:
        """
        Выполняет комплексную проверку всех компонентов системы.

        Returns:
            dict: Детализированный отчет о состоянии системы со структурой:
                {
                    "status": "ok" | "fail",  # Общий статус здоровья
                    "checks": {               # Результаты проверок компонентов
                        "component_name": "ok" | "fail" | "error: details",
                        ...
                    }
                }

        Notes:
            - Если хотя бы одна проверка вернула fail или выбросила исключение - общий статус "fail"
            - Если проверки не настроены - возвращает базовый статус "core": "ok"
            - Исключения в проверках перехватываются и записываются как "error: message"
        """
        results = {}
        all_ok = True

        if self._checkers:
            for checker in self._checkers:
                try:
                    ok, name = await checker()
                    results[name] = "ok" if ok else "fail"
                    if not ok:
                        all_ok = False
                except Exception as e:
                    results[name] = f"error: {str(e)}"
                    all_ok = False
        else:
            results["core"] = "ok"

        return {
            "status": "ok" if all_ok else "fail",
            "checks": results
        }
