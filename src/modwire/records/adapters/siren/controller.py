from typing import Annotated, Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest, SirenEntityRequest
from ninja import Query
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...use_cases.record.build_knowledge_route import BuildKnowledgeRoute
from ...use_cases.record.get_record_details import GetRecordDetails
from .contract import (
    COLLECTION_ROUTE,
    ENTITY_ROUTE,
    GET_OPERATION,
    IDENTIFIER_PARAMETER,
    LIST_OPERATION,
    RESOURCE_NAME,
)


@api_controller(COLLECTION_ROUTE, tags=["records"])
class RecordsSirenController(ControllerBase):
    @route.get("", response=dict, operation_id=LIST_OPERATION)
    def list_records(self, request: Any, tag: Annotated[list[str], Query(...)]) -> Any:
        records = DjangoRequest.resolve(request, BuildKnowledgeRoute).execute(tag)
        document = project_siren(request).collection(
            SirenCollectionRequest(
                resource_name=RESOURCE_NAME,
                items=tuple(
                    {"id": str(record.identifier), "title": record.title, "reason": f"tag: {record.matched_tag}"}
                    for record in records
                ),
                collection_operation_ids=(LIST_OPERATION,),
                item_operation_ids=(GET_OPERATION,),
                path_values={},
                query=tuple(("tag", value) for value in tag),
            )
        )
        return siren_response(document)

    @route.get(ENTITY_ROUTE, response=dict, operation_id=GET_OPERATION)
    def get_record(self, request: Any, record_id: UUID) -> Any:
        try:
            record = DjangoRequest.resolve(request, GetRecordDetails).execute(record_id)
        except LookupError as error:
            raise HttpError(404, str(error)) from error
        document = project_siren(request).document(
            SirenEntityRequest(
                resource_name=RESOURCE_NAME,
                properties={
                    "id": str(record.identifier),
                    "title": record.title,
                    "kind": record.kind,
                    "status": record.status,
                    "tags": list(record.tag_names),
                },
                operation_ids=(GET_OPERATION,),
                path_values={IDENTIFIER_PARAMETER: record.identifier},
                entities=(),
            )
        )
        return siren_response(document)
