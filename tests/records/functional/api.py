from django.test import TestCase
from dirty_equals import IsPartialDict, IsUUID
from urllib.parse import urlencode

from .content_api import ContentApiMixin
from .proposals_api import ProposalsApiMixin
from .read_api import ReadApiMixin


class RecordsApiTestCase(ContentApiMixin, ProposalsApiMixin, ReadApiMixin, TestCase):
    def create_section(self, title: str, allowed_kinds: list[str]) -> dict[str, object]:
        response = self.client.post("/api/sections", data={"title": title, "allowed_kinds": allowed_kinds}, content_type="application/json", headers=self.agent_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID, title=title))
        return response.json()

    def create_tag(self, name: str) -> dict[str, object]:
        response = self.client.post("/api/tags", data={"name": name}, content_type="application/json", headers=self.agent_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID))
        return response.json()

    def create_record(self, section_id: str, title: str, kind: str) -> dict[str, object]:
        response = self.request_record(section_id, title, kind)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), IsPartialDict(id=IsUUID, kind=kind, title=title))
        return response.json()

    def request_record(self, section_id: str, title: str, kind: str):
        return self.client.post(f"/api/sections/{section_id}/records", data={"title": title, "kind": kind}, content_type="application/json", headers=self.agent_headers())

    def replace_section_placements(self, section_id: str, record_ids: list[str], headers: dict[str, str]):
        return self.client.put(f"/api/sections/{section_id}/placements", data={"record_ids": record_ids}, content_type="application/json", headers=headers)

    def agent_headers(self) -> dict[str, str]:
        return {"X-Actor-Id": "test-agent", "X-Actor-Type": "agent"}

    def set_record_tags(self, record_id: str, tag_ids: list[str]) -> None:
        response = self.client.put(f"/api/records/{record_id}/tags", data={"tag_ids": tag_ids}, content_type="application/json", headers=self.agent_headers())
        self.assertEqual(response.status_code, 204)

    def publish_record(self, record_id: str):
        return self.client.post(f"/api/records/{record_id}/publish", headers=self.agent_headers())

    def find_records(self, tags: list[str]):
        query = urlencode([("tag", tag) for tag in tags])
        return self.client.get(f"/api/records?{query}")
