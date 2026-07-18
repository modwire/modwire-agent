from ninja import Query

from modwire.apps.records.api.errors import validation_error
from modwire.apps.records.services.section import SectionService
from modwire.shared.api.hypermedia import CrudResource, QuerySpec, ResourceSpec
from modwire.shared.api.types import Slug

from .schemas import SectionIn, SectionOut, SectionPatchIn

section = CrudResource(
    name="section",
    collection_path="/api/sections",
    entity_path="/api/sections/{slug}",
    path_parameter="slug",
    path_parameter_type=Slug,
    in_schema=SectionIn,
    out_schema=SectionOut,
    patch_schema=SectionPatchIn,
    service=SectionService,
    tags=("Sections",),
    summaries={
        "list": "List sections.",
        "get": "Get section.",
        "create": "Create section.",
        "update": "Update section.",
        "partial_update": "Partially update section.",
        "delete": "Delete section.",
    },
    validation_error=validation_error,
    list_queries=(
        QuerySpec("limit", int, Query(200, ge=1, le=200)),
        QuerySpec("offset", int, Query(0, ge=0)),
        QuerySpec("tag", list[Slug], Query(default_factory=list), service_name="tag_slugs"),
    ),
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="section",
        path="/api/sections/{slug}",
        resource_class="section",
        identifier="slug",
        path_parameters={"slug": "slug"},
        relations={"tag_slugs": {"rel": "tag", "resource": "tag", "many": True}},
    ),
)
