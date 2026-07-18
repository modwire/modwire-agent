from ninja import Query

from modwire.apps.records.api.errors import validation_error
from modwire.apps.records.services.record import RecordService
from modwire.shared.api.hypermedia import CrudResource, QuerySpec, ResourceSpec
from modwire.shared.api.types import RecordSlug, Slug

from .schemas import RecordIn, RecordOut, RecordPatchIn, RecordSummaryOut

record = CrudResource(
    name="record",
    collection_path="/api/records",
    entity_path="/api/records/{record_slug}",
    path_parameter="record_slug",
    path_parameter_type=RecordSlug,
    in_schema=RecordIn,
    out_schema=RecordOut,
    patch_schema=RecordPatchIn,
    service=RecordService,
    tags=("Records",),
    summaries={
        "list": "List records.",
        "get": "Get record.",
        "create": "Create record.",
        "update": "Update record.",
        "partial_update": "Partially update record.",
        "delete": "Delete record.",
    },
    validation_error=validation_error,
    list_schema=RecordSummaryOut,
    list_queries=(
        QuerySpec("limit", int, Query(200, ge=1, le=200)),
        QuerySpec("offset", int, Query(0, ge=0)),
        QuerySpec("section_slugs", list[Slug], Query(default_factory=list)),
        QuerySpec("tag", list[Slug], Query(default_factory=list), service_name="tag_slugs"),
    ),
    route_path="/{path:record_slug}",
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="record",
        path="/api/records/{record_slug}",
        resource_class="record",
        identifier="slug",
        path_parameters={"record_slug": "slug"},
        relations={
            "section_slug": {"rel": "section", "resource": "section", "many": False},
            "tag_slugs": {"rel": "tag", "resource": "tag", "many": True},
        },
        collection_operations=("search_records",),
    ),
    ResourceSpec(
        name="record_search",
        path="/api/records/search",
        resource_class="record-search",
        identifier="query",
        path_parameters={},
        relations={},
        singleton=True,
        root_visible=False,
    ),
)
