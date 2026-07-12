import json
import re
from copy import deepcopy
from functools import lru_cache

from django.http import JsonResponse

SIREN_TYPE = "application/vnd.siren+json"
PROBLEM_TYPE = "application/problem+json"

RESOURCE_CLASSES = {
    "package_managers": "package-manager",
    "tool_commands": "tool-command",
    "api_keys": "api-key",
}

RELATED_FIELDS = {
    "section_slug": ("section", "sections"),
    "tag_slugs": ("tag", "tags"),
    "record_slug": ("record", "records"),
    "scaffolding": ("scaffolding", "scaffoldings"),
    "scaffolding_id": ("scaffolding", "scaffoldings"),
    "language": ("language", "languages"),
    "language_id": ("language", "languages"),
    "package_manager": ("package-manager", "package_managers"),
    "tool": ("tool", "tools"),
}


def _absolute(request, path: str) -> str:
    return request.build_absolute_uri(path)


def _resource_class(collection: str) -> str:
    return RESOURCE_CLASSES.get(collection, collection.rstrip("s").replace("_", "-"))


def _identifier(properties: dict):
    return properties.get("slug", properties.get("id"))


def _link(rel: str | list[str], href: str, title: str | None = None) -> dict:
    result = {"rel": [rel] if isinstance(rel, str) else rel, "href": href}
    if title:
        result["title"] = title
    return result


