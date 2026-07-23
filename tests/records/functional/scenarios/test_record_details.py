from dirty_equals import IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class RecordDetailsScenarios(RecordsApiTestCase):
    def test_returns_a_records_metadata_and_normalized_tags(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        tag = self.create_tag("Testing")
        self.set_record_tags(record["id"], [tag["id"]])

        response = self.get_record(record["id"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), IsPartialDict(id=IsUUID, title="API tests", kind="rule", status="draft", tags=["testing"])
        )
