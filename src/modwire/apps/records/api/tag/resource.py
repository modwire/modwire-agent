from modwire.apps.records.api.errors import validation_error
from modwire.apps.records.services.tag import TagService
from modwire.shared.api.hypermedia import CrudResource, ResourceSpec
from modwire.shared.api.types import Slug

from .schemas import TagIn, TagOut, TagPatchIn

tag = CrudResource(
    name="tag",
    collection_path="/api/tags",
    entity_path="/api/tags/{slug}",
    path_parameter="slug",
    path_parameter_type=Slug,
    in_schema=TagIn,
    out_schema=TagOut,
    patch_schema=TagPatchIn,
    service=TagService,
    tags=("Tags",),
    summaries={
        "list": "List tags.",
        "get": "Get tag.",
        "create": "Create tag.",
        "update": "Update tag.",
        "partial_update": "Partially update tag.",
        "delete": "Delete tag.",
    },
    validation_error=validation_error,
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="tag",
        path="/api/tags/{slug}",
        resource_class="tag",
        identifier="slug",
        path_parameters={"slug": "slug"},
        relations={},
    ),
)
