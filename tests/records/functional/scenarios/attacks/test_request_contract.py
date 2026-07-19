from ...api import RecordsApiTestCase


class RequestContractAttacks(RecordsApiTestCase):
    def test_rejects_undeclared_fields_when_creating_resources(self) -> None:
        section = self.client.post(
            "/api/sections",
            data={"title": "Architecture", "allowed_kinds": ["rule"], "status": "published"},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        tag = self.client.post(
            "/api/tags",
            data={"name": "testing", "system": True},
            content_type="application/json",
            headers=self.agent_headers(),
        )

        self.assertEqual(section.status_code, 422)
        self.assertEqual(tag.status_code, 422)
