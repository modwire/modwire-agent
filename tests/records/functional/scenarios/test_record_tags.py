from ..api import RecordsApiTestCase


class RecordTagScenarios(RecordsApiTestCase):
    def test_assigns_existing_tags_to_a_record(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        tag = self.create_tag("Testing")

        self.set_record_tags(record["id"], [tag["id"]])
