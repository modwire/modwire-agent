from ...api import RecordsApiTestCase


class RouteFilteringAttacks(RecordsApiTestCase):
    def setUp(self) -> None:
        self.section = self.create_section("Architecture", ["rule"])
        self.tag = self.create_tag("testing")
        self.record = self.create_record(self.section["id"], "API tests", "rule")
        self.set_record_tags(self.record["id"], [self.tag["id"]])
        self.replace_content(self.record["id"], "## Rules\n\nUse HTTP.\n\n## Verification\n\nRun tests.")
        self.publish_record(self.record["id"])

    def test_does_not_route_a_record_for_an_unassigned_tag(self) -> None:
        response = self.find_records(["architecture"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
