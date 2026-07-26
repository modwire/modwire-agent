from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.record.content_revision import ContentRevision
from ...domain.record.content_schema_policy import ContentSchemaPolicy
from ...ports.outbound import ContentStore, RecordStore, SearchProjectionStore


@dataclass(frozen=True, slots=True)
class ReplaceContent:
    records: RecordStore
    content: ContentStore
    schema: ContentSchemaPolicy
    actors: ActorPolicy
    projections: SearchProjectionStore

    def execute(self, record_id: UUID, markdown: str, actor: Actor) -> ContentRevision:
        self.actors.allow_editing(actor)
        record = self.records.get(record_id)
        revision = self.schema.create_revision(record, markdown, self.content.next_version(record_id), actor)
        self.content.save(revision)
        if record.status.value == "published":
            self.projections.index(record)
        return revision
