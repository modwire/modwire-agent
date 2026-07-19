from dataclasses import dataclass
from uuid import UUID

from ...ports.section.section_details import SectionDetails
from ...ports.section.section_details_reader import SectionDetailsReader


@dataclass(frozen=True, slots=True)
class GetSectionDetails:
    reader: SectionDetailsReader

    def execute(self, section_id: UUID) -> SectionDetails:
        return self.reader.get(section_id)
