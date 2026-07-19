from typing import Any

from modwire_hex.django import DjangoRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.tag.create_tag import CreateTag
from ...use_cases.tag.list_tags import ListTags
from ...domain.collaboration.invalid import InvalidActor
from ...domain.collaboration.policy import ActorPolicy
from .actor_headers import ActorHeaders
from .schemas.tag_input import TagInput
from .schemas.tag_output import TagOutput


@api_controller("/tags", tags=["records"])
class TagsController(ControllerBase):
    @route.get("", response={200: list[TagOutput]}, operation_id="list_tags")
    def list_tags(self, request: Any) -> tuple[int, list[TagOutput]]:
        tags = DjangoRequest.resolve(request, ListTags).execute()
        return 200, [TagOutput(id=str(tag.identifier), name=tag.name) for tag in tags]

    @route.post("", response={201: TagOutput}, operation_id="create_tag")
    def create(self, request: Any, payload: TagInput) -> tuple[int, TagOutput]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            tag = DjangoRequest.resolve(request, CreateTag).execute(payload.name, actor)
        except InvalidActor as error:
            raise HttpError(422, str(error)) from error
        return 201, TagOutput(id=str(tag.identifier), name=tag.name)
