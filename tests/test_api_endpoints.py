import json
from collections.abc import Iterable

import pytest

from modwire.apps.tokens.models.api_key import ApiKey

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_key():
    _, key = ApiKey.generate("endpoint-test")
    return key


@pytest.fixture
def auth(api_key):
    return {"HTTP_APIKEY": api_key}


def request_json(client, method: str, path: str, auth: dict, payload: dict | None = None):
    request = getattr(client, method.lower())
    kwargs = dict(auth)
    if payload is not None:
        kwargs.update(data=json.dumps(payload), content_type="application/json")
    response = request(path, **kwargs)
    assert response.status_code < 400, response.content
    if response.status_code == 204:
        return response, None
    return response, response.json()


def post_json(client, path: str, auth: dict, payload: dict):
    return request_json(client, "post", path, auth, payload)


def patch_json(client, path: str, auth: dict, payload: dict):
    return request_json(client, "patch", path, auth, payload)


def put_json(client, path: str, auth: dict, payload: dict):
    return request_json(client, "put", path, auth, payload)


def siren_properties(document: dict) -> dict:
    return document.get("properties", {})


def siren_links(document: dict) -> dict[str, str]:
    return {
        rel: link["href"]
        for link in document.get("links", [])
        for rel in link.get("rel", [])
    }


def siren_action_names(document: dict) -> set[str]:
    return {action["name"] for action in document.get("actions", [])}


def siren_embedded(document: dict, *classes: str) -> list[dict]:
    wanted = set(classes)
    return [
        entity
        for entity in document.get("entities", [])
        if wanted.issubset(set(entity.get("class", [])))
    ]


def assert_siren(response):
    assert response["Content-Type"].startswith("application/vnd.siren+json")


def assert_classes(document: dict, *classes: str):
    assert set(classes).issubset(set(document.get("class", [])))


def assert_actions(document: dict, names: Iterable[str]):
    assert set(names).issubset(siren_action_names(document))


def create_tag(client, auth, name="Endpoint API"):
    _, document = post_json(
        client,
        "/api/tags",
        auth,
        {"name": name, "description": "Created through the HTTP API."},
    )
    return siren_properties(document)


def create_section(client, auth, title="Endpoint Docs", tag_slugs=None):
    if not tag_slugs:
        tag_slugs = [create_tag(client, auth, f"{title} Tag")["slug"]]
    _, document = post_json(
        client,
        "/api/sections",
        auth,
        {
            "title": title,
            "description": "Endpoint-only test section.",
            "tag_slugs": tag_slugs,
        },
    )
    return siren_properties(document)


def content_block(text="Endpoint body"):
    return {
        "role": "paragraph",
        "content": text,
        "language": "en",
        "metadata": {"source": "endpoint-test"},
    }


def create_record(client, auth, section_slug, tag_slugs=None, title="Endpoint Intro"):
    _, document = post_json(
        client,
        "/api/records",
        auth,
        {
            "section_slug": section_slug,
            "title": title,
            "description": "Record created through the HTTP API.",
            "sources": ["https://example.test/source"],
            "tag_slugs": tag_slugs or [],
            "content": [content_block()],
        },
    )
    return siren_properties(document)


def create_scaffolding(client, auth, name="Endpoint Scaffolding"):
    _, document = post_json(
        client,
        "/api/scaffoldings",
        auth,
        {
            "language_id": "python",
            "name": name,
            "description": "Created through endpoint tests.",
        },
    )
    return siren_properties(document)


class TestDiscoveryEndpoints:
    def test_api_root_requires_a_valid_api_key(self, client):
        response = client.get("/api/")

        assert response.status_code == 401
        assert response["Content-Type"].startswith("application/problem+json")
        assert response.json()["status"] == 401

    def test_api_root_and_openapi_describe_the_same_siren_api(self, client, auth):
        root_response = client.get("/api/", **auth)
        openapi_response = client.get("/api/openapi.json", **auth)

        assert root_response.status_code == 200
        assert openapi_response.status_code == 200
        assert_siren(root_response)

        root = root_response.json()
        openapi = openapi_response.json()

        assert_classes(root, "api")
        assert siren_properties(root)["version"] == openapi["info"]["version"]
        assert {"self", "records", "scaffoldings", "browser", "service-desc"}.issubset(
            siren_links(root)
        )
        assert {"SirenEntity", "Problem"}.issubset(openapi["components"]["schemas"])
        assert openapi["paths"]["/api/records/{record_slug}"]["x-siren-resource"]["name"] == "record"

    def test_discovery_links_honor_https_forwarded_by_the_deployment_proxy(self, client, auth, settings):
        settings.ALLOWED_HOSTS = ["modwire.example"]

        response = client.get(
            "/api/",
            HTTP_HOST="modwire.example",
            HTTP_X_FORWARDED_PROTO="https",
            **auth,
        )

        assert response.status_code == 200
        links = siren_links(response.json())
        assert links["self"].startswith("https://modwire.example/")
        assert links["service-desc"] == "https://modwire.example/api/openapi.json"


