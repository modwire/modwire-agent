from dirty_equals import IsList, IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class SearchScenarios(RecordsApiTestCase):
    def test_keeps_text_and_semantic_search_as_separate_public_paths(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "HTTP contract", "rule")
        self.replace_content(record["id"], self.valid_rule_markdown())
        self.publish_record(record["id"])

        text = self.search_text("HTTP")
        semantic = self.search_semantic("HTTP contract")

        self.assertEqual(text.status_code, 200)
        self.assertEqual(text.json(), IsList(IsPartialDict(id=IsUUID, reason="text")))
        self.assertEqual(semantic.status_code, 200)
        self.assertEqual(semantic.json(), IsList(IsPartialDict(id=IsUUID, reason="semantic")))
