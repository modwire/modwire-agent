from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.tag.tag import Tag


class TagStore(ABC):
    @abstractmethod
    def has_all(self, tag_ids: list[UUID]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save(self, tag: Tag) -> None:
        raise NotImplementedError
