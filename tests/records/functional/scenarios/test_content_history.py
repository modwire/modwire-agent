from ..api import RecordsApiTestCase


class ContentHistoryScenarios(RecordsApiTestCase):
    def test_preserves_each_valid_content_replacement_as_an_ordered_revision(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        first = self.replace_content(record["id"], self.valid_rule_markdown())
        second = self.replace_content(record["id"], "## Rules\n\nUse REST.\n\n## Verification\n\nExercise the public API.")

        revisions = self.list_content_revisions(record["id"])

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(revisions.status_code, 200)
        self.assertEqual([revision["schema_version"] for revision in revisions.json()], [1, 2])
        self.assertEqual([revision["actor_type"] for revision in revisions.json()], ["agent", "agent"])
