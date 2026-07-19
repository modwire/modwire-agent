from ..api import RecordsApiTestCase


class RecordArchiveScenarios(RecordsApiTestCase):
    def test_archives_a_record_without_removing_its_detail_resource(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        archived = self.archive_record(record["id"], self.agent_headers())
        details = self.get_record(record["id"])

        self.assertEqual(archived.status_code, 204)
        self.assertEqual(details.json()["status"], "archived")
