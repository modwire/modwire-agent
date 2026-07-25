from dataclasses import dataclass
from uuid import UUID

from ...domain.record.content_revision import ContentRevision
from ...ports.record.content_store import ContentStore


@dataclass(frozen=True, slots=True)
class ListContentRevisions:
    content: ContentStore

    def execute(self, record_id: UUID) -> list[ContentRevision]:
        return self.content.for_record(record_id)
