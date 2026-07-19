from dataclasses import dataclass
from uuid import UUID

from ..record.kind import RecordKind
from .placement import SectionPlacement


@dataclass(frozen=True, slots=True)
class Section:
    identifier: UUID
    title: str
    allowed_kinds: tuple[RecordKind, ...]
    placements: tuple[SectionPlacement, ...]

    def place(self, record_id: UUID) -> Section:
        placement = SectionPlacement(record_id=record_id, position=len(self.placements))
        return Section(self.identifier, self.title, self.allowed_kinds, (*self.placements, placement))

    def reorder(self, record_ids: list[UUID]) -> Section:
        placements = tuple(SectionPlacement(record_id=record_id, position=position) for position, record_id in enumerate(record_ids))
        return Section(self.identifier, self.title, self.allowed_kinds, placements)
