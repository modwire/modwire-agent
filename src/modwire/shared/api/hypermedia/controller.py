from collections.abc import Callable
from dataclasses import dataclass
from inspect import Parameter, Signature
from typing import Annotated, Any

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject


@dataclass(frozen=True, slots=True)
class QuerySpec:
    name: str
    annotation: Any
    default: Any
    service_name: str | None = None

    @property
    def argument_name(self) -> str:
        return self.service_name or self.name


@dataclass(frozen=True, slots=True)
class CrudResource:
    name: str
    collection_path: str
    entity_path: str
    path_parameter: str
    path_parameter_type: Any
    in_schema: Any
    out_schema: Any
    patch_schema: Any
    service: type
    tags: tuple[str, ...]
    summaries: dict[str, str]
    validation_error: Callable[[Exception], Exception]
    list_schema: Any | None = None
    list_queries: tuple[QuerySpec, ...] = ()
    route_path: str | None = None
    methods: tuple[str, ...] = ("list", "get", "create", "update", "partial_update", "delete")
    list_operation_name: str | None = None

    @property
    def controller_path(self) -> str:
        return self.collection_path.removeprefix("/api")

    @property
    def route_entity_path(self) -> str:
        return self.route_path or self.entity_path.removeprefix(self.collection_path)

    @property
    def plural_name(self) -> str:
        if self.list_operation_name:
            return self.list_operation_name
        if self.name.endswith("y"):
            return f"{self.name[:-1]}ies"
        return f"{self.name}s"


@dataclass(frozen=True, slots=True)
class CollectionResource:
    name: str
    collection_path: str
    out_schema: Any
    service: type
    tags: tuple[str, ...]
    summary: str
    service_method: str = "list"
    list_operation_name: str | None = None
    list_queries: tuple[QuerySpec, ...] = ()

    @property
    def controller_path(self) -> str:
        return self.collection_path.removeprefix("/api")

    @property
    def plural_name(self) -> str:
        if self.list_operation_name:
            return self.list_operation_name
        if self.name.endswith("y"):
            return f"{self.name[:-1]}ies"
        return f"{self.name}s"


class ResourceController:
    def __init__(self, resource: CrudResource):
        self._resource = resource

    def __call__(self, controller):
        attrs = {
            name: value
            for name, value in vars(controller).items()
            if name not in {"__dict__", "__weakref__"}
        }
        attrs.update(CrudMethodFactory(self._resource).methods())
        generated = type(controller.__name__, (controller, ControllerBase), attrs)
        generated.__module__ = controller.__module__
        return api_controller(
            self._resource.controller_path,
            tags=list(self._resource.tags),
        )(generated)


class CollectionController:
    def __init__(self, resource: CollectionResource):
        self._resource = resource

    def __call__(self, controller):
        attrs = {
            name: value
            for name, value in vars(controller).items()
            if name not in {"__dict__", "__weakref__"}
        }
        attrs["list"] = CollectionMethodFactory(self._resource).list_method()
        generated = type(controller.__name__, (controller, ControllerBase), attrs)
        generated.__module__ = controller.__module__
        return api_controller(
            self._resource.controller_path,
            tags=list(self._resource.tags),
        )(generated)


class CollectionMethodFactory:
    def __init__(self, resource: CollectionResource):
        self._resource = resource

    def list_method(self):
        resource = self._resource

        def method(self, service, **kwargs):
            arguments = {
                query.argument_name: kwargs[query.name]
                for query in resource.list_queries
            }
            return getattr(service, resource.service_method)(**arguments)
        method.__name__ = "list"

        return route.get(
            "",
            response=list[resource.out_schema],
            operation_id=f"list_{resource.plural_name}",
            summary=resource.summary,
        )(inject(SignatureBuilder(method).build(
            "self",
            "service",
            *resource.list_queries,
            collection_resource=resource,
        )))


