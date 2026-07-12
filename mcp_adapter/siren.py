import json
from types import TracebackType
from typing import Any, Self
from urllib.parse import urlsplit

import httpx


class AdapterError(RuntimeError):
    def __init__(self, payload: dict[str, Any]):
        self.payload = payload
        super().__init__(json.dumps(payload, sort_keys=True))


class SirenNavigator:
    def __init__(
        self,
        root_url: str,
        api_key: str,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.root_url = root_url
        self._origin = self._url_origin(root_url)
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

    async def root(self) -> dict[str, Any]:
        return await self.get(self.root_url)

    async def get(self, href: str) -> dict[str, Any]:
        return await self._request("GET", href)

    async def follow(self, document: dict[str, Any], relation: str) -> dict[str, Any]:
        link = self._find(document.get("links", []), "rel", relation)
        return await self.get(self._href(link, f"link relation '{relation}'"))

    async def execute(
        self,
        document: dict[str, Any],
        action_name: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        action = self._find(document.get("actions", []), "name", action_name)
        method = action.get("method")
        if not isinstance(method, str):
            raise self._contract_error(f"Siren action '{action_name}' has no method")
        href = self._href(action, f"Siren action '{action_name}'")
        return await self._request(method.upper(), href, payload)

    def require_action(self, document: dict[str, Any], action_name: str) -> None:
        action = self._find(document.get("actions", []), "name", action_name)
        self._href(action, f"Siren action '{action_name}'")

    async def _request(
        self,
        method: str,
        href: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._validate_href(href)
        try:
            response = await self._client.request(method, href, json=payload)
        except httpx.HTTPError as error:
            raise AdapterError(
                {
                    "kind": "api-unreachable",
                    "detail": str(error),
                    "method": method,
                    "href": href,
                }
            ) from error

        try:
            body = response.json()
        except ValueError as error:
            raise AdapterError(
                {
                    "kind": "invalid-api-response",
                    "detail": "The scaffolding API response is not JSON.",
                    "status": response.status_code,
                    "method": method,
                    "href": href,
                }
            ) from error
        if not isinstance(body, dict):
            raise AdapterError(
                {
                    "kind": "invalid-api-response",
                    "detail": "The scaffolding API response is not an object.",
                    "status": response.status_code,
                    "method": method,
                    "href": href,
                }
            )
        if response.is_error:
            raise AdapterError(
                {
                    "kind": "api-problem",
                    "status": response.status_code,
                    "title": body.get("title", response.reason_phrase),
                    "detail": body.get("detail"),
                    "body": body,
                }
            )
        return body

    @staticmethod
    def _find(items: Any, field: str, expected: str) -> dict[str, Any]:
        if not isinstance(items, list):
            raise SirenNavigator._contract_error(f"Siren '{field}' collection is not a list")
        for item in items:
            if not isinstance(item, dict):
                continue
            value = item.get(field)
            if value == expected or isinstance(value, list) and expected in value:
                return item
        raise SirenNavigator._contract_error(f"Siren {field} '{expected}' is not advertised")

    @staticmethod
    def _href(item: dict[str, Any], context: str) -> str:
        href = item.get("href")
        if not isinstance(href, str):
            raise SirenNavigator._contract_error(f"{context} has no href")
        return href

    def _validate_href(self, href: str) -> None:
        if self._url_origin(href) != self._origin:
            raise self._contract_error("Siren target leaves the configured API origin")

    @staticmethod
    def _url_origin(url: str) -> tuple[str, str, int | None]:
        parsed = urlsplit(url)
        return parsed.scheme, parsed.hostname or "", parsed.port

    @staticmethod
    def _contract_error(detail: str) -> AdapterError:
        return AdapterError({"kind": "invalid-siren-contract", "detail": detail})
