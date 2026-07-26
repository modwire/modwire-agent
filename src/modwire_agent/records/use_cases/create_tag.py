from dataclasses import dataclass

from ..domain.collaboration.actor import Actor
from ..domain.collaboration.policy import ActorPolicy
from ..domain.tag.policy import TagPolicy
from ..domain.tag.tag import Tag
from ..ports.outbound import TagStore


@dataclass(frozen=True, slots=True)
class CreateTag:
    tags: TagStore
    actors: ActorPolicy
    policy: TagPolicy

    def execute(self, name: str, actor: Actor) -> Tag:
        self.actors.allow_contributing(actor)
        tag = self.policy.create(name)
        self.tags.save(tag)
        return tag
