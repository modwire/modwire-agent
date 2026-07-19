from ..api import RecordsApiTestCase


class ContentKindScenarios(RecordsApiTestCase):
    def test_stores_a_decision_with_its_required_heading_schema(self) -> None:
        section = self.create_section("Architecture decisions", ["decision"])
        record = self.create_record(section["id"], "Adopt REST", "decision")

        response = self.replace_content(record["id"], "## Context\n\nWe need an API.\n\n## Decision\n\nUse REST.\n\n## Consequences\n\nClients use resources.")

        self.assertEqual(response.status_code, 200)
