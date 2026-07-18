from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from modwire.shared.api.hypermedia import siren_resource

from ...services.api_key import ApiKeyService
from .schemas import ApiKeyCreatedOut, ApiKeyIn, ApiKeyOut, ApiKeyPatchIn


@siren_resource(
    name="api_key",
    path="/api/api_keys/{api_key_id}",
    class_="api-key",
    identifier="id",
    path_parameters={"api_key_id": "id"},
    relations={},
)
@api_controller("/api_keys", tags=["ApiKeys"])
class ApiKeyController(ControllerBase):
    @route.get("", response=list[ApiKeyOut], operation_id="list_api_keys", summary="List API keys.")
    @inject
    def list(self, service: Annotated[ApiKeyService, Inject()]):
        return service.list()

    @route.get("/{api_key_id}", response=ApiKeyOut, operation_id="get_api_key", summary="Get an API key.")
    @inject
    def get(self, api_key_id: int, service: Annotated[ApiKeyService, Inject()]):
        return service.get(api_key_id)

    @route.post("", response=ApiKeyCreatedOut, operation_id="create_api_key", summary="Generate an API key.")
    @inject
    def create(self, data: ApiKeyIn, service: Annotated[ApiKeyService, Inject()]):
        api_key, secret = service.generate(data.name)
        return {
            "id": api_key.id,
            "name": api_key.name,
            "created_at": api_key.created_at,
            "updated_at": api_key.updated_at,
            "key": secret,
        }

    @route.patch(
        "/{api_key_id}", response=ApiKeyOut, operation_id="partial_update_api_key", summary="Rename an API key."
    )
    @inject
    def update(self, api_key_id: int, data: ApiKeyPatchIn, service: Annotated[ApiKeyService, Inject()]):
        return service.update(api_key_id, **data.model_dump(exclude_unset=True))

    @route.delete("/{api_key_id}", response={204: None}, operation_id="delete_api_key", summary="Delete an API key.")
    @inject
    def delete(self, api_key_id: int, service: Annotated[ApiKeyService, Inject()]):
        service.delete(api_key_id)
        return Status(204, None)
