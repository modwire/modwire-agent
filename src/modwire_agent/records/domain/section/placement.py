from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SectionPlacement:
    record_id: UUID
    position: int
