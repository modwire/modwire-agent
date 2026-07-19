from dataclasses import dataclass
from uuid import UUID

from ..collaboration.actor import Actor
from ..collaboration.policy import ActorPolicy
from ..record.record import Record
from .invalid import InvalidSection
from .section import Section


@dataclass(frozen=True, slots=True)
class SectionPlacementPolicy:
    actors: ActorPolicy

    def place(self, section: Section, record: Record) -> Section:
        if record.kind not in section.allowed_kinds:
            raise InvalidSection("Record kind is not allowed by this section.")
        return section.place(record.identifier)

    def reorder(self, section: Section, record_ids: list[UUID], actor: Actor) -> Section:
        self.actors.allow_reordering(actor)
        existing_ids = [placement.record_id for placement in section.placements]
        if len(record_ids) != len(set(record_ids)):
            raise InvalidSection("Section placements cannot contain duplicates.")
        if set(record_ids) != set(existing_ids):
            raise InvalidSection("Section placements must contain exactly its records.")
        return section.reorder(record_ids)
