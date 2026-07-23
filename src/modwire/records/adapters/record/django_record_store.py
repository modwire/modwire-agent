from uuid import UUID

from modwire_hex.django import DjangoRepository

from ...domain.record.kind import RecordKind
from ...domain.record.record import Record
from ...domain.record.status import RecordStatus
from ...ports.record.record_store import RecordStore
from ..django.models import RecordModel


class DjangoRecordStore(DjangoRepository[Record, RecordModel, UUID], RecordStore):
    def save(self, record: Record) -> None:
        super().save(record)
        RecordModel.objects.get(identifier=record.identifier).tags.set(record.tag_ids)

    def key_of(self, domain: Record) -> UUID:
        return domain.identifier

    def find_record(self, key: UUID) -> RecordModel | None:
        try:
            return RecordModel.objects.get(identifier=key)
        except RecordModel.DoesNotExist:
            return None

    def create_record(self, domain: Record) -> RecordModel:
        return RecordModel(identifier=domain.identifier, title=domain.title, kind=domain.kind, status=domain.status)

    def update_record(self, model: RecordModel, domain: Record) -> None:
        model.title = domain.title
        model.kind = domain.kind
        model.status = domain.status

    def get(self, record_id: UUID) -> Record:
        record = self.load(record_id)
        if record is None:
            raise LookupError(f"Record {record_id!r} was not found.")
        return record

    def to_domain(self, model: RecordModel) -> Record:
        return Record(
            identifier=model.identifier,
            title=model.title,
            kind=RecordKind(model.kind),
            status=RecordStatus(model.status),
            tag_ids=tuple(model.tags.values_list("identifier", flat=True)),
        )
