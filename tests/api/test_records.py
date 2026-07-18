import pytest

from .support import RecordResourceFactory

pytestmark = pytest.mark.django_db


class TestTagResource(RecordResourceFactory):
    def test_tag_lifecycle_is_available_through_endpoint_actions(self, client, auth):
        api = self.api(client, auth)
        tag = self.create_tag(api, "Lifecycle")

        updated = self.siren(
            api.put(
                f"/api/tags/{tag['slug']}",
                {"name": "Lifecycle", "description": "Replaced through PUT."},
            )
        )
        updated.assert_classes("tag").assert_actions(["get_tag", "update_tag", "delete_tag"])
        assert updated.properties["description"] == "Replaced through PUT."

        self.siren(api.get("/api/tags")).assert_classes("collection", "tag").assert_actions(
            ["list_tags", "create_tag"]
        )
        assert api.delete(f"/api/tags/{tag['slug']}").content == b""

    def test_duplicate_tag_name_is_rejected_as_problem_document(self, client, auth):
        api = self.api(client, auth)
        self.create_tag(api, "Duplicate")

        document = self.problem(api.post("/api/tags", self.tag_payload("Duplicate"), expected=422))

        assert "already exists" in document.body["detail"]

    def test_missing_tag_is_reported_as_problem_document(self, client, auth):
        document = self.problem(self.api(client, auth).get("/api/tags/missing-tag", expected=404))

        assert document.body["status"] == 404


class TestSectionResource(RecordResourceFactory):
    def test_section_lifecycle_requires_tags_and_advertises_actions(self, client, auth):
        api = self.api(client, auth)
        tag = self.create_tag(api, "Section Lifecycle")
        section = self.create_section(api, "Lifecycle Section", [tag["slug"]])

        patched = self.siren(
            api.patch(
                f"/api/sections/{section['slug']}",
                {"description": "Patched through the API."},
            )
        )
        patched.assert_classes("section").assert_actions(["get_section", "update_section", "delete_section"])
        assert patched.properties["description"] == "Patched through the API."

        self.siren(api.get("/api/sections?limit=10&offset=0")).assert_classes(
            "collection",
            "section",
        ).assert_actions(["list_sections", "create_section"])
        assert api.delete(f"/api/sections/{section['slug']}").content == b""
        assert api.delete(f"/api/tags/{tag['slug']}").content == b""

    def test_section_without_tags_is_rejected_before_state_changes(self, client, auth):
        document = self.problem(
            self.api(client, auth).post(
                "/api/sections",
                self.section_payload("No Tags", []),
                expected=422,
            )
        )

        assert "tag_slugs" in document.body["detail"]


class TestRecordResource(RecordResourceFactory):
    def test_record_lifecycle_search_and_slash_slug_resolution_are_endpoint_contracts(self, client, auth):
        api = self.api(client, auth)
        tag = self.create_tag(api, "API")
        second_tag = self.create_tag(api, "Guide")
        section = self.create_section(api, tag_slugs=[tag["slug"]])
        record = self.create_record(api, section["slug"], [tag["slug"], second_tag["slug"]])

        assert record["slug"] == "endpoint-docs/endpoint-intro"

        records = self.siren(api.get(f"/api/records?limit=1&offset=0&tag={tag['slug']}"))
        records.assert_classes("collection", "record").assert_actions(
            ["list_records", "create_record", "search_records"]
        )
        assert {"self", "first", "next"}.issubset(records.links)
        assert records.embedded("record")

        entity = self.siren(api.get(f"/api/records/{record['slug']}"))
        entity.assert_classes("record").assert_actions(["get_record", "update_record", "delete_record"])
        assert {"self", "section", "tag"}.issubset(entity.links)

        patched = self.siren(
            api.patch(f"/api/records/{record['slug']}", {"description": "Updated through PATCH."})
        )
        assert patched.properties["description"] == "Updated through PATCH."

        search = self.siren(
            api.post(
                "/api/records/search",
                {
                    "query": "Endpoint body",
                    "mode": "fts",
                    "target": "all",
                    "limit": 10,
                    "offset": 0,
                    "section_slugs": [],
                    "tag_slugs": [tag["slug"]],
                },
            )
        )
        search.assert_classes("record-search").assert_actions(["search_records"])
        assert any(result["slug"] == record["slug"] for result in search.properties["results"])

        assert api.delete(f"/api/records/{record['slug']}").content == b""

    def test_record_pagination_preserves_repeated_filter_query_values(self, client, auth):
        api = self.api(client, auth)
        first_tag = self.create_tag(api, "Alpha")
        second_tag = self.create_tag(api, "Beta")
        section = self.create_section(api, tag_slugs=[first_tag["slug"], second_tag["slug"]])
        self.create_record(api, section["slug"], [first_tag["slug"], second_tag["slug"]], "Repeated Query")

        document = self.siren(
            api.get(
                f"/api/records?limit=1&offset=0&tag={first_tag['slug']}&tag={second_tag['slug']}"
            )
        )

        assert f"tag={first_tag['slug']}" in document.links["next"]
        assert f"tag={second_tag['slug']}" in document.links["next"]

    def test_search_result_singleton_has_static_self_link(self, client, auth):
        api = self.api(client, auth)

        document = self.siren(
            api.post(
                "/api/records/search",
                {
                    "query": "anything",
                    "mode": "fts",
                    "target": "all",
                    "limit": 10,
                    "offset": 0,
                    "section_slugs": [],
                    "tag_slugs": [],
                },
            )
        ).assert_classes("record-search")

        assert document.links["self"].endswith("/api/records/search")

    def test_record_without_tags_is_rejected_as_problem_document(self, client, auth):
        api = self.api(client, auth)
        section = self.create_section(api)
        payload = self.record_payload(section["slug"], [])

        document = self.problem(api.post("/api/records", payload, expected=422))

        assert "tag_slugs" in document.body["detail"]

    def test_invalid_search_mode_is_rejected_as_problem_document(self, client, auth):
        document = self.problem(
            self.api(client, auth).post(
                "/api/records/search",
                {
                    "query": "anything",
                    "mode": "sql",
                    "target": "all",
                    "limit": 10,
                    "offset": 0,
                    "section_slugs": [],
                    "tag_slugs": [],
                },
                expected=422,
            )
        )

        assert document.body["status"] == 422
