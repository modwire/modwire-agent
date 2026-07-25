from abc import ABC, abstractmethod

from ...domain.record.record import Record


class SearchProjectionStore(ABC):
    @abstractmethod
    def index(self, record: Record) -> None:
        raise NotImplementedError
