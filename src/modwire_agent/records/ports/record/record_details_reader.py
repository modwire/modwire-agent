from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RecordDetails:
    identifier: UUID
    title: str
    kind: str
    status: str
    tag_names: tuple[str, ...]


class RecordDetailsReader(ABC):
    @abstractmethod
    def get(self, record_id: UUID) -> RecordDetails:
        raise NotImplementedError
