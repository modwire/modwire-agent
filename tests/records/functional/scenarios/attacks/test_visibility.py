from ...api import RecordsApiTestCase


class DraftVisibilityAttacks(RecordsApiTestCase):
    def setUp(self) -> None:
        self.section = self.create_section("Architecture", ["rule"])
        self.tag = self.create_tag("testing")
        self.record = self.create_record(self.section["id"], "API tests", "rule")
        self.set_record_tags(self.record["id"], [self.tag["id"]])

    def test_does_not_route_a_draft_record(self) -> None:
        response = self.find_records(["testing"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
