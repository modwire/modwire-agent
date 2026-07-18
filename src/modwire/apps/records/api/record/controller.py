from typing import Annotated

from ninja_extra import route
from ninja_extra.controllers import ControllerBase, api_controller
from wireup import Inject
from wireup.integration.django import inject

from ...services.record import RecordService
from .schemas import SearchIn, SearchOut


@api_controller("/records", tags=["Records"])
class RecordController(ControllerBase):
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
