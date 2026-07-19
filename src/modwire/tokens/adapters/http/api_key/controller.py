from modwire_hex.django import DjangoRequest
from ninja import Status
from ninja.errors import HttpError
from ninja_extra import route
from ninja_extra.controllers import ControllerBase, api_controller

from ....use_cases.issue_api_key import IssueApiKey
from .schemas import ApiKeyCreatedOut, ApiKeyIn


@api_controller("/api_keys", tags=["API Keys"])
class ApiKeyController(ControllerBase):
    @route.post("", response={201: ApiKeyCreatedOut}, operation_id="create_api_key", summary="Generate an API key.")
    def create(self, request, data: ApiKeyIn):
        service = DjangoRequest.resolve(request, IssueApiKey)
        try:
            key, secret = service.execute(data.name)
        except ValueError as error:
            raise HttpError(422, str(error)) from error
        return Status(
            201,
            {
                "id": key.identifier,
                "name": key.name,
                "created_at": key.created_at,
                "updated_at": key.updated_at,
                "key": secret,
            },
        )
