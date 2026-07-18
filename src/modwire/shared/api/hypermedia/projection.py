import re
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Literal

from modwire_siren.openapi.error import OpenApiError

from .resources import ResourceSpec

HTTP_METHODS = ("get", "post", "put", "patch", "delete")


@dataclass(frozen=True, slots=True)
class ProjectionConfig:
    path: str
    methods: tuple[str, ...]
    kind: Literal["collection", "entity"]
    resource_name: str
    operation_ids: tuple[str, ...]
    path_parameters: dict[str, str]
    item_operation_ids: tuple[str, ...] = ()


class ProjectionCatalog:
    def __init__(self, schema: dict[str, Any], resources: tuple[ResourceSpec, ...]):
        self._schema = schema
        self._resources = resources

    @cached_property
    def configs(self) -> tuple[ProjectionConfig, ...]:
        paths = self._schema.get("paths", {})
        configs: list[ProjectionConfig] = []
        for resource in self._resources:
            path_item = paths.get(resource.path)
            if not isinstance(path_item, dict):
                raise OpenApiError(f"Siren resource path is not present in OpenAPI schema: {resource.path}")
            if resource.collection_only:
                configs.extend(_collection_only_configs(resource, path_item))
                continue
            if resource.singleton:
                configs.append(_entity_config(resource, resource.path, path_item))
                continue

            configs.append(_entity_config(resource, resource.path, path_item))
            collection_path = _parent_path(resource.path)
            if collection_path in paths and not _has_placeholders(collection_path):
                collection_path_item = paths[collection_path]
                collection_operation_ids = _merge_operation_ids(
                    _operation_ids(collection_path_item),
                    resource.collection_operations,
                )
                collection_methods = ("get",) if "get" in collection_path_item else ()
                if collection_operation_ids and collection_methods:
                    configs.append(
                        ProjectionConfig(
                            path=collection_path,
                            methods=collection_methods,
                            kind="collection",
                            resource_name=resource.name,
                            operation_ids=collection_operation_ids,
                            item_operation_ids=_get_operation_ids(path_item),
                            path_parameters={},
                        )
                    )
                entity_methods = tuple(
                    method
                    for method in _methods(collection_path_item)
                    if method != "get"
                )
                if entity_methods:
                    configs.append(
                        ProjectionConfig(
                            path=collection_path,
                            methods=entity_methods,
                            kind="entity",
                            resource_name=resource.name,
                            operation_ids=_merge_operation_ids(
                                _operation_ids(path_item),
                                resource.operations,
                            ),
                            path_parameters={},
                        )
                    )
        return tuple(sorted(configs, key=_projection_priority))

    def match(self, path: str, method: str) -> tuple[ProjectionConfig, dict[str, str]]:
        normalized = path.rstrip("/") or path
        paths = self._schema.get("paths", {})
        method = method.lower()
        for config in self.configs:
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


def _collection_only_configs(resource: ResourceSpec, path_item: dict[str, Any]) -> tuple[ProjectionConfig, ...]:
    return tuple(
        ProjectionConfig(
            path=resource.path,
            methods=(method,),
            kind="collection" if _is_list_operation(operation) else "entity",
            resource_name=resource.name,
            operation_ids=_method_operation_ids(path_item, method),
            path_parameters=dict(resource.path_parameters),
        )
        for method, operation in _method_operations(path_item)
    )


def _entity_config(resource: ResourceSpec, path: str, path_item: dict[str, Any]) -> ProjectionConfig:
    return ProjectionConfig(
        path=path,
        methods=_methods(path_item),
        kind="entity",
        resource_name=resource.name,
        operation_ids=_merge_operation_ids(
            _operation_ids(path_item),
            resource.operations,
        ),
        path_parameters=dict(resource.path_parameters),
    )


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


def _projection_priority(config: ProjectionConfig) -> tuple[bool, int]:
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
