from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from modwire.shared.api.errors import validated
from modwire.shared.api.hypermedia import siren_resource
from modwire.shared.api.types import ShortUUID

from ...services.variable import VariableService
from .schemas import VariableIn, VariableOut, VariablePatchIn


@siren_resource(
    name="variable",
    path="/api/variables/{variable_id}",
    class_="variable",
    identifier="id",
    path_parameters={"variable_id": "id"},
    relations={"scaffolding": {"rel": "scaffolding", "resource": "scaffolding", "many": False}},
)
@api_controller("/variables", tags=["Variables"])
class VariableController(ControllerBase):
    @route.get(
        "",
        response=list[VariableOut],
        operation_id="list_variables",
        summary="List variables.",
    )
    @inject
    def list(self, service: Annotated[VariableService, Inject()]):
        return service.list()

    @route.get(
        "/{variable_id}",
        response=VariableOut,
        operation_id="get_variable",
        summary="Get variable.",
    )
    @inject
    def get(self, variable_id: ShortUUID, service: Annotated[VariableService, Inject()]):
        return service.get(variable_id)

    @route.post(
        "",
        response=VariableOut,
        operation_id="create_variable",
        summary="Create variable.",
    )
    @inject
    def create(self, data: VariableIn, service: Annotated[VariableService, Inject()]):
        return validated(service.create, **data.model_dump())

    @route.put(
        "/{variable_id}",
        response=VariableOut,
        operation_id="update_variable",
        summary="Update variable.",
    )
    @inject
    def update(
        self,
        variable_id: ShortUUID,
        data: VariableIn,
        service: Annotated[VariableService, Inject()],
    ):
        return validated(service.update, variable_id, **data.model_dump())

    @route.patch(
        "/{variable_id}",
        response=VariableOut,
        operation_id="partial_update_variable",
        summary="Partially update variable.",
    )
    @inject
    def partial_update(
        self,
        variable_id: ShortUUID,
        data: VariablePatchIn,
        service: Annotated[VariableService, Inject()],
    ):
        return validated(service.update, variable_id, **data.model_dump(exclude_unset=True, warnings=False))

    @route.delete(
        "/{variable_id}",
        response={204: None},
        operation_id="delete_variable",
        summary="Delete variable.",
    )
    @inject
    def delete(self, variable_id: ShortUUID, service: Annotated[VariableService, Inject()]):
        service.delete(variable_id)
        return Status(204, None)
