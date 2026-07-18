import json
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Literal

from django.conf import settings
from django.http import HttpResponse
from modwire_siren import (
    CustomPagination,
    ModwireSirenFactory,
    NinjaExtraSirenResponseAdapter,
    OffsetPagination,
    PaginationLinkInput,
    SirenCollectionRequest,
)
from modwire_siren.integrations.django import to_django_response
from modwire_siren.openapi.error import OpenApiError
from modwire_siren.standards import SirenMediaType

SIREN_TYPE = str(SirenMediaType.ENTITY)
PROBLEM_TYPE = str(SirenMediaType.PROBLEM)
SIREN_RESOURCE_EXTENSION = "x-siren-resource"
HTTP_METHODS = ("get", "post", "put", "patch", "delete")


@dataclass(frozen=True, slots=True)
class _ProjectionConfig:
    path: str
    methods: tuple[str, ...]
    kind: Literal["collection", "entity"]
    resource_name: str
    operation_ids: tuple[str, ...]
    path_parameters: dict[str, str]
    item_operation_ids: tuple[str, ...] = ()


def _base_url(request) -> str:
    return request.build_absolute_uri("/")


@lru_cache(maxsize=1)
def _openapi_schema() -> dict[str, Any]:
    from modwire.core.api import api

    return api.get_openapi_schema()


@lru_cache(maxsize=1)
def _siren_factory():
    return ModwireSirenFactory.web(_openapi_schema(), base_url_resolver=_base_url)


def _adapter(request) -> NinjaExtraSirenResponseAdapter:
    return NinjaExtraSirenResponseAdapter.for_request(siren_factory=_siren_factory(), request=request)


def api_root_document(request) -> dict[str, Any]:
    return _siren_factory().for_request(request).root(
        self_href=request.build_absolute_uri("/api/"),
        title="Modwire API",
        version=settings.RELEASE_VERSION,
        service_desc_href=request.build_absolute_uri("/api/openapi.json"),
        extra_links=(
            {"rel": ["browser"], "href": request.build_absolute_uri("/browser/")},
        ),
    )


@lru_cache(maxsize=1)
def _projection_configs() -> tuple[_ProjectionConfig, ...]:
    paths = _openapi_schema().get("paths", {})
    configs: list[_ProjectionConfig] = []
    for resource_path, path_item in paths.items():
        resource = path_item.get(SIREN_RESOURCE_EXTENSION)
        if not resource:
            continue
        if resource.get("collection-only"):
            configs.extend(_collection_only_configs(resource_path, path_item, resource))
            continue

        configs.append(
            _ProjectionConfig(
                path=resource_path,
                methods=_methods(path_item),
                kind="entity",
                resource_name=resource["name"],
                operation_ids=_merge_operation_ids(
                    _operation_ids(path_item),
                    tuple(resource.get("operations", ())),
                ),
                path_parameters=dict(resource.get("path-parameters", {})),
            )
        )
        collection_path = _parent_path(resource_path)
        if collection_path in paths and not _has_placeholders(collection_path):
            collection_path_item = paths[collection_path]
            collection_operation_ids = _merge_operation_ids(
                _operation_ids(collection_path_item),
                tuple(resource.get("collection-operations", ())),
            )
            collection_methods = ("get",) if "get" in collection_path_item else ()
            if collection_operation_ids and collection_methods:
                configs.append(
                    _ProjectionConfig(
                        path=collection_path,
                        methods=collection_methods,
                        kind="collection",
                        resource_name=resource["name"],
                        operation_ids=collection_operation_ids,
                        item_operation_ids=_get_operation_ids(path_item),
                        path_parameters={},
                    )
                )
            entity_methods = tuple(method for method in _methods(collection_path_item) if method != "get")
            if entity_methods:
                configs.append(
                    _ProjectionConfig(
                        path=collection_path,
                        methods=entity_methods,
                        kind="entity",
                        resource_name=resource["name"],
                        operation_ids=_merge_operation_ids(
                            _operation_ids(path_item),
                            tuple(resource.get("operations", ())),
                        ),
                        path_parameters={},
                    )
                )
    return tuple(sorted(configs, key=_projection_priority))


