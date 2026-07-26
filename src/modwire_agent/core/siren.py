import json
import re
from collections.abc import Mapping
from functools import cached_property
from typing import Any
from urllib.parse import unquote, urlparse

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

    @cached_property
    def action_field_types(self) -> dict[str, dict[str, str]]:
        action_field_types: dict[str, dict[str, str]] = {}
        for path_item in self.schema["paths"].values():
            if not isinstance(path_item, Mapping):
                continue
            for operation in path_item.values():
                if not isinstance(operation, Mapping) or not isinstance(operation.get("operationId"), str):
                    continue
                request_body = operation.get("requestBody")
                if not isinstance(request_body, Mapping):
                    continue
                content = request_body.get("content")
                if not isinstance(content, Mapping) or not isinstance(content.get("application/json"), Mapping):
                    continue
                body_schema = self.resolve_schema(content["application/json"].get("schema"))
                properties = body_schema.get("properties")
                if not isinstance(properties, Mapping):
                    continue
                fields = {
                    name: self.field_type(property_schema)
                    for name, property_schema in properties.items()
                    if isinstance(name, str) and self.field_type(property_schema) is not None
                }
                if fields:
                    action_field_types[operation["operationId"]] = fields
        return action_field_types

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

    def response(self, document: Mapping[str, Any], status: int) -> JsonResponse:
        payload = dict(document)
        self.add_field_types(payload)
        SirenFacade.add_titles(payload)
        return JsonResponse(payload, status=status, content_type=_SIREN_MEDIA_TYPE)

    def add_field_types(self, document: dict[str, Any]) -> None:
        for entity in document.get("entities", []):
            if isinstance(entity, dict):
                self.add_field_types(entity)

        for action in document.get("actions", []):
            if not isinstance(action, dict) or not isinstance(action.get("name"), str):
                continue
            field_types = self.action_field_types.get(action["name"])
            if not field_types:
                continue
            fields = action.setdefault("fields", [])
            if not isinstance(fields, list):
                continue
            present = {
                field.get("name"): field
                for field in fields
                if isinstance(field, dict) and isinstance(field.get("name"), str)
            }
            for name, field_type in field_types.items():
                if name not in present:
                    fields.append({"name": name, "type": field_type, "title": self.humanize(name)})
                    continue
                field = present[name]
                if isinstance(field, dict) and field.get("name") in field_types:
                    field["type"] = field_type

    def resolve_schema(self, schema: Any) -> Mapping[str, Any]:
        while isinstance(schema, Mapping) and isinstance(schema.get("$ref"), str):
            reference = schema["$ref"]
            if not reference.startswith("#/components/"):
                return {}
            target: Any = self.schema
            for part in reference.removeprefix("#/").split("/"):
                if not isinstance(target, Mapping):
                    return {}
                target = target.get(part)
            schema = target
        return schema if isinstance(schema, Mapping) else {}

    def field_type(self, schema: Any) -> str | None:
        field_schema = self.resolve_schema(schema)
        if field_schema.get("type") == "object":
            return "object"
        if field_schema.get("type") != "array":
            return None
        item_schema = self.resolve_schema(field_schema.get("items"))
        return "list" if item_schema.get("type") in {"boolean", "integer", "number", "string"} else "object"

    @classmethod
    def add_titles(cls, document: dict[str, Any]) -> None:
        if not isinstance(document.get("title"), str) or not document["title"].strip():
            document["title"] = cls.document_title(document)

        for entity in document.get("entities", []):
            if isinstance(entity, dict):
                cls.add_titles(entity)

        for link in document.get("links", []):
            if isinstance(link, dict):
                if not isinstance(link.get("title"), str) or not link["title"].strip():
                    link["title"] = document["title"] if "self" in link.get("rel", []) else cls.link_title(link)

        for action in document.get("actions", []):
            if isinstance(action, dict):
                if not isinstance(action.get("title"), str) or not action["title"].strip():
                    action["title"] = cls.humanize(str(action.get("name", "action")))

    @classmethod
    def document_title(cls, document: Mapping[str, Any]) -> str:
        properties = document.get("properties")
        if isinstance(properties, Mapping):
            for key in ("title", "name", "label"):
                value = properties.get(key)
                if isinstance(value, str) and value.strip():
                    return value

        classes = document.get("class")
        if isinstance(classes, list):
            nouns = [value for value in classes if isinstance(value, str) and value not in {"collection", "entity"}]
            if nouns:
                noun = cls.humanize(nouns[-1])
                return cls.pluralize(noun) if "collection" in classes else noun

        return "Resource"

    @staticmethod
    def link_title(link: Mapping[str, Any]) -> str:
        href = link.get("href")
        if isinstance(href, str):
            path = unquote(urlparse(href).path).rstrip("/")
            if path:
                return SirenFacade.humanize(path.rsplit("/", maxsplit=1)[-1])
        return "Resource"

    @staticmethod
    def humanize(value: str) -> str:
        words = re.sub(r"[_-]+", " ", value).strip()
        return words.replace("/", " ").title() if words else "Resource"

    @staticmethod
    def pluralize(value: str) -> str:
        if value.endswith("y") and len(value) > 1 and value[-2].lower() not in "aeiou":
            return f"{value[:-1]}ies"
        return value if value.endswith("s") else f"{value}s"


facade = SirenFacade()
