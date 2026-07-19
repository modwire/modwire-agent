from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.record.content_revision import ContentRevision


class ContentStore(ABC):
    @abstractmethod
    def for_record(self, record_id: UUID) -> list[ContentRevision]:
        raise NotImplementedError

    @abstractmethod
    def has_revision(self, record_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def next_version(self, record_id: UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    def save(self, revision: ContentRevision) -> None:
        raise NotImplementedError
