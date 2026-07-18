import pytest

from .support import RecordResourceFactory

pytestmark = pytest.mark.django_db


class TestContentResource(RecordResourceFactory):
    def test_content_block_lifecycle_is_exposed_through_endpoints(self, client, auth):
        api = self.api(client, auth)
        section = self.create_section(api, "Content Docs")
        record = self.create_record(api, section["slug"], section["tag_slugs"], title="Content Intro")

        created = self.siren(
            api.post(
                "/api/contents",
                {
                    "record_slug": record["slug"],
                    "position": 1,
                    "role": "list",
                    "content": ["First", "Second"],
                    "language": "en",
                    "metadata": {"source": "endpoint-test"},
                },
            )
        )
        content = created.properties
        assert content["record_slug"] == record["slug"]
        assert content["role"] == "list"

        self.siren(api.get(f"/api/contents/{content['id']}")).assert_classes("content").assert_actions(
            ["get_content", "update_content", "delete_content"]
        )

        patched = self.siren(
            api.patch(
                f"/api/contents/{content['id']}",
                {"position": 2, "role": "paragraph", "content": "Moved.", "language": "en"},
            )
        )
        assert patched.properties["position"] == 2
        assert patched.properties["content"] == "Moved."
        assert api.delete(f"/api/contents/{content['id']}").content == b""

    def test_content_role_contract_rejects_wrong_shape(self, client, auth):
        api = self.api(client, auth)
        section = self.create_section(api, "Content Contract")
        record = self.create_record(api, section["slug"], section["tag_slugs"])

        document = self.problem(
            api.post(
                "/api/contents",
                {
                    "record_slug": record["slug"],
                    "position": 1,
                    "role": "list",
                    "content": "not-a-list",
                    "language": "en",
                    "metadata": {"source": "endpoint-test"},
                },
                expected=422,
            )
        )

        assert document.body["status"] == 422

    def test_duplicate_content_position_is_rejected_as_problem_document(self, client, auth):
        api = self.api(client, auth)
        section = self.create_section(api, "Content Collision")
        record = self.create_record(api, section["slug"], section["tag_slugs"])

        document = self.problem(
            api.post(
                "/api/contents",
                {
                    "record_slug": record["slug"],
                    "position": 0,
                    "role": "paragraph",
                    "content": "Position already exists.",
                    "language": "en",
                    "metadata": {"source": "endpoint-test"},
                },
                expected=422,
            )
        )

        assert "position" in document.body["detail"].lower()
