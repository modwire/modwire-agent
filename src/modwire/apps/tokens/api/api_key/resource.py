from modwire.apps.tokens.services.api_key import ApiKeyService
from modwire.shared.api.hypermedia import CrudResource, ResourceSpec

from .schemas import ApiKeyIn, ApiKeyOut, ApiKeyPatchIn

api_key = CrudResource(
    name="api_key",
    collection_path="/api/api_keys",
    entity_path="/api/api_keys/{api_key_id}",
    path_parameter="api_key_id",
    path_parameter_type=int,
    in_schema=ApiKeyIn,
    out_schema=ApiKeyOut,
    patch_schema=ApiKeyPatchIn,
    service=ApiKeyService,
    tags=("ApiKeys",),
    summaries={
        "list": "List API keys.",
        "get": "Get an API key.",
        "create": "Generate an API key.",
        "update": "Update an API key.",
        "partial_update": "Rename an API key.",
        "delete": "Delete an API key.",
    },
    validation_error=lambda error: error,
    methods=("list", "get", "partial_update", "delete"),
    list_operation_name="api_keys",
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="api_key",
        path="/api/api_keys/{api_key_id}",
        resource_class="api-key",
        identifier="id",
        path_parameters={"api_key_id": "id"},
        relations={},
    ),
)