class CrudMethodFactory:
    def __init__(self, resource: CrudResource):
        self._resource = resource

    def methods(self) -> dict[str, Callable[..., Any]]:
        methods = {
            "list": self._list(),
            "get": self._get(),
            "create": self._create(),
            "update": self._update(),
            "partial_update": self._partial_update(),
            "delete": self._delete(),
        }
        return {
            name: method
            for name, method in methods.items()
            if name in self._resource.methods
        }

    def _list(self):
        resource = self._resource

        def method(self, service, **kwargs):
            arguments = {
                query.argument_name: kwargs[query.name]
                for query in resource.list_queries
            }
            return service.list(**arguments)
        method.__name__ = "list"

        return route.get(
            "",
            response=list[resource.list_schema or resource.out_schema],
            operation_id=f"list_{resource.plural_name}",
            summary=resource.summaries["list"],
        )(inject(SignatureBuilder(method).build("self", "service", *resource.list_queries, resource=resource)))

    def _get(self):
        resource = self._resource

        def method(self, service, **kwargs):
            return service.get(kwargs[resource.path_parameter])
        method.__name__ = "get"

        return route.get(
            resource.route_entity_path,
            response=resource.out_schema,
            operation_id=f"get_{resource.name}",
            summary=resource.summaries["get"],
        )(inject(SignatureBuilder(method).build("self", "service", resource.path_parameter, resource=resource)))

    def _create(self):
        resource = self._resource

        def method(self, service, data):
            try:
                return service.create(**data.model_dump())
            except (ValidationError, IntegrityError, ValueError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "create"

        return route.post(
            "",
            response=resource.out_schema,
            operation_id=f"create_{resource.name}",
            summary=resource.summaries["create"],
        )(inject(SignatureBuilder(method).build("self", "service", "data", resource=resource, data_schema=resource.in_schema)))

    def _update(self):
        resource = self._resource

        def method(self, service, **kwargs):
            try:
                data = kwargs["data"]
                return service.update(
                    kwargs[resource.path_parameter],
                    **data.model_dump(),
                )
            except (ValidationError, IntegrityError, ValueError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "update"

        return route.put(
            resource.route_entity_path,
            response=resource.out_schema,
            operation_id=f"update_{resource.name}",
            summary=resource.summaries["update"],
        )(inject(SignatureBuilder(method).build(
            "self",
            "service",
            resource.path_parameter,
            "data",
            resource=resource,
            data_schema=resource.in_schema,
        )))

    def _partial_update(self):
        resource = self._resource

        def method(self, service, **kwargs):
            try:
                data = kwargs["data"]
                payload = data.model_dump(exclude_unset=True, warnings=False)
                return service.update(kwargs[resource.path_parameter], **payload)
            except (ValidationError, IntegrityError, ValueError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "partial_update"

        return route.patch(
            resource.route_entity_path,
            response=resource.out_schema,
            operation_id=f"partial_update_{resource.name}",
            summary=resource.summaries["partial_update"],
        )(inject(SignatureBuilder(method).build(
            "self",
            "service",
            resource.path_parameter,
            "data",
            resource=resource,
            data_schema=resource.patch_schema,
        )))

    def _delete(self):
        resource = self._resource

        def method(self, service, **kwargs):
            try:
                service.delete(kwargs[resource.path_parameter])
                return Status(204, None)
            except (ValidationError, IntegrityError, ValueError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "delete"

        return route.delete(
            resource.route_entity_path,
            response={204: None},
            operation_id=f"delete_{resource.name}",
            summary=resource.summaries["delete"],
        )(inject(SignatureBuilder(method).build("self", "service", resource.path_parameter, resource=resource)))


class SignatureBuilder:
    def __init__(self, method):
        self._method = method

    def build(
        self,
        *items: str | QuerySpec,
        resource: CrudResource | None = None,
        collection_resource: CollectionResource | None = None,
        data_schema: Any = Parameter.empty,
    ):
        parameters = []
        for item in items:
            if isinstance(item, QuerySpec):
                parameters.append(
                    Parameter(
                        item.name,
                        Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=item.annotation,
                        default=item.default,
                    )
                )
                continue
            name = item
            annotation = Parameter.empty
            service_type = resource.service if resource is not None else None
            if collection_resource is not None:
                service_type = collection_resource.service
            if name == "service":
                annotation = Annotated[service_type, Inject()]
            elif name == "data":
                annotation = data_schema
            elif resource is not None and name == resource.path_parameter:
                annotation = resource.path_parameter_type
            parameters.append(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=annotation))
        self._method.__signature__ = Signature(parameters)
        return self._method
