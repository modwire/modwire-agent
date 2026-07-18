from modwire.apps.records.api.errors import validation_error
from modwire.apps.records.services.content import ContentService
from modwire.shared.api.hypermedia import CrudResource, ResourceSpec

from .schemas import ContentIn, ContentOut, ContentPatchIn

content = CrudResource(
    name="content",
    collection_path="/api/contents",
    entity_path="/api/contents/{content_id}",
    path_parameter="content_id",
    path_parameter_type=int,
    in_schema=ContentIn,
    out_schema=ContentOut,
    patch_schema=ContentPatchIn,
    service=ContentService,
    tags=("Contents",),
    summaries={
        "list": "List contents.",
        "get": "Get content.",
        "create": "Create content.",
        "update": "Update content.",
        "partial_update": "Partially update content.",
        "delete": "Delete content.",
    },
    validation_error=validation_error,
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="content",
        path="/api/contents/{content_id}",
        resource_class="content",
        identifier="id",
        path_parameters={"content_id": "id"},
        relations={"record_slug": {"rel": "record", "resource": "record", "many": False}},
    ),
)
