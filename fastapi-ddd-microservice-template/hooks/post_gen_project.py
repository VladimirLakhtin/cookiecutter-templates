import dataclasses
import os
import shutil
import sys
import textwrap
from pathlib import Path


@dataclasses.dataclass
class Config:
    """
    Конфиг пост-хука
    """

    # Путь к папке приложения шаблона
    template_path = Path.cwd()
    app_path = Path.cwd() / "{{ cookiecutter.app_name }}"


class DependenciesCreator:
    """Класс, содержащий список используемых зависимостей в шаблонизаторе"""

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        # шаблон pyproject.toml
        self.pyproject_template = textwrap.dedent(
            """\
                [project]
                name = "{{ cookiecutter.service_name }}"
                version = "0.1.0"
                description = "{{ cookiecutter.description }}"
                requires-python = ">=3.11"
                dependencies = [
                    "fastapi>=0.114.0,<1.0.0",
                    "uvicorn>=0.30.6,<1.0.0",
                    "dishka>=1.6.0,<2.0.0",
                    "pydantic-settings>=2.5.0,<3.0.0",
                    "pydantic[email]>=2.11.7,<3.0.0",
                    "pyyaml>=6.0.2,<7.0.0",
                    {deps}
                ]

                [dependency-groups]
                dev = [
                    "pytest>=8.3.5,<9.0.0",
                    "pytest-asyncio>=0.26.0,<1.0.0",
                    "pytest-mock>=3.14.1,<4.0.0",
                ]
                
                [tool.uv]
                default-groups = ["dev"]
            """
        )

        # словарь зависимостей, где ключ - название библиотеки / фреймворка, значение - версия
        self.dependencies = {}

    def remove_dependency(self, name: str) -> None:
        """
        Удалить зависимость из словаря зависимостей
        :param name: название зависимости
        """

        if not self.dependencies.get(name):
            raise ValueError("Зависимость не была найдена в словаре зависимостей")

        del self.dependencies[name]

    def add_dependency(self, dep: dict[str, str]) -> None:
        """
        Добавить зависимость в словарь зависимостей
        :param dep: словарь с именем и версией зависимости
        """

        self.dependencies.update(dep)

    def create_pyproject(self) -> str:
        final_dependencies = []
        for dependency, version in self.dependencies.items():
            if version.startswith((">=", "~", "^", "<", "!")) or "," in version:
                # For version specs that already include operators
                final_dependencies.append(f'"{dependency}{version}"')
            else:
                # For plain version numbers
                final_dependencies.append(f'"{dependency}>={version}"')

        # Replace the {deps} placeholder with the actual dependencies
        content = self.pyproject_template.replace("{deps}", ",\n    ".join(final_dependencies))
        return content


class FileManager:
    def __init__(self):
        self.paths_to_remove: list[Path | None] = []

    def remove_files(self) -> None:
        """
        Удалить файл или директорию
        """

        for path in self.paths_to_remove:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    @staticmethod
    def rename_file(file_path: Path, new_name: str) -> None:
        """
        Переименовать файл
        :param file_path: полный путь до директории
        :param new_name: новое название файла
        """

        new_name_file_path = file_path.parent / new_name
        file_path.rename(new_name_file_path)


class LibsConfig:
    """
    Содержит поля с именем в виде названия библиотеки,
    и значением в виде словаря с путями до зависимых модулей и
    docker-compose файла, а также необходимыми зависимостями
    """

    postgres = {
        "modules": [
            Config.app_path / "infrastructure" / "config" / "db_config.py",
            Config.app_path / "infrastructure" / "database",
            Config.app_path / "infrastructure" / "health" / "postgres.py",
            Config.app_path / "utils",
        ],
        "dependencies": {
            "sqlalchemy": ">=2.0.41",
            "alembic": ">=1.13.0,<2.0.0",
            "asyncpg": ">=0.29.0,<1.0.0",
        },
    }
    redis = {
        "modules": [
            Config.app_path / "infrastructure" / "config" / "redis_config.py",
            Config.app_path / "infrastructure" / "health" / "redis.py",
        ],
        "dependencies": {
            "redis": ">=6.2.0,<7.0.0",
        },
    }
    httpx = {
        "modules": [
            Config.app_path / "infrastructure" / "http",
        ],
        "dependencies": {
            "httpx": ">=0.28.1,<1.0.0",
        },
    }
    # TODO: Дополнять в процессе добавления библиотек


uv_creator = DependenciesCreator()
file_manager = FileManager()


def create_uv_dependencies() -> None:
    """
    Создать файл зависимостей uv
    """

    file_content = uv_creator.create_pyproject()
    file_path = str(Config.template_path / "pyproject.toml")

    with open(file_path, "w") as f:
        f.write(file_content)


def resolve_libs() -> None:
    """Удалить лишние модули"""

    libs_to_add = {
        "postgres": "{{cookiecutter.add_postgresql}}" == "yes",
        "redis": "{{cookiecutter.add_redis}}" == "yes",
        "httpx": "{{cookiecutter.add_httpx}}" == "yes",
        # TODO: Дополнять в процессе добавления библиотек
    }

    modules_to_reserve = set()
    modules_to_delete = set()

    for lib, is_add in libs_to_add.items():
        if not is_add:
            for module in getattr(LibsConfig, lib)["modules"]:
                modules_to_delete.add(module)
        else:
            for module in getattr(LibsConfig, lib)["modules"]:
                modules_to_reserve.add(module)

            dependencies = getattr(LibsConfig, lib)["dependencies"]
            uv_creator.add_dependency(dependencies)

    for module in modules_to_delete - modules_to_reserve:
        file_manager.paths_to_remove.append(module)


def main() -> None:
    """Вызвать функции для выполнения логики пост-хука"""
    resolve_libs()
    create_uv_dependencies()
    file_manager.remove_files()


if __name__ == "__main__":
    sys.exit(main())