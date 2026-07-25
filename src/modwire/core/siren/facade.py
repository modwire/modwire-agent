import json
import re
from collections.abc import Mapping
from functools import cached_property
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import Resolver404, resolve
from modwire_siren import SirenContext, siren

from ..api import api
from .response import SirenResponseFactory

_PATH_PARAMETER = re.compile(r"\{[^}]+\}")


class SirenFacade:
    """Expose every REST operation through a Siren representation.

    Resource operations are projected by ``modwire-siren`` from the API's OpenAPI
    contract. Standalone OpenAPI commands have no Siren resource graph, so they
    receive a small command representation while retaining their result as
    properties (or a link for binary output).
    """

    @cached_property
    def schema(self) -> Mapping[str, Any]:
        return api.get_openapi_schema()

    @cached_property
    def operation_ids(self) -> frozenset[str]:
        return frozenset(self._operation_ids(self.schema))

    @cached_property
    def engine(self) -> Any:
        return siren(self._siren_schema(self.schema), root_path="/siren/")

    @cached_property
    def _resources(self) -> dict[str, Any]:
        return {resource.reference: resource for resource in self.engine._api.resources}

    def root(self, request: HttpRequest) -> JsonResponse:
        document = self.engine.project(
            SirenContext(
                base_url=SirenResponseFactory.base_url(request),
                scope="root",
                capabilities=self.operation_ids,
            )
        )
        document["properties"] = self.schema["info"]
        return SirenResponseFactory.response(document, 200)

    def dispatch(self, request: HttpRequest, path: str) -> HttpResponse:
        api_path = f"/api/{path}"
        try:
            match = resolve(api_path)
        except Resolver404:
            return HttpResponse(status=404)

        response = match.func(request, *match.args, **match.kwargs)
        if response.status_code >= 400:
            return SirenResponseFactory(self.engine, self._resources).error(request, response)

        operation = self._operation(request.method, request.path)
        if operation is None or operation.resource is None:
            return SirenResponseFactory(self.engine, self._resources).command(request, api_path, response)
        return SirenResponseFactory(self.engine, self._resources).resource(request, match.kwargs, operation, response)

    @staticmethod
    def _operation_ids(schema: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(
            operation["operationId"]
            for path_item in schema["paths"].values()
            for operation in path_item.values()
            if isinstance(operation, Mapping) and "operationId" in operation
        )

    @staticmethod
    def _siren_schema(schema: Mapping[str, Any]) -> dict[str, Any]:
        document = json.loads(json.dumps(schema))
        document["paths"] = {
            f"/siren{path.removeprefix('/api')}": path_item for path, path_item in document["paths"].items()
        }
        return document

    def _operation(self, method: str, path: str) -> Any | None:
        return next(
            (
                operation
                for operation in self.engine._api.operations
                if operation.method == method and re.fullmatch(self._route_pattern(operation.route.path), path)
            ),
            None,
        )

    @staticmethod
    def _route_pattern(path: str) -> str:
        parts = _PATH_PARAMETER.split(path)
        return "".join(f"{re.escape(part)}[^/]+" for part in parts[:-1]) + re.escape(parts[-1])


facade = SirenFacade()
