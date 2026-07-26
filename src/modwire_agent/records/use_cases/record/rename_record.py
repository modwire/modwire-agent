from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.policy import RecordPolicy
from ...domain.record.record import Record
from ...ports.outbound import RecordStore


@dataclass(frozen=True, slots=True)
class RenameRecord:
    records: RecordStore
    actors: ActorPolicy
    policy: RecordPolicy

    def execute(self, record_id: UUID, title: str, actor: Actor) -> Record:
        self.actors.allow_editing(actor)
        renamed = self.policy.rename(self.records.get(record_id), title)
        self.records.save(renamed)
        return renamed
