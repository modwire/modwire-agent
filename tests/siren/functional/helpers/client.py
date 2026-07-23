from collections.abc import Callable
from typing import Any

from .response import SirenResponse


class SirenClient:
    """Route existing REST test calls through the Siren facade."""

    _methods = frozenset({"delete", "get", "head", "options", "patch", "post", "put"})

    def __init__(self, client: Any) -> None:
        self._client = client

    def __getattr__(self, name: str) -> Any:
        method = getattr(self._client, name)
        if name not in self._methods:
            return method
        return self._request(method, name == "get")

    def _request(self, method: Callable[..., Any], collection_response: bool) -> Callable[..., SirenResponse]:
        def request(path: str, *args: Any, **kwargs: Any) -> SirenResponse:
            return SirenResponse(method(self._siren_path(path), *args, **kwargs), collection_response)

        return request

    @staticmethod
    def _siren_path(path: str) -> str:
        return path.replace("/api/", "/siren/", 1)
