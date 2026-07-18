from typing import Annotated

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from modwire_siren import siren_resource
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from modwire.apps.records.api.errors import validation_error

from ...services.content import ContentService
from .schemas import ContentIn, ContentOut, ContentPatchIn


def _content_out(content):
    return {
        "id": content.id,
        "record_slug": content.record_id,
        "position": content.position,
        "role": content.role,
        "content": content.content,
        "language": content.language,
        "metadata": content.metadata,
    }


@siren_resource(
    name="content",
    path="/api/contents/{content_id}",
    class_="content",
    identifier="id",
    path_parameters={"content_id": "id"},
    relations={"record_slug": {"rel": "record", "resource": "record", "many": False}},
)
@api_controller("/contents", tags=["Contents"])
class ContentController(ControllerBase):
    @route.get(
        "",
        response=list[ContentOut],
        operation_id="list_contents",
        summary="List contents.",
    )
    @inject
    def list(self, service: Annotated[ContentService, Inject()]):
        return [_content_out(content) for content in service.list()]

    @route.get(
        "/{content_id}",
        response=ContentOut,
        operation_id="get_content",
        summary="Get content.",
    )
    @inject
    def get(self, content_id: int, service: Annotated[ContentService, Inject()]):
        return _content_out(service.get(content_id))

    @route.post(
        "",
        response=ContentOut,
        operation_id="create_content",
        summary="Create content.",
    )
    @inject
    def create(self, data: ContentIn, service: Annotated[ContentService, Inject()]):
        try:
            return _content_out(service.create(**data.model_dump()))
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.put(
        "/{content_id}",
        response=ContentOut,
        operation_id="update_content",
        summary="Update content.",
    )
    @inject
    def update(
        self,
        content_id: int,
        data: ContentIn,
        service: Annotated[ContentService, Inject()],
    ):
        try:
            return _content_out(service.update(content_id, **data.model_dump()))
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.patch(
        "/{content_id}",
        response=ContentOut,
        operation_id="partial_update_content",
        summary="Partially update content.",
    )
    @inject
    def partial_update(
        self,
        content_id: int,
        data: ContentPatchIn,
        service: Annotated[ContentService, Inject()],
    ):
        try:
            return _content_out(
                service.update(content_id, **data.model_dump(exclude_unset=True, warnings=False))
            )
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.delete(
        "/{content_id}",
        response={204: None},
        operation_id="delete_content",
        summary="Delete content.",
    )
    @inject
    def delete(self, content_id: int, service: Annotated[ContentService, Inject()]):
        service.delete(content_id)
        return Status(204, None)
