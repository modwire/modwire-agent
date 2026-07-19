from dirty_equals import IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class PublicationScenarios(RecordsApiTestCase):
    def test_publishes_a_record_after_valid_content_is_stored(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        self.replace_content(record["id"], self.valid_rule_markdown())

        response = self.publish_record(record["id"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID, status="published"))
