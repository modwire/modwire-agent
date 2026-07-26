from typing import Annotated, Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja import Query
from ninja_extra import ControllerBase, api_controller, route

from ...domain.collaboration.policy import ActorPolicy
from ...use_cases.archive_record import ArchiveRecord
from ...use_cases.assign_tags import AssignTags
from ...use_cases.build_knowledge_route import BuildKnowledgeRoute
from ...use_cases.create_record import CreateRecord
from ...use_cases.create_section import CreateSection
from ...use_cases.create_tag import CreateTag
from ...use_cases.get_record_details import GetRecordDetails
from ...use_cases.get_section_details import GetSectionDetails
from ...use_cases.list_content_proposals import ListContentProposals
from ...use_cases.list_content_revisions import ListContentRevisions
from ...use_cases.list_sections import ListSections
from ...use_cases.list_tags import ListTags
from ...use_cases.propose_content import ProposeContent
from ...use_cases.publish_record import PublishRecord
from ...use_cases.rename_record import RenameRecord
from ...use_cases.reorder_section import ReorderSection
from ...use_cases.replace_content import ReplaceContent
from ...use_cases.resolve_content_proposal import ResolveContentProposal
from ...use_cases.search_records import SearchRecords
from .schemas import (
    ActorHeaders,
    ContentInput,
    ContentOutput,
    ContentProposalDetailsOutput,
    ContentProposalOutput,
    ContentRevisionOutput,
    ProposalStatusInput,
    RecordDetailsOutput,
    RecordInput,
    RecordOutput,
    RecordTitleInput,
    RoutedRecordOutput,
    SearchResultOutput,
    SectionDetailsOutput,
    SectionInput,
    SectionOutput,
    SectionPlacementsInput,
    SectionPlacementsOutput,
    SectionRecordOutput,
    TagAssignmentInput,
    TagInput,
    TagOutput,
)


@api_controller("/sections", tags=["records"])
class SectionsController(ControllerBase):
    @route.get("", response={200: list[SectionOutput]}, operation_id="list_sections")
    def list_sections(self, request: Any) -> tuple[int, list[SectionOutput]]:
        """List all sections and their allowed record kinds."""
        sections = DjangoRequest.resolve(request, ListSections).execute()
        return 200, [
            SectionOutput(id=str(section.identifier), title=section.title, allowed_kinds=list(section.allowed_kinds))
            for section in sections
        ]

    @route.get("/{section_id}", response={200: SectionDetailsOutput}, operation_id="get_section_details")
    def get_details(self, request: Any, section_id: UUID) -> tuple[int, SectionDetailsOutput]:
        """Return one section with its ordered records."""
        section = DjangoRequest.resolve(request, GetSectionDetails).execute(section_id)
        records = [
            SectionRecordOutput(id=str(record.identifier), title=record.title, kind=record.kind, status=record.status)
            for record in section.records
        ]
        return 200, SectionDetailsOutput(
            id=str(section.identifier), title=section.title, allowed_kinds=list(section.allowed_kinds), records=records
        )

    @route.post("", response={201: SectionOutput}, operation_id="create_section")
    def create(self, request: Any, payload: SectionInput) -> tuple[int, SectionOutput]:
        """Create a section that accepts the supplied record kinds."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        section = DjangoRequest.resolve(request, CreateSection).execute(payload.title, payload.allowed_kinds, actor)
        return 201, SectionOutput(
            id=str(section.identifier), title=section.title, allowed_kinds=[str(kind) for kind in section.allowed_kinds]
        )

    @route.put(
        "/{section_id}/placements", response={200: SectionPlacementsOutput}, operation_id="replace_section_placements"
    )
    def replace_placements(
        self, request: Any, section_id: UUID, payload: SectionPlacementsInput
    ) -> tuple[int, SectionPlacementsOutput]:
        """Replace the complete record order within a section."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        section = DjangoRequest.resolve(request, ReorderSection).execute(section_id, payload.record_ids, actor)
        return 200, SectionPlacementsOutput(record_ids=[str(placement.record_id) for placement in section.placements])

    @route.post("/{section_id}/records", response={201: RecordOutput}, operation_id="create_section_record")
    def create_record(self, request: Any, section_id: UUID, payload: RecordInput) -> tuple[int, RecordOutput]:
        """Create a draft record in a section."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        record = DjangoRequest.resolve(request, CreateRecord).execute(section_id, payload.title, payload.kind, actor)
        return 201, RecordOutput(
            id=str(record.identifier), title=record.title, kind=str(record.kind), status=str(record.status)
        )


@api_controller("/content-proposals", tags=["records"])
class ContentProposalsController(ControllerBase):
    @route.patch("/{proposal_id}", response={200: ContentProposalOutput}, operation_id="resolve_content_proposal")
    def resolve(
        self, request: Any, proposal_id: UUID, payload: ProposalStatusInput
    ) -> tuple[int, ContentProposalOutput]:
        """Accept or reject a pending content proposal."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        proposal = DjangoRequest.resolve(request, ResolveContentProposal).execute(proposal_id, payload.status, actor)
        return 200, ContentProposalOutput(id=str(proposal.identifier), status=proposal.status)


