from dirty_equals import IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class ContentScenarios(RecordsApiTestCase):
    def test_stores_a_valid_rule_content_revision(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        response = self.replace_content(record["id"], self.valid_rule_markdown())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID, schema_version=1))
