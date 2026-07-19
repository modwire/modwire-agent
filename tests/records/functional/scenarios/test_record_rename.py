from dirty_equals import IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class RecordRenameScenarios(RecordsApiTestCase):
    def test_an_agent_can_rename_a_record(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        response = self.rename_record(record["id"], "REST API tests", self.agent_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID, title="REST API tests"))
