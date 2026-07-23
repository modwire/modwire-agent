from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...domain.collaboration.policy import ActorPolicy
from ...use_cases.record.create_record import CreateRecord
from ...use_cases.section.create_section import CreateSection
from ...use_cases.section.get_section_details import GetSectionDetails
from ...use_cases.section.list_sections import ListSections
from ...use_cases.section.reorder_section import ReorderSection
from .actor_headers import ActorHeaders
from .schemas.record_input import RecordInput
from .schemas.record_output import RecordOutput
from .schemas.section_details_output import SectionDetailsOutput
from .schemas.section_input import SectionInput
from .schemas.section_output import SectionOutput
from .schemas.section_placements_input import SectionPlacementsInput
from .schemas.section_placements_output import SectionPlacementsOutput
from .schemas.section_record_output import SectionRecordOutput


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
