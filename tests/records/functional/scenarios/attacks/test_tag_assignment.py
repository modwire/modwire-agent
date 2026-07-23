from uuid import uuid4

from ...api import RecordsApiTestCase


class TagAssignmentAttacks(RecordsApiTestCase):
    def test_rejects_an_unknown_tag(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        response = self.client.put(
            f"/api/records/{record['id']}/tags", data={"tag_ids": [str(uuid4())]}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
