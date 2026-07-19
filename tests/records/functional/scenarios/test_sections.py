from ..api import RecordsApiTestCase


class SectionScenarios(RecordsApiTestCase):
    def test_creates_a_section_with_its_allowed_record_kinds(self) -> None:
        section = self.create_section("Architecture", ["rule", "decision"])

        self.assertEqual(section["allowed_kinds"], ["rule", "decision"])
