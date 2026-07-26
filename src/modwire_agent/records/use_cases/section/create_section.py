from dataclasses import dataclass

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.section.policy import SectionPolicy
from ...domain.section.section import Section
from ...ports.outbound import SectionStore


@dataclass(frozen=True, slots=True)
class CreateSection:
    sections: SectionStore
    actors: ActorPolicy
    policy: SectionPolicy

    def execute(self, title: str, allowed_kinds: list[str], actor: Actor) -> Section:
        self.actors.allow_contributing(actor)
        section = self.policy.create(title, allowed_kinds)
        self.sections.save(section)
        return section
