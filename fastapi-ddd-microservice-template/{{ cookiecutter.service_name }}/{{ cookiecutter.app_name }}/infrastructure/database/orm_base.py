"""Базовый класс модели SQLAlchemy."""
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from {{ cookiecutter.app_name }}.utils import camel_case_to_snake_case


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class OrmBase(DeclarativeBase):
    """Базовый класс orm-модели"""
    __abstract__ = True

    metadata = MetaData(
        naming_convention=NAMING_CONVENTION,
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
