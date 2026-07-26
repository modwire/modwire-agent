from dataclasses import dataclass
from uuid import UUID

from ..domain.collaboration.actor import Actor
from ..domain.collaboration.policy import ActorPolicy
from ..domain.record.policy import RecordPolicy
from ..domain.record.record import Record
from ..ports.outbound import ContentStore, RecordStore, SearchProjectionStore


@dataclass(frozen=True, slots=True)
class PublishRecord:
    records: RecordStore
    content: ContentStore
    actors: ActorPolicy
    policy: RecordPolicy
    projections: SearchProjectionStore

    def execute(self, record_id: UUID, actor: Actor) -> Record:
        self.actors.allow_contributing(actor)
        record = self.records.get(record_id)
        published = self.policy.publish(record, self.content.has_revision(record_id))
        self.records.save(published)
        self.projections.index(published)
        return published
