from dirty_equals import IsPartialDict

from ..api import RecordsApiTestCase


class SectionPlacementScenarios(RecordsApiTestCase):
    def test_replaces_a_sections_complete_record_order(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        first = self.create_record(section["id"], "First", "rule")
        second = self.create_record(section["id"], "Second", "rule")

        response = self.replace_section_placements(section["id"], [second["id"], first["id"]], self.agent_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), IsPartialDict(record_ids=[second["id"], first["id"]]))
