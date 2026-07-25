from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.policy import RecordPolicy
from ...ports.record.record_store import RecordStore
from ...ports.tag.tag_store import TagStore


@dataclass(frozen=True, slots=True)
class AssignTags:
    records: RecordStore
    tags: TagStore
    actors: ActorPolicy
    policy: RecordPolicy

    def execute(self, record_id: UUID, tag_ids: list[UUID], actor: Actor) -> None:
        self.actors.allow_contributing(actor)
        record = self.records.get(record_id)
        tagged = self.policy.assign_tags(record, tag_ids, self.tags.has_all(tag_ids))
        self.records.save(tagged)
