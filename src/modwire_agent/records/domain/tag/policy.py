from dataclasses import dataclass
from uuid import uuid4

from .invalid import InvalidTag
from .tag import Tag


@dataclass(frozen=True, slots=True)
class TagPolicy:
    def create(self, name: str) -> Tag:
        normalized_name = name.strip().lower()
        if not normalized_name:
            raise InvalidTag("Tag name is required.")
        return Tag(identifier=uuid4(), name=normalized_name)
