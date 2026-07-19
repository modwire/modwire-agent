from ...api import RecordsApiTestCase


class SectionPlacementAttacks(RecordsApiTestCase):
    def test_rejects_a_placement_list_that_omits_a_section_record(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        first = self.create_record(section["id"], "First", "rule")
        self.create_record(section["id"], "Second", "rule")

        response = self.replace_section_placements(section["id"], [first["id"]], self.agent_headers())

        self.assertEqual(response.status_code, 422)
