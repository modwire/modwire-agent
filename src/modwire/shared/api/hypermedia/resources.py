from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, TypeVar

from modwire_siren.openapi.relation_spec import SirenRelationSpec
from modwire_siren.openapi.resource_spec import SirenResourceSpec

T = TypeVar("T")

RESOURCE_SPECS_ATTRIBUTE = "modwire_hypermedia_resource_specs"


@dataclass(frozen=True, slots=True)
class RelationSpec:
    rel: str
    resource: str
    many: bool

    @classmethod
    def from_input(cls, value: "RelationSpec | SirenRelationSpec | Mapping[str, Any]") -> "RelationSpec":
        if isinstance(value, RelationSpec):
            return value
        if isinstance(value, SirenRelationSpec):
            return cls(rel=value.rel, resource=value.resource, many=value.many)
        rel = value["rel"]
        resource = value["resource"]
        many = value["many"]
        if not isinstance(rel, str):
            raise ValueError("Siren relation 'rel' must be a string")
        if not isinstance(resource, str):
            raise ValueError("Siren relation 'resource' must be a string")
        if not isinstance(many, bool):
            raise ValueError("Siren relation 'many' must be a boolean")
        return cls(rel=rel, resource=resource, many=many)

    def to_modwire_siren(self) -> SirenRelationSpec:
        return SirenRelationSpec(rel=self.rel, resource=self.resource, many=self.many)


@dataclass(frozen=True, slots=True)
class ResourceSpec:
    name: str
    path: str | None
    resource_class: str | None
    identifier: str
    path_parameters: Mapping[str, str] | None
    relations: Mapping[str, RelationSpec]
    operations: tuple[str, ...] = ()
    collection_operations: tuple[str, ...] = ()
    path_operation_ids: tuple[str, ...] = ()
    collection_only: bool = False
    singleton: bool = False
    root_visible: bool | None = None

    def to_modwire_siren(self) -> SirenResourceSpec:
        if self.path is None:
            raise ValueError(f"Siren resource {self.name!r} must be resolved before export")
        if self.resource_class is None:
            raise ValueError(f"Siren resource {self.name!r} must be resolved before export")
        if self.path_parameters is None:
            raise ValueError(f"Siren resource {self.name!r} must be resolved before export")
        return SirenResourceSpec(
            name=self.name,
            path=self.path,
            resource_class=self.resource_class,
            identifier=self.identifier,
            path_parameters=dict(self.path_parameters),
            relations={
                field: relation.to_modwire_siren()
                for field, relation in self.relations.items()
            },
            operations=self.operations,
            collection_operations=self.collection_operations,
            collection_only=self.collection_only,
            singleton=self.singleton,
            root_visible=self.root_visible,
        )


class ResourceDecorator:
    def __init__(
        self,
        *,
        name: str,
        path: str | None,
        resource_class: str | None,
        identifier: str,
        path_parameters: Mapping[str, str] | None,
        relations: Mapping[str, RelationSpec | SirenRelationSpec | Mapping[str, Any]],
        operations: tuple[str, ...] = (),
        collection_operations: tuple[str, ...] = (),
        path_operation_ids: tuple[str, ...] = (),
        collection_only: bool = False,
        singleton: bool = False,
        root_visible: bool | None = None,
    ):
        self._spec = ResourceSpec(
            name=name,
            path=path,
            resource_class=resource_class,
            identifier=identifier,
            path_parameters=dict(path_parameters) if path_parameters is not None else None,
            relations={
                field: RelationSpec.from_input(relation)
                for field, relation in relations.items()
            },
            operations=tuple(operations),
            collection_operations=tuple(collection_operations),
            path_operation_ids=tuple(path_operation_ids),
            collection_only=collection_only,
            singleton=singleton,
            root_visible=root_visible,
        )

    def __call__(self, controller: T) -> T:
        existing = getattr(controller, RESOURCE_SPECS_ATTRIBUTE, ())
        setattr(controller, RESOURCE_SPECS_ATTRIBUTE, (*existing, self._spec))
        return controller


