from dirty_equals import IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class SectionDetailsScenarios(RecordsApiTestCase):
    def test_returns_records_in_the_sections_persisted_order(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        first = self.create_record(section["id"], "First", "rule")
        second = self.create_record(section["id"], "Second", "rule")
        self.replace_section_placements(section["id"], [second["id"], first["id"]], self.agent_headers())

        response = self.get_section(section["id"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID, title="Architecture", records=[IsPartialDict(id=second["id"], title="Second"), IsPartialDict(id=first["id"], title="First")]))
