from {{ cookiecutter.app_name }}.infrastructure.health import HealthChecker


class HealthService:
    def __init__(self, checkers: list[HealthChecker]):
        self._checkers = checkers

    async def check_all(self) -> dict:
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
