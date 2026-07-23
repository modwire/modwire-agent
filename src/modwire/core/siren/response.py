import json
from collections.abc import Mapping
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from modwire_siren import SirenContext

_SIREN_MEDIA_TYPE = "application/vnd.siren+json"


class SirenResponseFactory:
    def __init__(self, engine: Any, resources: Mapping[str, Any]) -> None:
        self.engine = engine
        self.resources = resources

    def resource(
        self,
        request: HttpRequest,
        path_values: Mapping[str, Any],
        operation: Any,
        response: HttpResponse,
    ) -> JsonResponse:
        resource = self.resources[operation.resource]
        payload = self._payload(response)
        scope, value, items = self._representation(operation.scope, resource, payload)
        context = SirenContext(
            base_url=self.base_url(request),
            scope=scope,
            resource=resource.name,
            value=value,
            items=items,
            path_values=path_values,
            query=tuple((key, value) for key, values in request.GET.lists() for value in values),
            capabilities=frozenset((*resource.collection_operations, *resource.entity_operations)),
        )
        return self.response(self.engine.project(context), status=response.status_code)

    def command(self, request: HttpRequest, api_path: str, response: HttpResponse) -> JsonResponse:
        payload = self._payload(response)
        document: dict[str, Any] = {
            "class": ["command"],
            "links": [{"rel": ["self"], "href": request.build_absolute_uri()}],
        }
        if payload is None:
            document["properties"] = {"content_type": response.get("Content-Type", "application/octet-stream")}
            document["links"].append({"rel": ["content"], "href": f"{self.base_url(request)}{api_path}"})
        else:
            document["properties"] = payload if isinstance(payload, Mapping) else {"result": payload}
        return self.response(document, status=response.status_code)

    @staticmethod
    def _representation(
        scope: str,
        resource: Any,
        payload: Any,
    ) -> tuple[str, Mapping[str, Any], tuple[Mapping[str, Any], ...]]:
        if scope == "entity":
            return "entity", SirenResponseFactory._mapping(payload), ()
        if isinstance(payload, list):
            return "collection", {}, tuple(SirenResponseFactory._mapping(item) for item in payload)
        if resource.entity is not None and resource.identifier in SirenResponseFactory._mapping(payload):
            return "entity", SirenResponseFactory._mapping(payload), ()
        return "collection", {}, (SirenResponseFactory._mapping(payload),) if payload else ()

    @staticmethod
    def _mapping(value: Any) -> Mapping[str, Any]:
        return value if isinstance(value, Mapping) else {}

    @staticmethod
    def _payload(response: HttpResponse) -> Any | None:
        if "application/json" not in response.get("Content-Type", ""):
            return None
        return json.loads(response.content)

    @staticmethod
    def base_url(request: HttpRequest) -> str:
        return request.build_absolute_uri("/").rstrip("/")

    @staticmethod
    def response(document: dict[str, Any], status: int = 200) -> JsonResponse:
        return JsonResponse(document, status=status, content_type=_SIREN_MEDIA_TYPE)
