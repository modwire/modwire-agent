from uuid import uuid4

from ...api import RecordsApiTestCase


class RecordDetailsAttacks(RecordsApiTestCase):
    def test_returns_not_found_for_an_unknown_record(self) -> None:
        response = self.get_record(str(uuid4()))

        self.assertEqual(response.status_code, 404)
