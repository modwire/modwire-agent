from ...api import RecordsApiTestCase


class RecordArchiveAttacks(RecordsApiTestCase):
    def test_rejects_archiving_an_archived_record(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        self.archive_record(record["id"], self.agent_headers())

        response = self.archive_record(record["id"], self.agent_headers())

        self.assertEqual(response.status_code, 422)
