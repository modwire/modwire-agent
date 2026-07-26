from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.policy import RecordPolicy
from ...ports.outbound import RecordStore


@dataclass(frozen=True, slots=True)
class ArchiveRecord:
    records: RecordStore
    actors: ActorPolicy
    policy: RecordPolicy

    def execute(self, record_id: UUID, actor: Actor) -> None:
        self.actors.allow_contributing(actor)
        self.records.save(self.policy.archive(self.records.get(record_id)))
