"""Параметры логирования и форматирования вывода логов."""
import logging
import logging.config
from pathlib import Path
import yaml
from pydantic import BaseModel, field_validator
from typing import Literal

CONFIG_PATH = Path(__file__).with_name("logging.yaml")


class LoggingConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @field_validator("level", mode="before")
    @classmethod
    def upper_level(cls, v: str) -> str:
        return v.upper()

def configure_logging(level: str = "INFO") -> None:
    """Настройка логирования из logging.yaml + уровень из параметров."""

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)["logging"]

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"standard": {"format": raw_config["format"]}},
        "handlers": {},
        "loggers": {},
    }

    # Хэндлеры
    for name, handler in raw_config["handlers"].items():
        handler_conf = {
            "class": handler["class"],
            "level": level,
            "formatter": "standard",
        }
        if "filename" in handler:
            Path(handler["filename"]).parent.mkdir(parents=True, exist_ok=True)
            handler_conf["filename"] = handler["filename"]

        logging_config["handlers"][name] = handler_conf

    # Логгеры
    for logger_name, logger_conf in raw_config["loggers"].items():
        logging_config["loggers"][logger_name if logger_name != "root" else ""] = {
            "handlers": logger_conf["handlers"],
            "level": level,
            "propagate": logger_conf.get("propagate", False),
        }
    logging.config.dictConfig(logging_config)
