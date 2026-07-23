from typing import Annotated, Any
from uuid import UUID

from django.http import HttpResponse
from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest, SirenEntityRequest
from ninja import Query
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...domain.collaboration.invalid import InvalidActor
from ...domain.record.invalid import InvalidRecord
from ...use_cases.proposal.list_content_proposals import ListContentProposals
from ...use_cases.proposal.propose_content import ProposeContent
from ...use_cases.record.archive_record import ArchiveRecord
from ...use_cases.record.build_knowledge_route import BuildKnowledgeRoute
from ...use_cases.record.get_record_details import GetRecordDetails
from ...use_cases.record.list_content_revisions import ListContentRevisions
from ...use_cases.record.publish_record import PublishRecord
from ...use_cases.record.rename_record import RenameRecord
from ...use_cases.record.replace_content import ReplaceContent
from ...use_cases.tag.assign_tags import AssignTags
from ..http.schemas.content_input import ContentInput
from ..http.schemas.record_title_input import RecordTitleInput
from ..http.schemas.tag_assignment_input import TagAssignmentInput
from .contract import (
    ARCHIVE_OPERATION,
    ASSIGN_TAGS_OPERATION,
    COLLECTION_ROUTE,
    ENTITY_ROUTE,
    GET_OPERATION,
    IDENTIFIER_PARAMETER,
    LIST_OPERATION,
    LIST_PROPOSALS_OPERATION,
    LIST_REVISIONS_OPERATION,
    PROPOSAL_RESOURCE_NAME,
    PROPOSE_CONTENT_OPERATION,
    PUBLISH_OPERATION,
    RENAME_OPERATION,
    REPLACE_CONTENT_OPERATION,
    RESOLVE_PROPOSAL_OPERATION,
    RESOURCE_NAME,
    REVISION_RESOURCE_NAME,
)
from .record_document import record_document
from .request_validation import validated_siren_actor


@api_controller(COLLECTION_ROUTE, tags=["records"], auto_import=False)
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
                operation_ids=(
                    GET_OPERATION,
                    ASSIGN_TAGS_OPERATION,
                    REPLACE_CONTENT_OPERATION,
                    PROPOSE_CONTENT_OPERATION,
                    PUBLISH_OPERATION,
                    RENAME_OPERATION,
                    ARCHIVE_OPERATION,
                    LIST_REVISIONS_OPERATION,
                    LIST_PROPOSALS_OPERATION,
                ),
                path_values={IDENTIFIER_PARAMETER: record.identifier},
                entities=(),
            )
        )
        return siren_response(document)

    @route.put(ENTITY_ROUTE + "/tags", response=dict, operation_id=ASSIGN_TAGS_OPERATION)
    def assign_tags(self, request: Any, record_id: UUID, payload: TagAssignmentInput):
        try:
            actor = validated_siren_actor(request)
            DjangoRequest.resolve(request, AssignTags).execute(record_id, payload.tag_ids, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return record_document(request, record_id)

    @route.put(ENTITY_ROUTE + "/content", response=dict, operation_id=REPLACE_CONTENT_OPERATION)
    def replace_content(self, request: Any, record_id: UUID, payload: ContentInput):
        try:
            actor = validated_siren_actor(request)
            DjangoRequest.resolve(request, ReplaceContent).execute(record_id, payload.markdown, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return record_document(request, record_id)

    @route.post(ENTITY_ROUTE + "/content-proposals", response=dict, operation_id=PROPOSE_CONTENT_OPERATION)
    def propose_content(self, request: Any, record_id: UUID, payload: ContentInput):
        try:
            actor = validated_siren_actor(request)
            DjangoRequest.resolve(request, ProposeContent).execute(record_id, payload.markdown, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return record_document(request, record_id)

    @route.post(ENTITY_ROUTE + "/publish", response=dict, operation_id=PUBLISH_OPERATION)
    def publish(self, request: Any, record_id: UUID):
        try:
            actor = validated_siren_actor(request)
            DjangoRequest.resolve(request, PublishRecord).execute(record_id, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return record_document(request, record_id)

    @route.patch(ENTITY_ROUTE, response=dict, operation_id=RENAME_OPERATION)
    def rename(self, request: Any, record_id: UUID, payload: RecordTitleInput):
        try:
            DjangoRequest.resolve(request, RenameRecord).execute(
                record_id,
                payload.title,
                validated_siren_actor(request),
            )
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return record_document(request, record_id)

    @route.delete(ENTITY_ROUTE, response=None, operation_id=ARCHIVE_OPERATION)
    def archive(self, request: Any, record_id: UUID):
        try:
            DjangoRequest.resolve(request, ArchiveRecord).execute(record_id, validated_siren_actor(request))
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return HttpResponse(status=204)

    @route.get(ENTITY_ROUTE + "/content-revisions", response=dict, operation_id=LIST_REVISIONS_OPERATION)
    def list_revisions(self, request: Any, record_id: UUID):
        revisions = DjangoRequest.resolve(request, ListContentRevisions).execute(record_id)
        document = project_siren(request).collection(
            SirenCollectionRequest(
                resource_name=REVISION_RESOURCE_NAME,
                items=tuple(
                    {
                        "id": str(item.identifier),
                        "actor_id": item.actor.identifier,
                        "actor_type": item.actor.kind,
                        "markdown": item.markdown,
                        "schema_version": item.schema_version,
                    }
                    for item in revisions
                ),
                collection_operation_ids=(LIST_REVISIONS_OPERATION,),
                item_operation_ids=(),
                path_values={IDENTIFIER_PARAMETER: record_id},
            )
        )
        return siren_response(document)

    @route.get(ENTITY_ROUTE + "/content-proposals", response=dict, operation_id=LIST_PROPOSALS_OPERATION)
    def list_proposals(self, request: Any, record_id: UUID):
        try:
            proposals = DjangoRequest.resolve(request, ListContentProposals).execute(record_id)
        except LookupError as error:
            raise HttpError(404, str(error)) from error
        document = project_siren(request).collection(
            SirenCollectionRequest(
                resource_name=PROPOSAL_RESOURCE_NAME,
                items=tuple(
                    {
                        "id": str(item.identifier),
                        "markdown": item.markdown,
                        "proposed_by_id": item.proposed_by.identifier,
                        "proposed_by_type": item.proposed_by.kind,
                        "status": item.status,
                    }
                    for item in proposals
                ),
                collection_operation_ids=(LIST_PROPOSALS_OPERATION,),
                item_operation_ids=(RESOLVE_PROPOSAL_OPERATION,),
                path_values={IDENTIFIER_PARAMETER: record_id},
            )
        )
        return siren_response(document)
