from dataclasses import dataclass
from uuid import uuid4

from ..collaboration.actor import Actor
from .content_revision import ContentRevision
from .invalid import InvalidRecord
from .kind import RecordKind
from .record import Record


REQUIRED_HEADINGS = {
    RecordKind.RULE: ("## Rules", "## Verification"),
    RecordKind.DECISION: ("## Context", "## Decision", "## Consequences"),
    RecordKind.GUIDE: ("## Goal", "## Steps"),
    RecordKind.REFERENCE: ("## Summary",),
}


@dataclass(frozen=True, slots=True)
class ContentSchemaPolicy:
    def validate(self, record: Record, markdown: str) -> None:
        if not markdown.strip():
            raise InvalidRecord("Record content is required.")
        required_headings = REQUIRED_HEADINGS[record.kind]
        if not all(heading in markdown for heading in required_headings):
            raise InvalidRecord(f"{record.kind.title()} content is missing required headings.")

    def create_revision(self, record: Record, markdown: str, schema_version: int, actor: Actor) -> ContentRevision:
        self.validate(record, markdown)
        return ContentRevision(identifier=uuid4(), record_id=record.identifier, actor=actor, markdown=markdown, schema_version=schema_version)
