from dataclasses import dataclass
from uuid import UUID

from ..domain.collaboration.actor import Actor
from ..domain.section.placement_policy import SectionPlacementPolicy
from ..domain.section.section import Section
from ..ports.outbound import SectionStore


@dataclass(frozen=True, slots=True)
class ReorderSection:
    sections: SectionStore
    policy: SectionPlacementPolicy

    def execute(self, section_id: UUID, record_ids: list[UUID], actor: Actor) -> Section:
        reordered = self.policy.reorder(self.sections.get(section_id), record_ids, actor)
        self.sections.save(reordered)
        return reordered
