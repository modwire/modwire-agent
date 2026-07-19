from dataclasses import dataclass
from uuid import UUID

from ..collaboration.actor import Actor

@dataclass(frozen=True, slots=True)
class ContentRevision:
    identifier: UUID
    record_id: UUID
    actor: Actor
    markdown: str
    schema_version: int
