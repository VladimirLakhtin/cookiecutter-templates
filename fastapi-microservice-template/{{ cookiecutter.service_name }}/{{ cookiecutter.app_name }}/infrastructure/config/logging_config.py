"""Параметры логирования и форматирования вывода логов."""
import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, computed_field

LOG_DEFAULT_FORMAT = "[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

APP_LOG_FILE_PATH = LOG_DIR / "app.log"
UVICORN_ACCESS_LOG_FILE_PATH = LOG_DIR / "uvicorn_access.log"
GRAPHQL_LOG_FILE_PATH = LOG_DIR / "graphql.log"


class LoggingConfig(BaseModel):
    """Настройки логирования с преобразованием уровня в числовое значение."""

    level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @computed_field
    @property
    def log_level_value(self) -> int:
        """Объект уровня логгирования"""
        return logging.getLevelNamesMapping()[self.level.upper()]



LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # чтобы не сбрасывать uvicorn и прочие
    "formatters": {
        "standard": {
            "format": LOG_DEFAULT_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file_app": {
            "class": "logging.FileHandler",
            "filename": str(APP_LOG_FILE_PATH),
            "formatter": "standard",
            "level": "INFO",
        },
        "file_uvicorn_access": {
            "class": "logging.FileHandler",
            "filename": str(UVICORN_ACCESS_LOG_FILE_PATH),
            "formatter": "standard",
            "level": "INFO",
        },
    },
    "loggers": {
        # корневой логгер
        "": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file_uvicorn_access"],
            "level": "INFO",
            "propagate": False,
        },
        "asyncio": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

def configure_logging(config: LoggingConfig):
    import logging.config

    level_name = config.level.upper()
    for h in LOGGING_CONFIG["handlers"].values():
        h["level"] = level_name
    for l in LOGGING_CONFIG["loggers"].values():
        l["level"] = level_name

    logging.config.dictConfig(LOGGING_CONFIG)
