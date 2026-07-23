from ...api import RecordsApiTestCase


class ActorHeaderAttacks(RecordsApiTestCase):
    def test_rejects_a_reorder_without_an_actor_identity(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "First", "rule")

        response = self.client.put(
            f"/api/sections/{section['id']}/placements",
            data={"record_ids": [record["id"]]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Missing required actor headers: X-Actor-Id, X-Actor-Type.")

    def test_serves_the_siren_api_root_without_actor_headers(self) -> None:
        response = self.client.get("/siren/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
