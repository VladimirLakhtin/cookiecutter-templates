"""Базовый класс модели SQLAlchemy."""
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from {{ cookiecutter.service_name }}.common.utils.case_converter import camel_case_to_snake_case
from {{ cookiecutter.service_name }}.infrastructure.config.main_config import settings


class Base(DeclarativeBase):
    """Базовый класс модели"""
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        """
        Наименование таблицы.
        Преобразует наименование класса в snake-case
        """
        return f"{camel_case_to_snake_case(cls.__name__)}"

    def __repr__(self) -> str:
        if hasattr(self, "id"):
            return f"<{self.__class__.__name__}(id='{self.id}')>"
        return super().__repr__()
