from typing import Annotated, Any

from modwire_hex.django import DjangoRequest
from ninja import Query
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.record.search_records import SearchRecords
from .schemas.search_result_output import SearchResultOutput


@api_controller("/records/search", tags=["records"])
class SearchController(ControllerBase):
    @route.get("/semantic", response={200: list[SearchResultOutput]}, operation_id="semantic_record_search")
    def semantic(self, request: Any, q: Annotated[str, Query(...)]) -> tuple[int, list[SearchResultOutput]]:
        results = DjangoRequest.resolve(request, SearchRecords).semantic(q)
        return 200, [
            SearchResultOutput(id=str(result.identifier), title=result.title, reason=result.reason)
            for result in results
        ]

    @route.get("/text", response={200: list[SearchResultOutput]}, operation_id="text_record_search")
    def text(self, request: Any, q: Annotated[str, Query(...)]) -> tuple[int, list[SearchResultOutput]]:
        results = DjangoRequest.resolve(request, SearchRecords).text(q)
        return 200, [
            SearchResultOutput(id=str(result.identifier), title=result.title, reason=result.reason)
            for result in results
        ]
