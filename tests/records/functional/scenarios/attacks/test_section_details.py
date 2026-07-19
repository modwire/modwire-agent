from uuid import uuid4

from ...api import RecordsApiTestCase


class SectionDetailsAttacks(RecordsApiTestCase):
    def test_returns_not_found_for_an_unknown_section(self) -> None:
        response = self.get_section(str(uuid4()))

        self.assertEqual(response.status_code, 404)
