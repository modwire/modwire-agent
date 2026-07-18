from typing import Annotated

from ninja_extra import route
from ninja_extra.controllers import ControllerBase, api_controller
from wireup import Inject
from wireup.integration.django import inject

from ...services.api_key import ApiKeyService
from .schemas import ApiKeyCreatedOut, ApiKeyIn


@api_controller("/api_keys", tags=["API Keys"])
class ApiKeyController(ControllerBase):
    @route.post("", response=ApiKeyCreatedOut, operation_id="create_api_key", summary="Generate an API key.")
    @inject
    def create(self, data: ApiKeyIn, service: Annotated[ApiKeyService, Inject()]):
        key, secret = service.generate(data.name)
        return {
            "id": key.id,
            "name": key.name,
            "created_at": key.created_at,
            "updated_at": key.updated_at,
            "key": secret,
        }