@api_controller("/records", tags=["records"])
class RecordsController(ControllerBase):
    @route.delete("/{record_id}", response={204: None}, operation_id="archive_record")
    def archive(self, request: Any, record_id: UUID) -> tuple[int, None]:
        """Archive a record without deleting its history."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        DjangoRequest.resolve(request, ArchiveRecord).execute(record_id, actor)
        return 204, None

    @route.patch("/{record_id}", response={200: RecordOutput}, operation_id="rename_record")
    def rename(self, request: Any, record_id: UUID, payload: RecordTitleInput) -> tuple[int, RecordOutput]:
        """Rename a record."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        record = DjangoRequest.resolve(request, RenameRecord).execute(record_id, payload.title, actor)
        return 200, RecordOutput(id=str(record.identifier), title=record.title, kind=record.kind, status=record.status)

    @route.get(
        "/{record_id}/content-proposals",
        response={200: list[ContentProposalDetailsOutput]},
        operation_id="list_record_content_proposals",
    )
    def list_content_proposals(self, request: Any, record_id: UUID) -> tuple[int, list[ContentProposalDetailsOutput]]:
        """List pending and resolved content proposals for a record."""
        proposals = DjangoRequest.resolve(request, ListContentProposals).execute(record_id)
        return 200, [
            ContentProposalDetailsOutput(
                id=str(proposal.identifier),
                markdown=proposal.markdown,
                proposed_by_id=proposal.proposed_by.identifier,
                proposed_by_type=proposal.proposed_by.kind,
                status=proposal.status,
            )
            for proposal in proposals
        ]

    @route.get("/{record_id}", response={200: RecordDetailsOutput}, operation_id="get_record_details")
    def get_details(self, request: Any, record_id: UUID) -> tuple[int, RecordDetailsOutput]:
        """Return a record and its normalized tags."""
        record = DjangoRequest.resolve(request, GetRecordDetails).execute(record_id)
        return 200, RecordDetailsOutput(
            id=str(record.identifier),
            title=record.title,
            kind=record.kind,
            status=record.status,
            tags=list(record.tag_names),
        )

    @route.post(
        "/{record_id}/content-proposals", response={201: ContentProposalOutput}, operation_id="propose_record_content"
    )
    def propose_content(
        self, request: Any, record_id: UUID, payload: ContentInput
    ) -> tuple[int, ContentProposalOutput]:
        """Submit an actor-authored content proposal for a record."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        proposal = DjangoRequest.resolve(request, ProposeContent).execute(record_id, payload.markdown, actor)
        return 201, ContentProposalOutput(id=str(proposal.identifier), status=proposal.status)

    @route.get("", response={200: list[RoutedRecordOutput]}, operation_id="list_published_records")
    def list_published(
        self, request: Any, tag: Annotated[list[str] | None, Query()] = None
    ) -> tuple[int, list[RoutedRecordOutput]]:
        """List published records that match all requested tags."""
        records = DjangoRequest.resolve(request, BuildKnowledgeRoute).execute(tag or [])
        return 200, [
            RoutedRecordOutput(
                id=str(record.identifier),
                title=record.title,
                reason=f"tag: {record.matched_tag}" if record.matched_tag else None,
            )
            for record in records
        ]

    @route.get(
        "/{record_id}/content-revisions",
        response={200: list[ContentRevisionOutput]},
        operation_id="list_record_content_revisions",
    )
    def list_content_revisions(self, request: Any, record_id: UUID) -> tuple[int, list[ContentRevisionOutput]]:
        """List the ordered content revisions for a record."""
        revisions = DjangoRequest.resolve(request, ListContentRevisions).execute(record_id)
        return 200, [
            ContentRevisionOutput(
                id=str(revision.identifier),
                actor_id=revision.actor.identifier,
                actor_type=revision.actor.kind,
                markdown=revision.markdown,
                schema_version=revision.schema_version,
            )
            for revision in revisions
        ]

    @route.put("/{record_id}/tags", response={204: None}, operation_id="assign_record_tags")
    def assign_tags(self, request: Any, record_id: UUID, payload: TagAssignmentInput) -> tuple[int, None]:
        """Replace a record's complete tag assignment."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        DjangoRequest.resolve(request, AssignTags).execute(record_id, payload.tag_ids, actor)
        return 204, None

    @route.put("/{record_id}/content", response={200: ContentOutput}, operation_id="replace_record_content")
    def replace_content(self, request: Any, record_id: UUID, payload: ContentInput) -> tuple[int, ContentOutput]:
        """Store a validated content revision for a record."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        revision = DjangoRequest.resolve(request, ReplaceContent).execute(record_id, payload.markdown, actor)
        return 200, ContentOutput(id=str(revision.identifier), schema_version=revision.schema_version)

    @route.post("/{record_id}/publish", response={200: dict[str, str]}, operation_id="publish_record")
    def publish(self, request: Any, record_id: UUID) -> tuple[int, dict[str, str]]:
        """Publish a record with valid content."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        record = DjangoRequest.resolve(request, PublishRecord).execute(record_id, actor)
        return 200, {"id": str(record.identifier), "status": record.status}


