from dirty_equals import IsList, IsPartialDict, IsUUID
from django.test import TestCase


class PublishedRecordsCollectionScenarios(TestCase):
    def test_lists_published_records_without_a_tag_filter(self) -> None:
        section = self.create_section()
        tag = self.create_tag()
        record = self.create_record(section["id"])
        self.set_record_tags(record["id"], [tag["id"]])
        self.store_content(record["id"])
        self.publish(record["id"])

        response = self.client.get("/api/records")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), IsList(IsPartialDict(id=IsUUID, title="API tests", reason=None)))

    def create_section(self) -> dict[str, object]:
        response = self.client.post(
            "/api/sections",
            data={"title": "Architecture", "allowed_kinds": ["rule"]},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 201)
        return response.json()

    def create_tag(self) -> dict[str, object]:
        response = self.client.post(
            "/api/tags",
            data={"name": "testing"},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 201)
        return response.json()

    def create_record(self, section_id: object) -> dict[str, object]:
        response = self.client.post(
            f"/api/sections/{section_id}/records",
            data={"title": "API tests", "kind": "rule"},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 201)
        return response.json()

    def set_record_tags(self, record_id: object, tag_ids: list[object]) -> None:
        response = self.client.put(
            f"/api/records/{record_id}/tags",
            data={"tag_ids": tag_ids},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 204)

    def store_content(self, record_id: object) -> None:
        response = self.client.put(
            f"/api/records/{record_id}/content",
            data={"markdown": "## Rules\n\nUse HTTP.\n\n## Verification\n\nRun tests."},
            content_type="application/json",
            headers=self.agent_headers(),
        )
        self.assertEqual(response.status_code, 200)

    def publish(self, record_id: object) -> None:
        response = self.client.post(f"/api/records/{record_id}/publish", headers=self.agent_headers())
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def agent_headers() -> dict[str, str]:
        return {"X-Actor-Id": "test-agent", "X-Actor-Type": "agent"}
