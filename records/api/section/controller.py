from typing import Annotated

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja import Query, Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from records.api.errors import validation_error
from shared.api_types import Slug

from ...services.section import SectionService
from .schemas import SectionIn, SectionOut, SectionPatchIn


@api_controller("/sections", tags=["Sections"])
class SectionController(ControllerBase):
    @route.get(
        "",
        response=list[SectionOut],
        operation_id="list_sections",
        summary="List sections.",
    )
    @inject
    def list(
        self,
        service: Annotated[SectionService, Inject()],
        limit: int = Query(..., ge=1, le=200),
        offset: int = Query(..., ge=0),
        tag: list[Slug] = Query(...),
    ):
        return service.list(limit=limit, offset=offset, tag_slugs=tag)

    @route.get(
        "/{slug}",
        response=SectionOut,
        operation_id="get_section",
        summary="Get section.",
    )
    @inject
    def get(self, slug: Slug, service: Annotated[SectionService, Inject()]):
        return service.get(slug)

    @route.post(
        "",
        response=SectionOut,
        operation_id="create_section",
        summary="Create section.",
    )
    @inject
    def create(self, data: SectionIn, service: Annotated[SectionService, Inject()]):
        try:
            return service.create(**data.model_dump())
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.put(
        "/{slug}",
        response=SectionOut,
        operation_id="update_section",
        summary="Update section.",
    )
    @inject
    def update(
        self,
        slug: Slug,
        data: SectionIn,
        service: Annotated[SectionService, Inject()],
    ):
        try:
            return service.update(slug, **data.model_dump())
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.patch(
        "/{slug}",
        response=SectionOut,
        operation_id="partial_update_section",
        summary="Partially update section.",
    )
    @inject
    def partial_update(
        self,
        slug: Slug,
        data: SectionPatchIn,
        service: Annotated[SectionService, Inject()],
    ):
        try:
            return service.update(slug, **data.model_dump(exclude_unset=True, warnings=False))
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.delete(
        "/{slug}",
        response={204: None},
        operation_id="delete_section",
        summary="Delete section.",
    )
    @inject
    def delete(self, slug: Slug, service: Annotated[SectionService, Inject()]):
        try:
            service.delete(slug)
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error
        return Status(204, None)