@api_controller("/records/search", tags=["records"])
class SearchController(ControllerBase):
    @route.get("/semantic", response={200: list[SearchResultOutput]}, operation_id="semantic_record_search")
    def semantic(self, request: Any, q: Annotated[str, Query(...)]) -> tuple[int, list[SearchResultOutput]]:
        """Find published records by semantic similarity."""
        results = DjangoRequest.resolve(request, SearchRecords).semantic(q)
        return 200, [
            SearchResultOutput(id=str(result.identifier), title=result.title, reason=result.reason)
            for result in results
        ]

    @route.get("/text", response={200: list[SearchResultOutput]}, operation_id="text_record_search")
    def text(self, request: Any, q: Annotated[str, Query(...)]) -> tuple[int, list[SearchResultOutput]]:
        """Find published records by text matching."""
        results = DjangoRequest.resolve(request, SearchRecords).text(q)
        return 200, [
            SearchResultOutput(id=str(result.identifier), title=result.title, reason=result.reason)
            for result in results
        ]


@api_controller("/tags", tags=["records"])
class TagsController(ControllerBase):
    @route.get("", response={200: list[TagOutput]}, operation_id="list_tags")
    def list_tags(self, request: Any) -> tuple[int, list[TagOutput]]:
        """List all record tags."""
        tags = DjangoRequest.resolve(request, ListTags).execute()
        return 200, [TagOutput(id=str(tag.identifier), name=tag.name) for tag in tags]

    @route.post("", response={201: TagOutput}, operation_id="create_tag")
    def create(self, request: Any, payload: TagInput) -> tuple[int, TagOutput]:
        """Create a normalized record tag."""
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        tag = DjangoRequest.resolve(request, CreateTag).execute(payload.name, actor)
        return 201, TagOutput(id=str(tag.identifier), name=tag.name)
