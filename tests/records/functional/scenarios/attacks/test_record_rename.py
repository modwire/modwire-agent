from ...api import RecordsApiTestCase


class RecordRenameAttacks(RecordsApiTestCase):
    def test_rejects_a_blank_record_title(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        response = self.rename_record(record["id"], " ", self.agent_headers())

        self.assertEqual(response.status_code, 422)
