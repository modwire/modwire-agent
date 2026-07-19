from uuid import UUID

from ...ports.record.record_details_reader import RecordDetails, RecordDetailsReader
from ..django.models import RecordModel


class DjangoRecordDetailsReader(RecordDetailsReader):
    def get(self, record_id: UUID) -> RecordDetails:
        try:
            record = RecordModel.objects.prefetch_related("tags").get(identifier=record_id)
        except RecordModel.DoesNotExist as error:
            raise LookupError(f"Record {record_id!r} was not found.") from error
        return RecordDetails(identifier=record.identifier, title=record.title, kind=record.kind, status=record.status, tag_names=tuple(tag.name for tag in record.tags.all()))
