from collections.abc import Callable
from dataclasses import dataclass
from inspect import Parameter, Signature
from typing import Any

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route


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

    @property
    def controller_path(self) -> str:
        return self.collection_path.removeprefix("/api")

    @property
    def route_entity_path(self) -> str:
        return self.entity_path.removeprefix(self.collection_path)

    @property
    def plural_name(self) -> str:
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


class CrudMethodFactory:
    def __init__(self, resource: CrudResource):
        self._resource = resource

    def methods(self) -> dict[str, Callable[..., Any]]:
        return {
            "list": self._list(),
            "get": self._get(),
            "create": self._create(),
            "update": self._update(),
            "partial_update": self._partial_update(),
            "delete": self._delete(),
        }

    def _list(self):
        resource = self._resource

        def method(self):
            return resource.service().list()
        method.__name__ = "list"

        return route.get(
            "",
            response=list[resource.out_schema],
            operation_id=f"list_{resource.plural_name}",
            summary=resource.summaries["list"],
        )(SignatureBuilder(method).build("self"))

    def _get(self):
        resource = self._resource

        def method(self, **kwargs):
            return resource.service().get(kwargs[resource.path_parameter])
        method.__name__ = "get"

        return route.get(
            resource.route_entity_path,
            response=resource.out_schema,
            operation_id=f"get_{resource.name}",
            summary=resource.summaries["get"],
        )(SignatureBuilder(method).build("self", resource.path_parameter, resource=resource))

    def _create(self):
        resource = self._resource

        def method(self, data):
            try:
                return resource.service().create(**data.model_dump())
            except (ValidationError, IntegrityError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "create"

        return route.post(
            "",
            response=resource.out_schema,
            operation_id=f"create_{resource.name}",
            summary=resource.summaries["create"],
        )(SignatureBuilder(method).build("self", "data", data_schema=resource.in_schema))

    def _update(self):
        resource = self._resource

        def method(self, **kwargs):
            try:
                data = kwargs["data"]
                return resource.service().update(
                    kwargs[resource.path_parameter],
                    **data.model_dump(),
                )
            except (ValidationError, IntegrityError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "update"

        return route.put(
            resource.route_entity_path,
            response=resource.out_schema,
            operation_id=f"update_{resource.name}",
            summary=resource.summaries["update"],
        )(SignatureBuilder(method).build(
            "self",
            resource.path_parameter,
            "data",
            resource=resource,
            data_schema=resource.in_schema,
        ))

    def _partial_update(self):
        resource = self._resource

        def method(self, **kwargs):
            try:
                data = kwargs["data"]
                payload = data.model_dump(exclude_unset=True, warnings=False)
                return resource.service().update(kwargs[resource.path_parameter], **payload)
            except (ValidationError, IntegrityError) as error:
                raise resource.validation_error(error) from error
        method.__name__ = "partial_update"

        return route.patch(
            resource.route_entity_path,
            response=resource.out_schema,
            operation_id=f"partial_update_{resource.name}",
            summary=resource.summaries["partial_update"],
        )(SignatureBuilder(method).build(
            "self",
            resource.path_parameter,
            "data",
            resource=resource,
            data_schema=resource.patch_schema,
        ))

    def _delete(self):
        resource = self._resource

        def method(self, **kwargs):
            resource.service().delete(kwargs[resource.path_parameter])
            return Status(204, None)
        method.__name__ = "delete"

        return route.delete(
            resource.route_entity_path,
            response={204: None},
            operation_id=f"delete_{resource.name}",
            summary=resource.summaries["delete"],
        )(SignatureBuilder(method).build("self", resource.path_parameter, resource=resource))


class SignatureBuilder:
    def __init__(self, method):
        self._method = method

    def build(
        self,
        *names: str,
        resource: CrudResource | None = None,
        data_schema: Any = Parameter.empty,
    ):
        parameters = []
        for name in names:
            annotation = Parameter.empty
            if name == "data":
                annotation = data_schema
            elif resource is not None and name == resource.path_parameter:
                annotation = resource.path_parameter_type
            parameters.append(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=annotation))
        self._method.__signature__ = Signature(parameters)
        return self._method
