from ninja_extra import route

from modwire.shared.api.hypermedia import ResourceController

from .resource import record
from .schemas import SearchIn, SearchOut


@ResourceController(record)
class RecordController:
    @route.post(
        "/search",
        response=SearchOut,
        operation_id="search_records",
        summary="Search records and sections.",
    )
    def search(self, data: SearchIn):
        results = record.service().search(**data.model_dump())
        return {"results": [result.__dict__ for result in results]}
