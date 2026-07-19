from ...api import RecordsApiTestCase


class ActorHeaderAttacks(RecordsApiTestCase):
    def test_rejects_a_reorder_without_an_actor_identity(self) -> None:
        section = self._create_siren_section("Architecture")
        record = self._create_siren_record(section["id"], "First")

        response = self.client.put(
            f"/api/sections/{section['id']}/placements",
            data={"record_ids": [record["id"]]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Missing required actor headers: X-Actor-Id, X-Actor-Type.")

    def test_rejects_a_siren_mutation_without_actor_headers(self) -> None:
        section = self._create_siren_section("Siren")
        record = self._create_siren_record(section["id"], "Siren contract")
        tag = self._create_siren_tag("siren")
        proposal = self._create_siren_content_proposal(record["id"])

        requests = [
            ("post", "/siren/sections", {"title": "Missing actor", "allowed_kinds": ["rule"]}),
            ("post", "/siren/tags", {"name": "missing-actor"}),
            ("post", f"/siren/sections/{section['id']}/records", {"title": "Missing actor", "kind": "rule"}),
            ("put", f"/siren/sections/{section['id']}/placements", {"record_ids": [record["id"]]}),
            ("patch", f"/siren/records/{record['id']}", {"title": "Renamed"}),
            ("put", f"/siren/records/{record['id']}/tags", {"tag_ids": [tag["id"]]}),
            ("put", f"/siren/records/{record['id']}/content", {"markdown": self.valid_rule_markdown()}),
            ("post", f"/siren/records/{record['id']}/content-proposals", {"markdown": self.valid_rule_markdown()}),
            ("post", f"/siren/records/{record['id']}/publish", None),
            (
                "patch",
                f"/siren/records/{record['id']}/content-proposals/{proposal['id']}",
                {"status": "accepted"},
            ),
            ("delete", f"/siren/records/{record['id']}", None),
        ]

        for method, path, payload in requests:
            with self.subTest(method=method, path=path):
                response = self._siren_mutation_without_actor_headers(method, path, payload)

                self.assertEqual(response.status_code, 422)
                self.assertEqual(response.json()["detail"], "Missing required actor headers: X-Actor-Id, X-Actor-Type.")

    def test_rejects_a_siren_mutation_with_an_invalid_actor_type(self) -> None:
        response = self.client.post(
            "/siren/tags",
            data={"name": "invalid-actor-kind"},
            content_type="application/json",
            headers={"X-Actor-Id": "test", "X-Actor-Type": "service"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Actor kind must be user or agent.")

    def test_reads_siren_root_without_actor_headers(self) -> None:
        response = self.client.get("/siren/")

        self.assertEqual(response.status_code, 200)

    def _siren_mutation_without_actor_headers(self, method: str, path: str, payload: dict[str, object] | None):
        client_method = getattr(self.client, method)
        if payload is None:
            return client_method(path)
        return client_method(path, data=payload, content_type="application/json")

    def _create_siren_section(self, title: str) -> dict[str, object]:
        response = self.client.post(
            "/siren/sections",
            data={"title": title, "allowed_kinds": ["rule"]},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["properties"]

    def _create_siren_record(self, section_id: str, title: str) -> dict[str, object]:
        response = self.client.post(
            f"/siren/sections/{section_id}/records",
            data={"title": title, "kind": "rule"},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["properties"]

    def _create_siren_tag(self, name: str) -> dict[str, object]:
        response = self.client.post(
            "/siren/tags",
            data={"name": name},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["entities"][0]["properties"]

    def _create_siren_content_proposal(self, record_id: str) -> dict[str, object]:
        response = self.client.post(
            f"/siren/records/{record_id}/content-proposals",
            data={"markdown": self.valid_rule_markdown()},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 200)
        proposals = self.client.get(f"/siren/records/{record_id}/content-proposals")
        self.assertEqual(proposals.status_code, 200)
        return proposals.json()["entities"][0]["properties"]
