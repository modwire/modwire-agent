from ...api import RecordsApiTestCase


class ContentSchemaAttacks(RecordsApiTestCase):
    def setUp(self) -> None:
        self.section = self.create_section("Architecture", ["rule"])
        self.record = self.create_record(self.section["id"], "API tests", "rule")

    def test_rejects_rule_markdown_without_verification(self) -> None:
        response = self.replace_content(self.record["id"], "## Rules\n\nUse HTTP.")

        self.assertEqual(response.status_code, 422)

    def test_rejects_publishing_a_rule_without_valid_content(self) -> None:
        response = self.publish_record(self.record["id"])

        self.assertEqual(response.status_code, 422)

    def test_rejects_a_decision_without_its_required_headings(self) -> None:
        section = self.create_section("Architecture decisions", ["decision"])
        record = self.create_record(section["id"], "Adopt REST", "decision")

        response = self.replace_content(record["id"], "## Context\n\nWe need an API.")

        self.assertEqual(response.status_code, 422)