def _collection_only_configs(
    path: str,
    path_item: dict[str, Any],
    resource: dict[str, Any],
) -> tuple[_ProjectionConfig, ...]:
    return tuple(
        _ProjectionConfig(
            path=path,
            methods=(method,),
            kind="collection" if _is_list_operation(operation) else "entity",
            resource_name=resource["name"],
            operation_ids=_method_operation_ids(path_item, method),
            path_parameters=dict(resource.get("path-parameters", {})),
        )
        for method, operation in _method_operations(path_item)
    )


def _projection_config(path: str, method: str) -> tuple[_ProjectionConfig, dict[str, str]]:
    normalized = path.rstrip("/") or path
    paths = _openapi_schema().get("paths", {})
    method = method.lower()
    for config in _projection_configs():
        if method not in config.methods:
            continue
        match = re.fullmatch(_path_pattern(config.path, paths[config.path]), normalized)
        if not match:
            continue
        return config, {
            config.path_parameters[name]: value
            for name, value in match.groupdict().items()
        }
    raise OpenApiError(f"No Siren projection is configured for API path {path!r}")


def _path_pattern(template: str, path_item: dict[str, Any]) -> str:
    parameter_patterns = _path_parameter_patterns(path_item)
    pattern = ""
    index = 0
    for match in re.finditer(r"\{([^}]+)\}", template):
        pattern += re.escape(template[index:match.start()])
        name = match.group(1)
        pattern += rf"(?P<{name}>{parameter_patterns.get(name, '[^/]+')})"
        index = match.end()
    pattern += re.escape(template[index:])
    return pattern


def _path_parameter_patterns(path_item: dict[str, Any]) -> dict[str, str]:
    patterns: dict[str, str] = {}
    for operation in _operations(path_item):
        for parameter in operation.get("parameters", ()):
            if parameter.get("in") != "path":
                continue
            name = parameter["name"]
            schema_pattern = parameter.get("schema", {}).get("pattern", "")
            patterns[name] = ".+" if "/" in schema_pattern else "[^/]+"
    return patterns


def _projection_priority(config: _ProjectionConfig) -> tuple[bool, int]:
    return (_has_placeholders(config.path), -len(config.path))


def _operations(path_item: dict[str, Any]):
    return (
        operation
        for _, operation in _method_operations(path_item)
    )


def _method_operations(path_item: dict[str, Any]):
    return (
        (method, operation)
        for method, operation in path_item.items()
        if method in HTTP_METHODS and isinstance(operation, dict)
    )


def _methods(path_item: dict[str, Any]) -> tuple[str, ...]:
    return tuple(method for method, _ in _method_operations(path_item))


def _is_list_operation(operation: dict[str, Any]) -> bool:
    operation_id = operation.get("operationId", "")
    return isinstance(operation_id, str) and operation_id.startswith("list_")




def _operation_ids(path_item: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        operation["operationId"]
        for operation in _operations(path_item)
        if operation.get("operationId")
    )


def _method_operation_ids(path_item: dict[str, Any], *methods: str) -> tuple[str, ...]:
    return tuple(
        operation["operationId"]
        for method, operation in _method_operations(path_item)
        if method in methods and operation.get("operationId")
    )


def _get_operation_ids(path_item: dict[str, Any]) -> tuple[str, ...]:
    operation = path_item.get("get", {})
    return (operation["operationId"],) if operation.get("operationId") else ()


def _merge_operation_ids(*groups: tuple[str, ...]) -> tuple[str, ...]:
    operation_ids = []
    seen = set()
    for group in groups:
        for operation_id in group:
            if operation_id in seen:
                continue
            seen.add(operation_id)
            operation_ids.append(operation_id)
    return tuple(operation_ids)