class TestHealthEndpoints:
    def test_health_endpoint_reports_database_readiness(self, client):
        response = client.get("/health/?format=json")

        assert response.status_code == 200
        assert response.json() == {"Database(alias='default')": "OK"}


class TestCatalogEndpoints:
    def test_languages_are_advertised_as_siren_collection_entities(self, client, auth):
        response = client.get("/api/languages", **auth)

        assert response.status_code == 200
        assert_siren(response)
        document = response.json()
        assert_classes(document, "collection", "language")
        assert_actions(document, ["list_languages"])
        languages = siren_embedded(document, "language")
        assert languages
        assert any(siren_properties(language)["id"] == "python" for language in languages)


class TestRecordEndpoints:
    def test_record_workspace_can_be_managed_and_searched_through_endpoints(self, client, auth):
        tag = create_tag(client, auth, "API")
        section = create_section(client, auth, tag_slugs=[tag["slug"]])
        record = create_record(client, auth, section["slug"], [tag["slug"]])

        assert tag["slug"] == "api"
        assert section["slug"] == "endpoint-docs"
        assert record["slug"] == "endpoint-docs/endpoint-intro"

        list_response = client.get(
            f"/api/records?limit=1&offset=0&tag={tag['slug']}",
            **auth,
        )
        assert list_response.status_code == 200
        assert_siren(list_response)
        records = list_response.json()
        assert_classes(records, "collection", "record")
        assert_actions(records, ["list_records", "create_record", "search_records"])
        assert {"self", "first", "next"}.issubset(siren_links(records))
        embedded_records = siren_embedded(records, "record")
        assert embedded_records
        assert siren_properties(embedded_records[0])["slug"] == record["slug"]

        get_response = client.get(f"/api/records/{record['slug']}", **auth)
        assert get_response.status_code == 200
        record_document = get_response.json()
        assert_classes(record_document, "record")
        assert_actions(record_document, ["get_record", "update_record", "delete_record"])
        assert {"self", "section", "tag"}.issubset(siren_links(record_document))

        _, patched = patch_json(
            client,
            f"/api/records/{record['slug']}",
            auth,
            {"description": "Updated through PATCH."},
        )
        assert siren_properties(patched)["description"] == "Updated through PATCH."

        search_response, search_document = post_json(
            client,
            "/api/records/search",
            auth,
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
        assert_siren(search_response)
        assert_classes(search_document, "record-search")
        assert_actions(search_document, ["search_records"])
        assert any(result["slug"] == record["slug"] for result in siren_properties(search_document)["results"])

        delete_response = client.delete(f"/api/records/{record['slug']}", **auth)
        assert delete_response.status_code == 204
        assert delete_response.content == b""

    def test_sections_and_tags_expose_full_endpoint_lifecycle(self, client, auth):
        tag = create_tag(client, auth, "Lifecycle")
        _, updated_tag = put_json(
            client,
            f"/api/tags/{tag['slug']}",
            auth,
            {"name": "Lifecycle", "description": "Replaced through PUT."},
        )
        assert siren_properties(updated_tag)["description"] == "Replaced through PUT."

        section = create_section(client, auth, "Lifecycle Section", [tag["slug"]])
        _, patched_section = patch_json(
            client,
            f"/api/sections/{section['slug']}",
            auth,
            {"description": "Patched through the API."},
        )
        assert siren_properties(patched_section)["description"] == "Patched through the API."

        section_list = client.get("/api/sections?limit=10&offset=0", **auth)
        assert section_list.status_code == 200
        assert_classes(section_list.json(), "collection", "section")
        assert_actions(section_list.json(), ["list_sections", "create_section"])

        assert client.delete(f"/api/sections/{section['slug']}", **auth).status_code == 204
        assert client.delete(f"/api/tags/{tag['slug']}", **auth).status_code == 204


class TestContentEndpoints:
    def test_record_content_blocks_expose_full_endpoint_lifecycle(self, client, auth):
        section = create_section(client, auth, "Content Docs")
        record = create_record(client, auth, section["slug"], section["tag_slugs"], title="Content Intro")

        _, created = post_json(
            client,
            "/api/contents",
            auth,
            {
                "record_slug": record["slug"],
                "position": 1,
                "role": "list",
                "content": ["First", "Second"],
                "language": "en",
                "metadata": {"source": "endpoint-test"},
            },
        )
        content = siren_properties(created)
        assert content["record_slug"] == record["slug"]
        assert content["role"] == "list"

        get_response = client.get(f"/api/contents/{content['id']}", **auth)
        assert get_response.status_code == 200
        assert_classes(get_response.json(), "content")
        assert_actions(get_response.json(), ["get_content", "update_content", "delete_content"])

        _, patched = patch_json(
            client,
            f"/api/contents/{content['id']}",
            auth,
            {"position": 2, "role": "paragraph", "content": "Moved.", "language": "en"},
        )
        assert siren_properties(patched)["position"] == 2
        assert siren_properties(patched)["content"] == "Moved."

        assert client.delete(f"/api/contents/{content['id']}", **auth).status_code == 204


class TestScaffoldingEndpoints:
    def test_scaffolding_bundle_schema_preview_and_convergence_are_endpoint_resources(self, client, auth):
        scaffolding = create_scaffolding(client, auth)

        _, variable = post_json(
            client,
            "/api/variables",
            auth,
            {
                "scaffolding_id": scaffolding["id"],
                "name": "project_name",
                "type": "str",
                "description": "Project display name.",
                "default_value": "World",
                "required": True,
            },
        )
        _, template = post_json(
            client,
            "/api/templates",
            auth,
            {
                "scaffolding_id": scaffolding["id"],
                "relative_path": "README.md",
                "file_content": "# {{ project_name }}",
                "write_mode": "managed",
            },
        )

        scaffolding_response = client.get(f"/api/scaffoldings/{scaffolding['id']}", **auth)
        assert scaffolding_response.status_code == 200
        assert_actions(
            scaffolding_response.json(),
            [
                "get_scaffolding",
                "get_scaffolding_schema",
                "get_scaffolding_bundle",
                "preview_scaffolding",
            ],
        )

        schema_response = client.get(f"/api/scaffoldings/{scaffolding['id']}/schema", **auth)
        assert schema_response.status_code == 200
        schema = schema_response.json()
        assert_classes(schema, "scaffolding-schema")
        assert "project_name" in siren_properties(schema)["properties"]
        assert siren_properties(schema)["required"] == ["project_name"]

        bundle_response = client.get(f"/api/scaffoldings/{scaffolding['id']}/bundle", **auth)
        assert bundle_response.status_code == 200
        bundle = bundle_response.json()
        assert_classes(bundle, "scaffolding-bundle")
        assert siren_properties(bundle)["variables"][0]["id"] == siren_properties(variable)["id"]
        assert siren_properties(bundle)["templates"][0]["id"] == siren_properties(template)["id"]

        _, preview = post_json(
            client,
            f"/api/scaffoldings/{scaffolding['id']}/preview",
            auth,
            {"values": {"project_name": "Ada"}, "template_overrides": []},
        )
        assert_classes(preview, "scaffolding-preview")
        assert siren_properties(preview)["files"][0]["path"] == "README.md"
        assert "Ada" in siren_properties(preview)["files"][0]["source"]

        _, convergence = post_json(
            client,
            "/api/scaffoldings/converge",
            auth,
            {
                "language_id": "python",
                "name": "Endpoint Convergence",
                "description": "Dry-run convergence through endpoint tests.",
                "variables": [
                    {
                        "name": "project_name",
                        "type": "str",
                        "description": "Project display name.",
                        "default_value": "World",
                        "required": True,
                    }
                ],
                "templates": [
                    {
                        "relative_path": "README.md",
                        "file_content": "# {{ project_name }}",
                        "write_mode": "managed",
                    }
                ],
                "dry_run": True,
            },
        )
        assert_classes(convergence, "scaffolding-convergence")
        assert siren_properties(convergence)["dry_run"] is True
        assert siren_properties(convergence)["plan"]["scaffolding"] == "create"

        assert client.delete(f"/api/templates/{siren_properties(template)['id']}", **auth).status_code == 204
        assert client.delete(f"/api/variables/{siren_properties(variable)['id']}", **auth).status_code == 204
        assert client.delete(f"/api/scaffoldings/{scaffolding['id']}", **auth).status_code == 204


class TestApiKeyEndpoints:
    def test_api_keys_can_be_created_rotated_listed_and_deleted_through_endpoints(self, client, auth):
        _, created = post_json(client, "/api/api_keys", auth, {"name": "child-key"})
        child = siren_properties(created)

        assert child["name"] == "child-key"
        assert "key" in child

        list_response = client.get("/api/api_keys", **auth)
        assert list_response.status_code == 200
        api_keys = list_response.json()
        assert_classes(api_keys, "collection", "api-key")
        assert_actions(api_keys, ["list_api_keys", "create_api_key"])
        assert any(siren_properties(entity)["id"] == child["id"] for entity in siren_embedded(api_keys, "api-key"))

        _, patched = patch_json(client, f"/api/api_keys/{child['id']}", auth, {"name": "renamed-key"})
        assert siren_properties(patched)["name"] == "renamed-key"

        get_response = client.get(f"/api/api_keys/{child['id']}", **auth)
        assert get_response.status_code == 200
        assert_classes(get_response.json(), "api-key")
        assert_actions(get_response.json(), ["get_api_key", "partial_update_api_key", "delete_api_key"])

        assert client.delete(f"/api/api_keys/{child['id']}", **auth).status_code == 204
