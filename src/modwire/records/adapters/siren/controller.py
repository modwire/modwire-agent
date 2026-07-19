from typing import Annotated, Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest, SirenEntityRequest
from ninja import Query
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...domain.collaboration.invalid import InvalidActor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.invalid import InvalidRecord
from ...domain.section.invalid import InvalidSection
from ...use_cases.proposal.propose_content import ProposeContent
from ...use_cases.record.build_knowledge_route import BuildKnowledgeRoute
from ...use_cases.record.create_record import CreateRecord
from ...use_cases.record.get_record_details import GetRecordDetails
from ...use_cases.record.publish_record import PublishRecord
from ...use_cases.record.replace_content import ReplaceContent
from ...use_cases.section.create_section import CreateSection
from ...use_cases.section.get_section_details import GetSectionDetails
from ...use_cases.section.list_sections import ListSections
from ...use_cases.section.reorder_section import ReorderSection
from ...use_cases.tag.assign_tags import AssignTags
from ...use_cases.tag.create_tag import CreateTag
from ...use_cases.tag.list_tags import ListTags
from ..http.actor_headers import ActorHeaders
from ..http.schemas.content_input import ContentInput
from ..http.schemas.record_input import RecordInput
from ..http.schemas.section_input import SectionInput
from ..http.schemas.section_placements_input import SectionPlacementsInput
from ..http.schemas.tag_assignment_input import TagAssignmentInput
from ..http.schemas.tag_input import TagInput
from .contract import (
    COLLECTION_ROUTE,
    ENTITY_ROUTE,
    GET_OPERATION,
    IDENTIFIER_PARAMETER,
    LIST_OPERATION,
    ASSIGN_TAGS_OPERATION,
    REPLACE_CONTENT_OPERATION,
    PROPOSE_CONTENT_OPERATION,
    PUBLISH_OPERATION,
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
                operation_ids=(GET_OPERATION, ASSIGN_TAGS_OPERATION, REPLACE_CONTENT_OPERATION, PROPOSE_CONTENT_OPERATION, PUBLISH_OPERATION),
                path_values={IDENTIFIER_PARAMETER: record.identifier},
                entities=(),
            )
        )
        return siren_response(document)

    @route.put(ENTITY_ROUTE + "/tags", response=dict, operation_id=ASSIGN_TAGS_OPERATION)
    def assign_tags(self, request: Any, record_id: UUID, payload: TagAssignmentInput):
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            DjangoRequest.resolve(request, AssignTags).execute(record_id, payload.tag_ids, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return self._record_document(request, record_id)

    @route.put(ENTITY_ROUTE + "/content", response=dict, operation_id=REPLACE_CONTENT_OPERATION)
    def replace_content(self, request: Any, record_id: UUID, payload: ContentInput):
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            DjangoRequest.resolve(request, ReplaceContent).execute(record_id, payload.markdown, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return self._record_document(request, record_id)

    @route.post(ENTITY_ROUTE + "/content-proposals", response=dict, operation_id=PROPOSE_CONTENT_OPERATION)
    def propose_content(self, request: Any, record_id: UUID, payload: ContentInput):
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            DjangoRequest.resolve(request, ProposeContent).execute(record_id, payload.markdown, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return self._record_document(request, record_id)

    @route.post(ENTITY_ROUTE + "/publish", response=dict, operation_id=PUBLISH_OPERATION)
    def publish(self, request: Any, record_id: UUID):
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            DjangoRequest.resolve(request, PublishRecord).execute(record_id, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return self._record_document(request, record_id)

    @staticmethod
    def _record_document(request: Any, record_id: UUID):
        record = DjangoRequest.resolve(request, GetRecordDetails).execute(record_id)
        return siren_response(
            project_siren(request).document(
                SirenEntityRequest(
                    resource_name=RESOURCE_NAME,
                    properties={"id": str(record.identifier), "title": record.title, "kind": record.kind, "status": record.status, "tags": list(record.tag_names)},
                    operation_ids=(GET_OPERATION, ASSIGN_TAGS_OPERATION, REPLACE_CONTENT_OPERATION, PROPOSE_CONTENT_OPERATION, PUBLISH_OPERATION),
                    path_values={IDENTIFIER_PARAMETER: record.identifier},
                    entities=(),
                )
            )
        )
