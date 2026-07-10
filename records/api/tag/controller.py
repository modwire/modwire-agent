from typing import Annotated

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from records.api.errors import validation_error
from shared.api.types import Slug

from ...services.tag import TagService
from .schemas import TagIn, TagOut, TagPatchIn


@api_controller("/tags", tags=["Tags"])
class TagController(ControllerBase):
    @route.get(
        "",
        response=list[TagOut],
        operation_id="list_tags",
        summary="List tags.",
    )
    @inject
    def list(self, service: Annotated[TagService, Inject()]):
        return service.list()

    @route.get(
        "/{slug}",
        response=TagOut,
        operation_id="get_tag",
        summary="Get tag.",
    )
    @inject
    def get(self, slug: Slug, service: Annotated[TagService, Inject()]):
        return service.get(slug)

    @route.post(
        "",
        response=TagOut,
        operation_id="create_tag",
        summary="Create tag.",
    )
    @inject
    def create(self, data: TagIn, service: Annotated[TagService, Inject()]):
        try:
            return service.create(**data.model_dump())
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.put(
        "/{slug}",
        response=TagOut,
        operation_id="update_tag",
        summary="Update tag.",
    )
    @inject
    def update(
        self,
        slug: Slug,
        data: TagIn,
        service: Annotated[TagService, Inject()],
    ):
        try:
            return service.update(slug, **data.model_dump())
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.patch(
        "/{slug}",
        response=TagOut,
        operation_id="partial_update_tag",
        summary="Partially update tag.",
    )
    @inject
    def partial_update(
        self,
        slug: Slug,
        data: TagPatchIn,
        service: Annotated[TagService, Inject()],
    ):
        try:
            return service.update(slug, **data.model_dump(exclude_unset=True, warnings=False))
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.delete(
        "/{slug}",
        response={204: None},
        operation_id="delete_tag",
        summary="Delete tag.",
    )
    @inject
    def delete(self, slug: Slug, service: Annotated[TagService, Inject()]):
        service.delete(slug)
        return Status(204, None)
