import json
import re
from collections.abc import Mapping
from functools import cached_property
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import Resolver404, resolve
from modwire_siren import SirenContext, siren

from .api import api

_PATH_PARAMETER = re.compile(r"\{[^}]+\}")
_SIREN_MEDIA_TYPE = "application/vnd.siren+json"


class SirenFacade:
    @cached_property
    def schema(self) -> Mapping[str, Any]:
        return api.get_openapi_schema()

    @cached_property
    def engine(self) -> Any:
        schema = json.loads(json.dumps(self.schema))
        schema["paths"] = {
            f"/siren{path.removeprefix('/api')}": path_item for path, path_item in schema["paths"].items()
        }
        return siren(schema, root_path="/siren/")

    @cached_property
    def resources(self) -> dict[str, Any]:
        return {resource.reference: resource for resource in self.engine.api.resources}

    def root(self, request: HttpRequest) -> JsonResponse:
        capabilities = frozenset(
            operation.name
            for operation in self.engine.api.operations
            if operation.resource is None and "{" not in operation.route.path
        )
        document = self.engine.project(
            SirenContext(base_url=self.base_url(request), scope="root", capabilities=capabilities)
        )
        payload = document.model_dump(by_alias=True, mode="json", exclude_none=True)
        payload["properties"] = self.schema["info"]
        return self.response(payload, status=200)

    def dispatch(self, request: HttpRequest, path: str) -> HttpResponse:
        api_path = f"/api/{path}"
        try:
            match = resolve(api_path)
        except Resolver404:
            return HttpResponse(status=404)

        response = match.func(request, *match.args, **match.kwargs)
        if response.status_code >= 400:
            return self.error(request, response)

        operation = self.operation(request.method, request.path)
        if operation is None or operation.resource is None:
            return self.command(request, api_path, response)
        return self.resource(request, match.kwargs, operation, response)

    def resource(
        self,
        request: HttpRequest,
        path_values: Mapping[str, Any],
        operation: Any,
        response: HttpResponse,
    ) -> JsonResponse:
        resource = self.resources[operation.resource]
        payload = self.payload(response)
        scope, value, items = self.representation(operation.scope.value, resource, payload)
        document = self.engine.project(
            SirenContext(
                base_url=self.base_url(request),
                scope=scope,
                resource=resource.name,
                value=value,
                items=items,
                path_values=path_values,
                query=tuple((key, value) for key, values in request.GET.lists() for value in values),
                capabilities=frozenset((*resource.collection_operations, *resource.entity_operations)),
            )
        )
        return self.response(document.model_dump(by_alias=True, mode="json", exclude_none=True), response.status_code)

    def command(self, request: HttpRequest, api_path: str, response: HttpResponse) -> JsonResponse:
        payload = self.payload(response)
        document: dict[str, Any] = {
            "class": ["command"],
            "links": [{"rel": ["self"], "href": request.build_absolute_uri()}],
        }
        if payload is None:
            document["properties"] = {"content_type": response.get("Content-Type", "application/octet-stream")}
            document["links"].append({"rel": ["content"], "href": f"{self.base_url(request)}{api_path}"})
        else:
            document["properties"] = payload if isinstance(payload, Mapping) else {"result": payload}
        return self.response(document, response.status_code)

    def error(self, request: HttpRequest, response: HttpResponse) -> JsonResponse:
        payload = self.payload(response)
        properties = payload if isinstance(payload, Mapping) else {"result": payload} if payload is not None else {}
        return self.response(
            {
                "class": ["error"],
                "properties": properties,
                "links": [{"rel": ["self"], "href": request.build_absolute_uri()}],
            },
            response.status_code,
        )

    def operation(self, method: str, path: str) -> Any | None:
        return next(
            (
                operation
                for operation in self.engine.api.operations
                if operation.method.value == method and re.fullmatch(self.route_pattern(operation.route.path), path)
            ),
            None,
        )

    @staticmethod
    def representation(
        scope: str, resource: Any, payload: Any
    ) -> tuple[str, Mapping[str, Any], tuple[Mapping[str, Any], ...]]:
        if scope == "entity":
            return "entity", SirenFacade.mapping(payload), ()
        if isinstance(payload, list):
            return "collection", {}, tuple(SirenFacade.mapping(item) for item in payload)
        if resource.entity is not None and resource.identifier in SirenFacade.mapping(payload):
            return "entity", SirenFacade.mapping(payload), ()
        return "collection", {}, (SirenFacade.mapping(payload),) if payload else ()

    @staticmethod
    def route_pattern(path: str) -> str:
        parts = _PATH_PARAMETER.split(path)
        return "".join(f"{re.escape(part)}[^/]+" for part in parts[:-1]) + re.escape(parts[-1])

    @staticmethod
    def mapping(value: Any) -> Mapping[str, Any]:
        return value if isinstance(value, Mapping) else {}

    @staticmethod
    def payload(response: HttpResponse) -> Any | None:
        if not response.content or "application/json" not in response.get("Content-Type", ""):
            return None
        return json.loads(response.content)

    @staticmethod
    def base_url(request: HttpRequest) -> str:
        return request.build_absolute_uri("/").rstrip("/")

    @staticmethod
    def response(document: Mapping[str, Any], status: int) -> JsonResponse:
        return JsonResponse(document, status=status, content_type=_SIREN_MEDIA_TYPE)


facade = SirenFacade()
