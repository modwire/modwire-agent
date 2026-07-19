from typing import Annotated, Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja import Query
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from ...domain.collaboration.invalid import InvalidActor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.invalid import InvalidRecord
from ...use_cases.record.replace_content import ReplaceContent
from ...use_cases.record.publish_record import PublishRecord
from ...use_cases.tag.assign_tags import AssignTags
from ...use_cases.record.build_knowledge_route import BuildKnowledgeRoute
from ...use_cases.record.list_content_revisions import ListContentRevisions
from ...use_cases.proposal.propose_content import ProposeContent
from ...use_cases.record.get_record_details import GetRecordDetails
from ...use_cases.proposal.list_content_proposals import ListContentProposals
from ...use_cases.record.rename_record import RenameRecord
from ...use_cases.record.archive_record import ArchiveRecord
from .schemas.content_input import ContentInput
from .schemas.content_proposal_output import ContentProposalOutput
from .schemas.content_proposal_details_output import ContentProposalDetailsOutput
from .schemas.content_output import ContentOutput
from .schemas.content_revision_output import ContentRevisionOutput
from .schemas.record_details_output import RecordDetailsOutput
from .schemas.record_output import RecordOutput
from .schemas.record_title_input import RecordTitleInput
from .schemas.routed_record_output import RoutedRecordOutput
from .schemas.tag_assignment_input import TagAssignmentInput
from .actor_headers import ActorHeaders


@api_controller("/records", tags=["records"])
class RecordsController(ControllerBase):
    @route.delete("/{record_id}", response={204: None})
    def archive(self, request: Any, record_id: UUID) -> tuple[int, None]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            DjangoRequest.resolve(request, ArchiveRecord).execute(record_id, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return 204, None

    @route.patch("/{record_id}", response={200: RecordOutput})
    def rename(self, request: Any, record_id: UUID, payload: RecordTitleInput) -> tuple[int, RecordOutput]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            record = DjangoRequest.resolve(request, RenameRecord).execute(record_id, payload.title, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return 200, RecordOutput(id=str(record.identifier), title=record.title, kind=record.kind, status=record.status)

    @route.get("/{record_id}/content-proposals", response={200: list[ContentProposalDetailsOutput]})
    def list_content_proposals(self, request: Any, record_id: UUID) -> tuple[int, list[ContentProposalDetailsOutput]]:
        try:
            proposals = DjangoRequest.resolve(request, ListContentProposals).execute(record_id)
        except LookupError as error:
            raise HttpError(404, str(error)) from error
        return 200, [ContentProposalDetailsOutput(id=str(proposal.identifier), markdown=proposal.markdown, proposed_by_id=proposal.proposed_by.identifier, proposed_by_type=proposal.proposed_by.kind, status=proposal.status) for proposal in proposals]

    @route.get("/{record_id}", response={200: RecordDetailsOutput})
    def get_details(self, request: Any, record_id: UUID) -> tuple[int, RecordDetailsOutput]:
        try:
            record = DjangoRequest.resolve(request, GetRecordDetails).execute(record_id)
        except LookupError as error:
            raise HttpError(404, str(error)) from error
        return 200, RecordDetailsOutput(id=str(record.identifier), title=record.title, kind=record.kind, status=record.status, tags=list(record.tag_names))

    @route.post("/{record_id}/content-proposals", response={201: ContentProposalOutput})
    def propose_content(self, request: Any, record_id: UUID, payload: ContentInput) -> tuple[int, ContentProposalOutput]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            proposal = DjangoRequest.resolve(request, ProposeContent).execute(record_id, payload.markdown, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return 201, ContentProposalOutput(id=str(proposal.identifier), status=proposal.status)

    @route.get("", response={200: list[RoutedRecordOutput]})
    def list_published(self, request: Any, tag: Annotated[list[str], Query(...)]) -> tuple[int, list[RoutedRecordOutput]]:
        records = DjangoRequest.resolve(request, BuildKnowledgeRoute).execute(tag)
        return 200, [RoutedRecordOutput(id=str(record.identifier), title=record.title, reason=f"tag: {record.matched_tag}") for record in records]

    @route.get("/{record_id}/content-revisions", response={200: list[ContentRevisionOutput]})
    def list_content_revisions(self, request: Any, record_id: UUID) -> tuple[int, list[ContentRevisionOutput]]:
        revisions = DjangoRequest.resolve(request, ListContentRevisions).execute(record_id)
        return 200, [ContentRevisionOutput(id=str(revision.identifier), actor_id=revision.actor.identifier, actor_type=revision.actor.kind, markdown=revision.markdown, schema_version=revision.schema_version) for revision in revisions]

    @route.put("/{record_id}/tags", response={204: None})
    def assign_tags(self, request: Any, record_id: UUID, payload: TagAssignmentInput) -> tuple[int, None]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            DjangoRequest.resolve(request, AssignTags).execute(record_id, payload.tag_ids, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return 204, None

    @route.put("/{record_id}/content", response={200: ContentOutput})
    def replace_content(self, request: Any, record_id: UUID, payload: ContentInput) -> tuple[int, ContentOutput]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            revision = DjangoRequest.resolve(request, ReplaceContent).execute(record_id, payload.markdown, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return 200, ContentOutput(id=str(revision.identifier), schema_version=revision.schema_version)

    @route.post("/{record_id}/publish", response={200: dict[str, str]})
    def publish(self, request: Any, record_id: UUID) -> tuple[int, dict[str, str]]:
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            record = DjangoRequest.resolve(request, PublishRecord).execute(record_id, actor)
        except (InvalidActor, InvalidRecord) as error:
            raise HttpError(422, str(error)) from error
        return 200, {"id": str(record.identifier), "status": record.status}
