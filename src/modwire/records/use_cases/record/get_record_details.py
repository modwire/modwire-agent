from dataclasses import dataclass
from uuid import UUID

from ...ports.record.record_details_reader import RecordDetails, RecordDetailsReader


@dataclass(frozen=True, slots=True)
class GetRecordDetails:
    reader: RecordDetailsReader

    def execute(self, record_id: UUID) -> RecordDetails:
        return self.reader.get(record_id)
