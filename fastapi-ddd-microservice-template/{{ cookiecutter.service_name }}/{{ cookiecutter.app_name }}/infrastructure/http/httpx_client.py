"""Базовый сервис для взаимодействия с внешними API"""
import logging
from typing import Any

import httpx

from {{ cookiecutter.app_name }}.infrastructure.http.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class HttpxClient:
    """
    Реализация HTTP-клиента на основе httpx.

    Обеспечивает отправку HTTP-запросов, обработку статуса ответов,
    логирование и проброс ошибок в виде HTTPException.

    Attributes:
        base_url (str): Базовый URL внешнего API.
        timeout (int): Таймаут запросов в секундах.
    """

    def __init__(self, base_url: str, timeout: int = 15.0):
        """
        Инициализирует базовый внешний сервис.

        Args:
            base_url (str): Базовый URL внешнего API.
            timeout (int): Таймаут HTTP-запросов (по умолчанию 15 секунд).
        """
        self.base_url = base_url
        self.timeout = timeout
        logger.info(f"{self.__class__.__name__} initialized with base URL: {base_url}")


    async def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        response = await self._request("GET", endpoint, params=params)
        return response.json()

    async def post(self, endpoint: str, data: dict[str, Any] | None = None) -> Any:
        response = await self._request("POST", endpoint, json=data)
        return response.json()

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        headers: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        content: bytes | None = None,
        files: dict | None = None,
        expected_status: int = 200,
    ) -> httpx.Response:
        """
        Выполняет HTTP-запрос к внешнему API и обрабатывает результат.

        Args:
            method (str): HTTP-метод (GET, POST, PUT, DELETE и т.д.).
            endpoint (str): Относительный путь эндпоинта (без base_url).
            headers (dict, optional): Заголовки запроса.
            json (dict, optional): JSON-данные для отправки в теле запроса.
            params (dict, optional): Query-параметры запроса.
            content (bytes, optional): Сырые данные в теле запроса.
            files (dict, optional): Файлы для multipart/form-data.
            expected_status (int, optional): Ожидаемый статус-код успешного ответа (по умолчанию 200).

        Returns:
            httpx.Response: Ответ от внешнего сервиса.

        Raises:
            HTTPException: Если внешний сервис вернул неожиданный статус или недоступен.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json,
                    params=params,
                    content=content,
                    files=files,
                    timeout=self.timeout,
                )
                logger.info(f"{method.upper()} {url} | Status: {response.status_code}")

                if response.status_code != expected_status:
                    logger.warning(f"Unexpected status: {response.status_code}, body: {response.text}")
                    raise ExternalServiceError(
                        f"{method} {url} failed: {response.text}",
                        status_code=response.status_code,
                    )
        except httpx.RequestError as e:
            logger.error(f"{method.upper()} {url} failed: {e}")
            raise ExternalServiceError(f"{method} {url} connection failed: {e}")
        else:
            return response
