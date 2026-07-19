from abc import ABC, abstractmethod
from uuid import UUID

from .section_details import SectionDetails


class SectionDetailsReader(ABC):
    @abstractmethod
    def get(self, section_id: UUID) -> SectionDetails:
        raise NotImplementedError
