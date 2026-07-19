from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.record.record import Record


class RecordStore(ABC):
    @abstractmethod
    def get(self, record_id: UUID) -> Record:
        raise NotImplementedError

    @abstractmethod
    def save(self, record: Record) -> None:
        raise NotImplementedError
