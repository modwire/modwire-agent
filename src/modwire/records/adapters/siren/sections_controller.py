from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest, SirenEntityRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...domain.collaboration.invalid import InvalidActor
from ...domain.section.invalid import InvalidSection
from ...use_cases.record.create_record import CreateRecord
from ...use_cases.section.create_section import CreateSection
from ...use_cases.section.get_section_details import GetSectionDetails
from ...use_cases.section.list_sections import ListSections
from ...use_cases.section.reorder_section import ReorderSection
from ..http.schemas.record_input import RecordInput
from ..http.schemas.section_input import SectionInput
from ..http.schemas.section_placements_input import SectionPlacementsInput
from .contract import (
    CREATE_SECTION_OPERATION,
    CREATE_SECTION_RECORD_OPERATION,
    GET_SECTION_OPERATION,
    LIST_SECTIONS_OPERATION,
    REPLACE_SECTION_PLACEMENTS_OPERATION,
    SECTION_COLLECTION_ROUTE,
    SECTION_IDENTIFIER_PARAMETER,
    SECTION_RESOURCE_NAME,
)
from .record_document import record_document
from .request_validation import validated_siren_actor


@api_controller(SECTION_COLLECTION_ROUTE, tags=["records"])
class SectionsSirenController(ControllerBase):
    @route.get("", response=dict, operation_id=LIST_SECTIONS_OPERATION)
    def list_sections(self, request: Any):
        sections = DjangoRequest.resolve(request, ListSections).execute()
        document = project_siren(request).collection(
            SirenCollectionRequest(
                resource_name=SECTION_RESOURCE_NAME,
                items=tuple(
                    {"id": str(item.identifier), "title": item.title, "allowed_kinds": list(item.allowed_kinds)}
                    for item in sections
                ),
                collection_operation_ids=(LIST_SECTIONS_OPERATION, CREATE_SECTION_OPERATION),
                item_operation_ids=(
                    GET_SECTION_OPERATION,
                    REPLACE_SECTION_PLACEMENTS_OPERATION,
                    CREATE_SECTION_RECORD_OPERATION,
                ),
                path_values={},
            )
        )
        return siren_response(document)

    @route.post("", response=dict, operation_id=CREATE_SECTION_OPERATION)
    def create_section(self, request: Any, payload: SectionInput):
        try:
            section = DjangoRequest.resolve(request, CreateSection).execute(
                payload.title,
                payload.allowed_kinds,
                validated_siren_actor(request),
            )
        except InvalidActor as error:
            raise HttpError(422, str(error)) from error
        return self._document(request, section.identifier)

    @route.get("/{section_id}", response=dict, operation_id=GET_SECTION_OPERATION)
    def get_section(self, request: Any, section_id: UUID):
        return self._document(request, section_id)

    @route.put("/{section_id}/placements", response=dict, operation_id=REPLACE_SECTION_PLACEMENTS_OPERATION)
    def replace_placements(self, request: Any, section_id: UUID, payload: SectionPlacementsInput):
        try:
            DjangoRequest.resolve(request, ReorderSection).execute(
                section_id,
                payload.record_ids,
                validated_siren_actor(request),
            )
        except (InvalidActor, InvalidSection) as error:
            raise HttpError(422, str(error)) from error
        return self._document(request, section_id)

    @route.post("/{section_id}/records", response=dict, operation_id=CREATE_SECTION_RECORD_OPERATION)
    def create_record(self, request: Any, section_id: UUID, payload: RecordInput):
        try:
            record = DjangoRequest.resolve(request, CreateRecord).execute(
                section_id,
                payload.title,
                payload.kind,
                validated_siren_actor(request),
            )
        except (InvalidActor, InvalidSection) as error:
            raise HttpError(422, str(error)) from error
        return record_document(request, record.identifier)

    @staticmethod
    def _document(request: Any, section_id: UUID):
        section = DjangoRequest.resolve(request, GetSectionDetails).execute(section_id)
        document = project_siren(request).document(
            SirenEntityRequest(
                resource_name=SECTION_RESOURCE_NAME,
                properties={
                    "id": str(section.identifier),
                    "title": section.title,
                    "allowed_kinds": list(section.allowed_kinds),
                    "records": [
                        {
                            "id": str(item.identifier),
                            "title": item.title,
                            "kind": item.kind,
                            "status": item.status,
                        }
                        for item in section.records
                    ],
                },
                operation_ids=(
                    GET_SECTION_OPERATION,
                    REPLACE_SECTION_PLACEMENTS_OPERATION,
                    CREATE_SECTION_RECORD_OPERATION,
                ),
                path_values={SECTION_IDENTIFIER_PARAMETER: section.identifier},
                entities=(),
            )
        )
        return siren_response(document)
