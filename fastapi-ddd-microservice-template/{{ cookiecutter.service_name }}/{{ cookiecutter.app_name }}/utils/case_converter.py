"""Модуль утилиты для преобразования формата строк."""
import re


def camel_case_to_snake_case(name: str) -> str:
    """
    Преобразует строку из camelCase в snake_case.

    Args:
        name: Строка в camelCase формате (напр. 'CamelCaseString')

    Returns:
        str: Строка в snake_case формате (напр. 'camel_case_string')

    Examples:
        >>> camel_case_to_snake_case('CamelCaseString')
        'camel_case_string'
        >>> camel_case_to_snake_case('HTTPResponse')
        'http_response'
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    return name