def siren_resource(
    *,
    name: str,
    identifier: str,
    relations: Mapping[str, RelationSpec | SirenRelationSpec | Mapping[str, Any]],
    path: str | None = None,
    class_: str | None = None,
    path_parameters: Mapping[str, str] | None = None,
    operations: tuple[str, ...] = (),
    collection_operations: tuple[str, ...] = (),
    path_operations: tuple[str, ...] = (),
    collection_only: bool = False,
    singleton: bool = False,
    root_visible: bool | None = None,
) -> ResourceDecorator:
    return ResourceDecorator(
        name=name,
        path=path,
        resource_class=class_,
        identifier=identifier,
        path_parameters=path_parameters,
        relations=relations,
        operations=operations,
        collection_operations=collection_operations,
        path_operation_ids=path_operations,
        collection_only=collection_only,
        singleton=singleton,
        root_visible=root_visible,
    )


def collect_resources(*controllers: Any) -> tuple[ResourceSpec, ...]:
    return tuple(
        resource
        for controller in controllers
        for resource in getattr(controller, RESOURCE_SPECS_ATTRIBUTE, ())
    )


def collect_siren_resources(*controllers: Any) -> tuple[SirenResourceSpec, ...]:
    return tuple(resource.to_modwire_siren() for resource in collect_resources(*controllers))


def resolve_resources(schema: dict[str, Any], resources: tuple[ResourceSpec, ...]) -> tuple[ResourceSpec, ...]:
    return tuple(_resolve_resource(schema, resource) for resource in resources)


def siren_specs(resources: tuple[ResourceSpec, ...]) -> tuple[SirenResourceSpec, ...]:
    return tuple(resource.to_modwire_siren() for resource in resources)


def _resolve_resource(schema: dict[str, Any], resource: ResourceSpec) -> ResourceSpec:
    path = resource.path or _path_for_resource(schema, resource)
    return ResourceSpec(
        name=resource.name,
        path=path,
        resource_class=resource.resource_class or _resource_class(resource.name),
        identifier=resource.identifier,
        path_parameters=resource.path_parameters if resource.path_parameters is not None else _path_parameters(path, resource),
        relations=resource.relations,
        operations=resource.operations,
        collection_operations=resource.collection_operations,
        path_operation_ids=resource.path_operation_ids,
        collection_only=resource.collection_only,
        singleton=resource.singleton,
        root_visible=resource.root_visible,
    )


def _path_for_resource(schema: dict[str, Any], resource: ResourceSpec) -> str:
    operation_ids = resource.path_operation_ids or _default_path_operation_ids(resource)
    paths = schema.get("paths", {})
    matches = [
        path
        for path, path_item in paths.items()
        if any(
            operation.get("operationId") in operation_ids
            for operation in _operations(path_item)
        )
    ]
    if not matches:
        raise ValueError(
            f"Cannot infer Siren path for resource {resource.name!r}; "
            f"none of operation IDs {operation_ids!r} exist in OpenAPI"
        )
    if len(matches) > 1:
        raise ValueError(
            f"Cannot infer Siren path for resource {resource.name!r}; "
            f"operation IDs {operation_ids!r} match multiple paths: {matches!r}"
        )
    return matches[0]


def _default_path_operation_ids(resource: ResourceSpec) -> tuple[str, ...]:
    if resource.collection_only:
        return (f"list_{_plural(resource.name)}",)
    return (f"get_{resource.name}",)


def _path_parameters(path: str, resource: ResourceSpec) -> dict[str, str]:
    placeholders = _path_placeholders(path)
    if not placeholders:
        return {}
    if len(placeholders) == 1:
        return {placeholders[0]: resource.identifier}
    raise ValueError(
        f"Cannot infer path parameters for Siren resource {resource.name!r}; "
        f"path {path!r} has multiple parameters"
    )


def _path_placeholders(path: str) -> tuple[str, ...]:
    import re

    return tuple(re.findall(r"\{([^}]+)}", path))


def _resource_class(name: str) -> str:
    return name.replace("_", "-")


def _plural(name: str) -> str:
    if name.endswith("y"):
        return f"{name[:-1]}ies"
    return f"{name}s"


def _operations(path_item: Any):
    if not isinstance(path_item, dict):
        return ()
    return (
        operation
        for method, operation in path_item.items()
        if method in {"get", "post", "put", "patch", "delete"} and isinstance(operation, dict)
    )