def _resolve_schema(schema: dict, components: dict, resolving: frozenset[str] = frozenset()) -> dict:
    """Bundle an operation schema so a Siren client never needs the OpenAPI document."""
    schema = deepcopy(schema)
    if "$ref" in schema:
        name = schema.pop("$ref").rsplit("/", 1)[-1]
        if name in resolving:
            return schema
        target = deepcopy(components.get(name, {}))
        target.update(schema)
        schema = _resolve_schema(target, components, resolving | {name})
    result = {}
    for key, value in schema.items():
        if key == "mapping" and isinstance(value, dict):
            continue
        if isinstance(value, dict):
            result[key] = _resolve_schema(value, components, resolving)
        elif isinstance(value, list):
            result[key] = [
                _resolve_schema(item, components, resolving) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def _field(name: str, schema: dict, required: bool, components: dict) -> dict:
    schema = _resolve_schema(schema, components)
    kind = schema.get("type", "text")
    result = {
        "name": name,
        "type": {"integer": "number", "boolean": "checkbox"}.get(kind, kind),
        "required": required,
    }
    if schema.get("title"):
        result["title"] = schema["title"]
    if schema.get("description"):
        result["description"] = schema["description"]
    if "default" in schema:
        result["value"] = schema["default"]
    if "enum" in schema:
        result["options"] = [{"value": value, "title": str(value)} for value in schema["enum"]]
    if kind in {"array", "object"} or any(key in schema for key in ("allOf", "anyOf", "oneOf")):
        result["type"] = "json"
        result["schema"] = schema
    for key in ("minimum", "maximum", "minLength", "maxLength", "pattern"):
        if key in schema:
            result[key] = schema[key]
    return result


def _operation_fields(operation: dict, components: dict) -> list[dict]:
    fields = []
    for parameter in operation.get("parameters", []):
        if parameter.get("in") != "query":
            continue
        fields.append(
            _field(parameter["name"], parameter.get("schema", {}), parameter.get("required", False), components)
        )
    content = operation.get("requestBody", {}).get("content", {})
    media = content.get("application/json") or next(iter(content.values()), {})
    schema = _resolve_schema(media.get("schema", {}), components)
    required = set(schema.get("required", []))
    fields.extend(
        _field(name, value, name in required, components) for name, value in schema.get("properties", {}).items()
    )
    return fields


@lru_cache(maxsize=1)
def _openapi():
    from core.api import api

    schema = api.get_openapi_schema()
    paths = {path.removeprefix("/api"): item for path, item in schema.get("paths", {}).items()}
    return paths, schema.get("components", {}).get("schemas", {})


def api_root_document(request) -> dict:
    """Build API discovery links from the generated OpenAPI document."""
    from django.conf import settings

    paths, _ = _openapi()
    collections = {}
    for path, path_item in paths.items():
        segments = path.strip("/").split("/")
        if len(segments) != 1 or not segments[0] or "{" in segments[0]:
            continue
        name = segments[0]
        operation = path_item.get("get") or path_item.get("post") or {}
        collections[name] = operation.get("tags", [name.replace("_", " ").title()])[0]
    absolute = request.build_absolute_uri
    return {
        "class": ["api", "entry-point"],
        "properties": {"title": "Modwire API", "version": settings.RELEASE_VERSION},
        "links": [
            _link("self", absolute("/api/")),
            *(
                _link(name.replace("_", "-"), absolute(f"/api/{name}"), title)
                for name, title in sorted(collections.items())
            ),
            {
                "rel": ["service-desc"],
                "href": absolute("/api/openapi.json"),
                "type": "application/vnd.oai.openapi+json;version=3.1",
            },
            _link("browser", absolute("/browser/")),
        ],
        "actions": [],
    }


def _matching_operations(api_path: str, item: bool) -> list[tuple[str, str, dict]]:
    paths, _ = _openapi()
    matches = []
    for template, path_item in paths.items():
        normalized = template.rstrip("/") or "/"
        is_item = "{" in normalized
        if item != is_item:
            continue
        pattern = re.sub(r"\{[^}]+\}", r"[^/]+(?:/[^/]+)*", normalized)
        if not re.fullmatch(pattern, api_path.rstrip("/") or "/"):
            continue
        for method, operation in path_item.items():
            if method.lower() in {"get", "post", "put", "patch", "delete"}:
                matches.append((template, method.upper(), operation))
    return matches


def _actions(request, api_path: str, properties: dict | None) -> list[dict]:
    paths, components = _openapi()
    item = properties is not None and _identifier(properties) is not None
    actions = []
    operation_path = api_path
    if item and not _matching_operations(operation_path, True):
        collection = "/" + api_path.strip("/").split("/")[0]
        operation_path = f"{collection}/{_identifier(properties)}"
    operations = _matching_operations(operation_path, item)
    if item:
        collection_path = "/" + api_path.strip("/").split("/")[0]
        operations += [op for op in _matching_operations(collection_path, False) if op[1] == "POST"]
    collection_path = "/" + api_path.strip("/").split("/")[0]
    related = []
    for template, path_item in paths.items():
        if not template.startswith(collection_path + "/"):
            continue
        if item:
            if not re.match(rf"^{re.escape(collection_path)}/\{{[^}}]+\}}/[^{{}}]+$", template):
                continue
            resolved = re.sub(r"\{[^}]+\}", str(_identifier(properties)), template, count=1)
        else:
            if "{" in template:
                continue
            resolved = template
        for method, operation in path_item.items():
            if method.lower() in {"get", "post"}:
                related.append((resolved, method.upper(), operation))
    operations += related
    for template, method, operation in operations:
        href = operation_path
        if "{" not in template:
            href = template
        action = {
            "name": operation.get("operationId", f"{method.lower()}-{api_path.strip('/')}"),
            "title": operation.get("summary", operation.get("operationId", method.title())),
            "method": method,
            "href": _absolute(request, "/api" + href),
            "type": "application/json",
            "fields": _operation_fields(operation, components),
        }
        actions.append(action)
    return actions


def _related_links(request, properties: dict) -> list[dict]:
    links = []
    for field, (rel, collection) in RELATED_FIELDS.items():
        value = properties.get(field)
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        links.extend(_link(rel, _absolute(request, f"/api/{collection}/{item}")) for item in values)
    return links


def _entity(request, collection: str, properties: dict) -> dict:
    identifier = _identifier(properties)
    path = f"/api/{collection}/{identifier}" if identifier is not None else f"/api/{collection}"
    links = [_link("collection", _absolute(request, f"/api/{collection}"))]
    if _matching_operations("/" + path.removeprefix("/api/"), True):
        links.insert(0, _link("self", _absolute(request, path)))
    links.extend(_related_links(request, properties))
    return {"class": [_resource_class(collection)], "rel": ["item"], "properties": properties, "links": links}


def _pagination_links(request, data: list, collection: str) -> list[dict]:
    if "limit" not in request.GET:
        return []
    limit = max(int(request.GET.get("limit", 1)), 1)
    offset = max(int(request.GET.get("offset", 0)), 0)
    links = []
    for rel, target in (("first", 0), ("previous", max(0, offset - limit))):
        if rel == "previous" and offset == 0:
            continue
        query = request.GET.copy()
        query["offset"] = target
        links.append(_link(rel, _absolute(request, f"/api/{collection}?{query.urlencode()}")))
    if len(data) == limit:
        query = request.GET.copy()
        query["offset"] = offset + limit
        links.append(_link("next", _absolute(request, f"/api/{collection}?{query.urlencode()}")))
    return links


def siren_document(request, data, collection: str, api_path: str) -> dict:
    root = _absolute(request, "/api/")
    if isinstance(data, list):
        links = [_link("self", request.build_absolute_uri()), _link("api", root)]
        links.extend(_pagination_links(request, data, collection))
        return {
            "class": ["collection", _resource_class(collection)],
            "properties": {"count": len(data)},
            "entities": [_entity(request, collection, item) for item in data],
            "links": links,
            "actions": _actions(request, api_path, None),
        }
    properties = data if isinstance(data, dict) else {"value": data}
    identifier = _identifier(properties)
    links = [_link("self", request.build_absolute_uri()), _link("api", root)]
    if identifier is not None:
        links.append(_link("collection", _absolute(request, f"/api/{collection}")))
    links.extend(_related_links(request, properties))
    return {
        "class": [_resource_class(collection)],
        "properties": properties,
        "links": links,
        "actions": _actions(request, api_path, properties),
    }


class SirenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/") or request.path in {"/api/openapi.json", "/api/docs"}:
            return response
        if response.status_code == 204 or not response.get("Content-Type", "").startswith("application/json"):
            return response
        try:
            data = json.loads(response.content)
        except (TypeError, ValueError, json.JSONDecodeError):
            return response
        if response.status_code >= 400:
            detail = data.get("detail", data) if isinstance(data, dict) else data
            problem = {
                "type": "about:blank",
                "title": response.reason_phrase,
                "status": response.status_code,
                "detail": detail,
            }
            result = JsonResponse(problem, status=response.status_code, content_type=PROBLEM_TYPE)
        else:
            if isinstance(data, dict) and "class" in data and "links" in data:
                result = JsonResponse(data, status=response.status_code, content_type=SIREN_TYPE)
                for key, value in response.items():
                    if key.lower() not in {"content-type", "content-length"}:
                        result[key] = value
                return result
            api_path = request.path.removeprefix("/api").rstrip("/") or "/"
            collection = api_path.strip("/").split("/")[0]
            result = JsonResponse(
                siren_document(request, data, collection, api_path),
                status=response.status_code,
                content_type=SIREN_TYPE,
            )
        for key, value in response.items():
            if key.lower() not in {"content-type", "content-length"}:
                result[key] = value
        return result
