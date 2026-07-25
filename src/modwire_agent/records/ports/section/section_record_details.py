from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SectionRecordDetails:
    identifier: UUID
    title: str
    kind: str
    status: str
