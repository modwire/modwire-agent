from dataclasses import dataclass
from uuid import UUID

from .kind import RecordKind
from .status import RecordStatus


@dataclass(frozen=True, slots=True)
class Record:
    identifier: UUID
    title: str
    kind: RecordKind
    status: RecordStatus
    tag_ids: tuple[UUID, ...] = ()
