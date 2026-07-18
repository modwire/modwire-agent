from modwire.apps.scaffoldings.services.scaffolding import ScaffoldingService
from modwire.shared.api.errors import validation_error
from modwire.shared.api.hypermedia import CrudResource, ResourceSpec
from modwire.shared.api.types import ShortUUID

from .schemas import ScaffoldingIn, ScaffoldingOut, ScaffoldingPatchIn

scaffolding = CrudResource(
    name="scaffolding",
    collection_path="/api/scaffoldings",
    entity_path="/api/scaffoldings/{scaffolding_id}",
    path_parameter="scaffolding_id",
    path_parameter_type=ShortUUID,
    in_schema=ScaffoldingIn,
    out_schema=ScaffoldingOut,
    patch_schema=ScaffoldingPatchIn,
    service=ScaffoldingService,
    tags=("Scaffoldings",),
    summaries={
        "list": "List scaffoldings.",
        "get": "Get scaffolding.",
        "create": "Create scaffolding.",
        "update": "Update scaffolding.",
        "partial_update": "Partially update scaffolding.",
        "delete": "Delete scaffolding.",
    },
    validation_error=validation_error,
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="scaffolding",
        path="/api/scaffoldings/{scaffolding_id}",
        resource_class="scaffolding",
        identifier="id",
        path_parameters={"scaffolding_id": "id"},
        relations={},
        operations=("get_scaffolding_schema", "get_scaffolding_bundle", "preview_scaffolding"),
        collection_operations=("converge_scaffolding",),
    ),
    ResourceSpec(
        name="scaffolding_convergence",
        path="/api/scaffoldings/converge",
        resource_class="scaffolding-convergence",
        identifier="name",
        path_parameters={},
        relations={},
        singleton=True,
        root_visible=False,
    ),
    ResourceSpec(
        name="scaffolding_schema",
        path="/api/scaffoldings/{scaffolding_id}/schema",
        resource_class="scaffolding-schema",
        identifier="scaffolding_id",
        path_parameters={"scaffolding_id": "scaffolding_id"},
        relations={},
        singleton=True,
    ),
    ResourceSpec(
        name="scaffolding_bundle",
        path="/api/scaffoldings/{scaffolding_id}/bundle",
        resource_class="scaffolding-bundle",
        identifier="scaffolding_id",
        path_parameters={"scaffolding_id": "scaffolding_id"},
        relations={},
        singleton=True,
    ),
    ResourceSpec(
        name="scaffolding_preview",
        path="/api/scaffoldings/{scaffolding_id}/preview",
        resource_class="scaffolding-preview",
        identifier="scaffolding_id",
        path_parameters={"scaffolding_id": "scaffolding_id"},
        relations={},
        singleton=True,
    ),
)
