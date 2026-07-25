from dataclasses import dataclass
from uuid import UUID

from .section_record_details import SectionRecordDetails


@dataclass(frozen=True, slots=True)
class SectionDetails:
    identifier: UUID
    title: str
    allowed_kinds: tuple[str, ...]
    records: tuple[SectionRecordDetails, ...]
