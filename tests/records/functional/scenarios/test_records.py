from ..api import RecordsApiTestCase


class RecordScenarios(RecordsApiTestCase):
    def test_creates_a_draft_record_in_an_allowed_section(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        self.assertEqual(record["status"], "draft")
