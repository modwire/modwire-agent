from dataclasses import dataclass
from uuid import uuid4

from ..record.kind import RecordKind
from .invalid import InvalidSection
from .section import Section


@dataclass(frozen=True, slots=True)
class SectionPolicy:
    def create(self, title: str, allowed_kinds: list[str]) -> Section:
        if not title.strip():
            raise InvalidSection("Section title is required.")
        if not allowed_kinds:
            raise InvalidSection("A section must allow at least one record kind.")
        try:
            kinds = tuple(RecordKind(kind) for kind in allowed_kinds)
        except ValueError as error:
            raise InvalidSection("Section contains an unknown record kind.") from error
        return Section(identifier=uuid4(), title=title, allowed_kinds=kinds, placements=())
