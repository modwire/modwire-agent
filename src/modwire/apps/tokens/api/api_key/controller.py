from ninja_extra import route

from modwire.shared.api.hypermedia import ResourceController

from .resource import api_key
from .schemas import ApiKeyCreatedOut, ApiKeyIn


@ResourceController(api_key)
class ApiKeyController:
    @route.post("", response=ApiKeyCreatedOut, operation_id="create_api_key", summary="Generate an API key.")
    def create(self, data: ApiKeyIn):
        key, secret = api_key.service().generate(data.name)
        return {
            "id": key.id,
            "name": key.name,
            "created_at": key.created_at,
            "updated_at": key.updated_at,
            "key": secret,
        }
