from ...api import RecordsApiTestCase


class SectionKindAttacks(RecordsApiTestCase):
    def setUp(self) -> None:
        self.section = self.create_section("Architecture", ["rule"])

    def test_rejects_a_record_kind_not_allowed_by_its_section(self) -> None:
        response = self.request_record(self.section["id"], "An ADR", "decision")

        self.assertEqual(response.status_code, 422)
