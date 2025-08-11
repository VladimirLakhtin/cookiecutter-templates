from pydantic import BaseModel, computed_field


class RunConfig(BaseModel):
    """
    Конфигурация запуска сервиса

    Attributes:
        host (str): Хост сервиса.
        port (int): Порт сервиса. По умолчанию 8000.
    """
    host: str = "0.0.0.0"
    port: int = 8000
