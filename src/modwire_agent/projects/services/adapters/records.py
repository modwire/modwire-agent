from dataclasses import dataclass

from wireup import injectable

from modwire_agent.records.services import RecordsService


@injectable
@dataclass(frozen=True)
class RecordsAdapter:
    records: RecordsService

    def check_records_existence(self, record_ids: list[str]) -> None:
        for record_id in record_ids:
            self.records.get_record(record_id)