def _parent_path(path: str) -> str:
    return path.rstrip("/").rsplit("/", 1)[0] or "/"


def _has_placeholders(path: str) -> bool:
    return bool(re.search(r"\{[^}]+}", path))


def _pagination(request, data: list[Any]):
    if "limit" not in request.GET:
        if request.GET:
            return CustomPagination(
                count=len(data),
                links=(PaginationLinkInput(rel="self", query=dict(request.GET.items())),),
            )
        return None
    limit = max(int(request.GET.get("limit", 1)), 1)
    offset = max(int(request.GET.get("offset", 0)), 0)
    if set(request.GET) <= {"limit", "offset"}:
        return OffsetPagination(limit=limit, offset=offset, count=len(data), has_next=len(data) == limit)

    links = [PaginationLinkInput(rel="self", query=dict(request.GET.items()))]
    first = request.GET.copy()
    first["offset"] = 0
    links.append(PaginationLinkInput(rel="first", query=dict(first.items())))
    if offset > 0:
        previous = request.GET.copy()
        previous["offset"] = max(0, offset - limit)
        links.append(PaginationLinkInput(rel="previous", query=dict(previous.items())))
    if len(data) == limit:
        next_page = request.GET.copy()
        next_page["offset"] = offset + limit
        links.append(PaginationLinkInput(rel="next", query=dict(next_page.items())))
    return CustomPagination(count=len(data), links=tuple(links))


def _project_response(request, data, status_code: int) -> HttpResponse:
    config, path_values = _projection_config(request.path, request.method)
    adapter = _adapter(request)
    if config.kind == "collection":
        if not isinstance(data, list | tuple):
            raise TypeError(f"Siren collection projection requires a list or tuple for {request.path}")
        request_kwargs = {
            "resource_name": config.resource_name,
            "items": tuple(data),
            "collection_operation_ids": config.operation_ids,
            "item_operation_ids": config.item_operation_ids,
            "path_values": path_values,
        }
        if pagination := _pagination(request, list(data)):
            request_kwargs["pagination"] = pagination
        payload = adapter.collection(SirenCollectionRequest(**request_kwargs), status_code=status_code)
    else:
        properties = data if isinstance(data, dict) else {"value": data}
        payload = adapter.entity(
            config.resource_name,
            properties,
            operations=config.operation_ids,
            path_values=path_values,
            status_code=status_code,
        )
    return to_django_response(payload)


def _problem_response(request, response, data) -> HttpResponse:
    detail = data.get("detail", data) if isinstance(data, dict) else data
    payload = _adapter(request).problem(
        {
            "title": response.reason_phrase,
            "status": response.status_code,
            "detail": str(detail),
        },
        status_code=response.status_code,
    )
    result = to_django_response(payload)
    _copy_headers(response, result)
    return result


def _no_content_response(request, response) -> HttpResponse:
    payload = _adapter(request).no_content(headers=_headers(response))
    return to_django_response(payload)


def _copy_headers(source, target) -> None:
    for key, value in _headers(source).items():
        target[key] = value


def _headers(response) -> dict[str, str]:
    return {
        key: value
        for key, value in response.items()
        if key.lower() not in {"content-type", "content-length"}
    }


class SirenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/") or request.path in {"/api/openapi.json", "/api/docs"}:
            return response
        if response.status_code == 204:
            return _no_content_response(request, response)
        if not response.get("Content-Type", "").startswith("application/json"):
            return response
        try:
            data = json.loads(response.content)
        except (TypeError, ValueError, json.JSONDecodeError):
            return response
        if response.status_code >= 400:
            return _problem_response(request, response, data)
        if isinstance(data, dict) and "class" in data and "links" in data:
            return response

        result = _project_response(request, data, response.status_code)
        _copy_headers(response, result)
        return result
