from collections.abc import Mapping
from types import TracebackType
from typing import Any, Self

import httpx
from modwire_siren import SirenClientError, SirenResponse


class HttpxSirenTransport:
    def __init__(
        self,
        api_key: str,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self._client = httpx.AsyncClient(
            headers={
                "Accept": "application/vnd.siren+json",
                "apikey": api_key,
            },
            timeout=10,
            follow_redirects=False,
            transport=transport,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        href: str,
        payload: Mapping[str, Any] | None = None,
    ) -> SirenResponse:
        try:
            response = await self._client.request(method, href, json=payload)
        except httpx.HTTPError as error:
            raise SirenClientError(
                "transport-failure",
                str(error),
                method=method,
                href=href,
            ) from error

        if response.status_code == 204:
            return SirenResponse(
                status_code=response.status_code,
                document={
                    "class": ["result"],
                    "properties": {"status": response.status_code},
                    "links": [],
                    "actions": [],
                },
            )

        try:
            document = response.json()
        except ValueError as error:
            raise SirenClientError(
                "invalid-transport-response",
                "The Siren API response is not JSON.",
                status=response.status_code,
                method=method,
                href=href,
            ) from error
        if not isinstance(document, dict):
            raise SirenClientError(
                "invalid-transport-response",
                "The Siren API response is not an object.",
                status=response.status_code,
                method=method,
                href=href,
            )
        return SirenResponse(status_code=response.status_code, document=document)
