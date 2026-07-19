from uuid import uuid4

from ...api import RecordsApiTestCase


class ContentProposalDetailsAttacks(RecordsApiTestCase):
    def test_returns_not_found_for_an_unknown_records_proposals(self) -> None:
        response = self.list_content_proposals(str(uuid4()))

        self.assertEqual(response.status_code, 404)
