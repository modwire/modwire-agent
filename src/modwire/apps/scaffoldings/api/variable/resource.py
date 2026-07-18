from modwire.apps.scaffoldings.services.variable import VariableService
from modwire.shared.api.errors import validation_error
from modwire.shared.api.hypermedia import CrudResource, ResourceSpec
from modwire.shared.api.types import ShortUUID

from .schemas import VariableIn, VariableOut, VariablePatchIn

variable = CrudResource(
    name="variable",
    collection_path="/api/variables",
    entity_path="/api/variables/{variable_id}",
    path_parameter="variable_id",
    path_parameter_type=ShortUUID,
    in_schema=VariableIn,
    out_schema=VariableOut,
    patch_schema=VariablePatchIn,
    service=VariableService,
    tags=("Variables",),
    summaries={
        "list": "List variables.",
        "get": "Get variable.",
        "create": "Create variable.",
        "update": "Update variable.",
        "partial_update": "Partially update variable.",
        "delete": "Delete variable.",
    },
    validation_error=validation_error,
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="variable",
        path="/api/variables/{variable_id}",
        resource_class="variable",
        identifier="id",
        path_parameters={"variable_id": "id"},
        relations={"scaffolding": {"rel": "scaffolding", "resource": "scaffolding", "many": False}},
    ),
)
