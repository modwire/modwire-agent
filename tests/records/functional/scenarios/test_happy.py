from dirty_equals import IsList, IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class HappyRecordsPath(RecordsApiTestCase):
    def test_publishes_a_valid_rule_and_returns_it_in_a_knowledge_route(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        tag = self.create_tag("testing")
        record = self.create_record(section["id"], "API tests", "rule")

        self.set_record_tags(record["id"], [tag["id"]])
        content = self.replace_content(record["id"], "## Rules\n\nUse HTTP.\n\n## Verification\n\nRun tests.")
        published = self.publish_record(record["id"])
        route = self.find_records(["testing"])

        self.assertEqual(content.status_code, 200)
        self.assertEqual(published.status_code, 200)
        self.assertEqual(route.status_code, 200)
        self.assertEqual(route.json(), IsList(IsPartialDict(id=IsUUID, reason="tag: testing", title="API tests")))
