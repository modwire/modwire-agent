import json
from functools import lru_cache
from typing import Any

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
from modwire_siren.standards import SirenMediaType

from modwire.shared.api.hypermedia import ProjectionCatalog

SIREN_TYPE = str(SirenMediaType.ENTITY)
PROBLEM_TYPE = str(SirenMediaType.PROBLEM)


def _base_url(request) -> str:
    return request.build_absolute_uri("/")


@lru_cache(maxsize=1)
def _openapi_schema() -> dict[str, Any]:
    from modwire.core.api import api

    return api.get_openapi_schema()


@lru_cache(maxsize=1)
def _siren_factory():
    return ModwireSirenFactory.web(_openapi_schema(), base_url_resolver=_base_url)


@lru_cache(maxsize=1)
def _projection_catalog() -> ProjectionCatalog:
    from modwire.core.api import RESOURCE_SPECS

    return ProjectionCatalog(_openapi_schema(), RESOURCE_SPECS)


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


def _projection_config(path: str, method: str):
    return _projection_catalog().match(path, method)


def _pagination(request, data: list[Any]):
    if "limit" not in request.GET:
        if request.GET:
            return CustomPagination(
                count=len(data),
                links=(PaginationLinkInput(rel="self", query=_query_pairs(request.GET)),),
            )
        return None
    limit = max(int(request.GET.get("limit", 1)), 1)
    offset = max(int(request.GET.get("offset", 0)), 0)
    if set(request.GET) <= {"limit", "offset"}:
        return OffsetPagination(limit=limit, offset=offset, count=len(data), has_next=len(data) == limit)

    links = [PaginationLinkInput(rel="self", query=_query_pairs(request.GET))]
    links.append(PaginationLinkInput(rel="first", query=_query_pairs(request.GET, offset=0)))
    if offset > 0:
        links.append(
            PaginationLinkInput(
                rel="previous",
                query=_query_pairs(request.GET, offset=max(0, offset - limit)),
            )
        )
    if len(data) == limit:
        links.append(PaginationLinkInput(rel="next", query=_query_pairs(request.GET, offset=offset + limit)))
    return CustomPagination(count=len(data), links=tuple(links))


def _query_pairs(query, **overrides) -> tuple[tuple[str, Any], ...]:
    pairs = [
        (key, value)
        for key, values in query.lists()
        if key not in overrides
        for value in values
    ]
    pairs.extend(overrides.items())
    return tuple(pairs)


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
