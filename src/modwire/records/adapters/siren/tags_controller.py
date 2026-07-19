from typing import Any

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...domain.collaboration.invalid import InvalidActor
from ...use_cases.tag.create_tag import CreateTag
from ...use_cases.tag.list_tags import ListTags
from ..http.schemas.tag_input import TagInput
from .contract import CREATE_TAG_OPERATION, LIST_TAGS_OPERATION, TAG_COLLECTION_ROUTE, TAG_RESOURCE_NAME
from .request_validation import validated_siren_actor


@api_controller(TAG_COLLECTION_ROUTE, tags=["records"])
class TagsSirenController(ControllerBase):
    @route.get("", response=dict, operation_id=LIST_TAGS_OPERATION)
    def list_tags(self, request: Any):
        tags = DjangoRequest.resolve(request, ListTags).execute()
        document = project_siren(request).collection(
            SirenCollectionRequest(
                resource_name=TAG_RESOURCE_NAME,
                items=tuple({"id": str(tag.identifier), "name": tag.name} for tag in tags),
                collection_operation_ids=(LIST_TAGS_OPERATION, CREATE_TAG_OPERATION),
                item_operation_ids=(),
                path_values={},
            )
        )
        return siren_response(document)

    @route.post("", response=dict, operation_id=CREATE_TAG_OPERATION)
    def create_tag(self, request: Any, payload: TagInput):
        try:
            DjangoRequest.resolve(request, CreateTag).execute(payload.name, validated_siren_actor(request))
        except InvalidActor as error:
            raise HttpError(422, str(error)) from error
        return self.list_tags(request)
