from typing import Annotated, Any

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest
from ninja import Query
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...use_cases.record.search_records import SearchRecords
from .contract import COLLECTION_ROUTE, GET_OPERATION, RESOURCE_NAME, SEMANTIC_SEARCH_OPERATION, TEXT_SEARCH_OPERATION


@api_controller(COLLECTION_ROUTE + "/search", tags=["records"], auto_import=False)
class RecordSearchSirenController(ControllerBase):
    @route.get("/text", response=dict, operation_id=TEXT_SEARCH_OPERATION)
    def text(self, request: Any, q: Annotated[str, Query(...)]):
        return self._collection(request, DjangoRequest.resolve(request, SearchRecords).text(q), TEXT_SEARCH_OPERATION, q)

    @route.get("/semantic", response=dict, operation_id=SEMANTIC_SEARCH_OPERATION)
    def semantic(self, request: Any, q: Annotated[str, Query(...)]):
        return self._collection(request, DjangoRequest.resolve(request, SearchRecords).semantic(q), SEMANTIC_SEARCH_OPERATION, q)

    @staticmethod
    def _collection(request: Any, results: list[Any], operation: str, query: str):
        return siren_response(project_siren(request).collection(SirenCollectionRequest(resource_name=RESOURCE_NAME, items=tuple({"id": str(item.identifier), "title": item.title, "reason": item.reason} for item in results), collection_operation_ids=(operation,), item_operation_ids=(GET_OPERATION,), path_values={}, query=(("q", query),))))
