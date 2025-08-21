class ExternalServiceError(Exception):
    """Ошибка при обращении к внешнему сервису"""
    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
