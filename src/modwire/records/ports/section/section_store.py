from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.section.section import Section


class SectionStore(ABC):
    @abstractmethod
    def get(self, section_id: UUID) -> Section:
        raise NotImplementedError

    @abstractmethod
    def save(self, section: Section) -> None:
        raise NotImplementedError
