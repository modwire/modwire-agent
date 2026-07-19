from dataclasses import dataclass
from uuid import UUID, uuid4

from .invalid import InvalidRecord
from .kind import RecordKind
from .record import Record
from .status import RecordStatus


@dataclass(frozen=True, slots=True)
class RecordPolicy:
    def create(self, title: str, kind: str) -> Record:
        if not title.strip():
            raise InvalidRecord("Record title is required.")
        try:
            record_kind = RecordKind(kind)
        except ValueError as error:
            raise InvalidRecord("Record has an unknown kind.") from error
        return Record(identifier=uuid4(), title=title, kind=record_kind, status=RecordStatus.DRAFT)

    def publish(self, record: Record, has_valid_content: bool) -> Record:
        if not has_valid_content:
            raise InvalidRecord("A record needs valid content before publication.")
        return Record(identifier=record.identifier, title=record.title, kind=record.kind, status=RecordStatus.PUBLISHED, tag_ids=record.tag_ids)

    def assign_tags(self, record: Record, tag_ids: list[UUID], all_exist: bool) -> Record:
        if len(set(tag_ids)) != len(tag_ids):
            raise InvalidRecord("A record cannot have the same tag more than once.")
        if not all_exist:
            raise InvalidRecord("A record can only use existing tags.")
        return Record(identifier=record.identifier, title=record.title, kind=record.kind, status=record.status, tag_ids=tuple(tag_ids))

    def rename(self, record: Record, title: str) -> Record:
        if not title.strip():
            raise InvalidRecord("Record title is required.")
        return Record(identifier=record.identifier, title=title, kind=record.kind, status=record.status, tag_ids=record.tag_ids)

    def archive(self, record: Record) -> Record:
        if record.status is RecordStatus.ARCHIVED:
            raise InvalidRecord("Record is already archived.")
        return Record(identifier=record.identifier, title=record.title, kind=record.kind, status=RecordStatus.ARCHIVED, tag_ids=record.tag_ids)
