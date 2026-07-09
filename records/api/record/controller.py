from typing import Annotated

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja import Query, Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from records.api.errors import validation_error

from ...services.record import RecordService
from .schemas import RecordIn, RecordOut, RecordPatchIn, RecordSummaryOut, SearchIn, SearchOut


@api_controller("/records", tags=["Records"])
class RecordController(ControllerBase):
    @route.get(
        "",
        response=list[RecordSummaryOut],
        operation_id="list_records",
        summary="List records.",
    )
    @inject
    def list(
        self,
        service: Annotated[RecordService, Inject()],
        limit: int = Query(..., ge=1, le=200),
        offset: int = Query(..., ge=0),
        section_slugs: list[str] = Query(...),
        tag: list[str] = Query(...),
    ):
        return service.list(limit=limit, offset=offset, section_slugs=section_slugs, tag_slugs=tag)

    @route.get(
        "/{path:record_slug}",
        response=RecordOut,
        operation_id="get_record",
        summary="Get record.",
    )
    @inject
    def get(self, record_slug: str, service: Annotated[RecordService, Inject()]):
        return service.get(record_slug)

    @route.post(
        "",
        response=RecordOut,
        operation_id="create_record",
        summary="Create record.",
    )
    @inject
    def create(self, data: RecordIn, service: Annotated[RecordService, Inject()]):
        try:
            return service.create(**data.model_dump())
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.put(
        "/{path:record_slug}",
        response=RecordOut,
        operation_id="update_record",
        summary="Update record.",
    )
    @inject
    def update(
        self,
        record_slug: str,
        data: RecordIn,
        service: Annotated[RecordService, Inject()],
    ):
        try:
            return service.update(record_slug, **data.model_dump())
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.patch(
        "/{path:record_slug}",
        response=RecordOut,
        operation_id="partial_update_record",
        summary="Partially update record.",
    )
    @inject
    def partial_update(
        self,
        record_slug: str,
        data: RecordPatchIn,
        service: Annotated[RecordService, Inject()],
    ):
        try:
            return service.update(record_slug, **data.model_dump(exclude_unset=True))
        except (ValidationError, IntegrityError) as error:
            raise validation_error(error) from error

    @route.delete(
        "/{path:record_slug}",
        response={204: None},
        operation_id="delete_record",
        summary="Delete record.",
    )
    @inject
    def delete(self, record_slug: str, service: Annotated[RecordService, Inject()]):
        service.delete(record_slug)
        return Status(204, None)

    @route.post(
        "/search",
        response=SearchOut,
        operation_id="search_records",
        summary="Search records and sections.",
    )
    @inject
    def search(self, data: SearchIn, service: Annotated[RecordService, Inject()]):
        results = service.search(**data.model_dump())
        return {"results": [result.__dict__ for result in results]}
