from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.policy import RecordPolicy
from ...domain.record.record import Record
from ...domain.section.placement_policy import SectionPlacementPolicy
from ...ports.record.record_store import RecordStore
from ...ports.section.section_store import SectionStore


@dataclass(frozen=True, slots=True)
class CreateRecord:
    sections: SectionStore
    records: RecordStore
    actors: ActorPolicy
    record_policy: RecordPolicy
    placement_policy: SectionPlacementPolicy

    def execute(self, section_id: UUID, title: str, kind: str, actor: Actor) -> Record:
        self.actors.allow_contributing(actor)
        section = self.sections.get(section_id)
        record = self.record_policy.create(title, kind)
        placed_section = self.placement_policy.place(section, record)
        self.records.save(record)
        self.sections.save(placed_section)
        return record
