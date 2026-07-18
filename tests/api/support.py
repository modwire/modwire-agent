import json
from collections.abc import Iterable


class ApiSession:
    def __init__(self, client, auth: dict | None = None):
        self.client = client
        self.auth = auth or {}

    def get(self, path: str, *, expected: int = 200, **headers):
        return self._request("get", path, expected=expected, headers=headers)

    def post(self, path: str, payload: dict | None = None, *, expected: int = 200, **headers):
        return self._request("post", path, payload, expected=expected, headers=headers)

    def put(self, path: str, payload: dict, *, expected: int = 200, **headers):
        return self._request("put", path, payload, expected=expected, headers=headers)

    def patch(self, path: str, payload: dict, *, expected: int = 200, **headers):
        return self._request("patch", path, payload, expected=expected, headers=headers)

    def delete(self, path: str, *, expected: int = 204, **headers):
        return self._request("delete", path, expected=expected, headers=headers)

    def _request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        *,
        expected: int,
        headers: dict,
    ):
        request = getattr(self.client, method)
        kwargs = self.auth | headers
        if payload is not None:
            kwargs.update(data=json.dumps(payload), content_type="application/json")
        response = request(path, **kwargs)
        assert response.status_code == expected, response.content
        return response


class SirenDocument:
    def __init__(self, response):
        self.response = response
        self.body = {} if response.status_code == 204 else response.json()

    @property
    def properties(self) -> dict:
        return self.body.get("properties", {})

    @property
    def links(self) -> dict[str, str]:
        return {
            rel: link["href"]
            for link in self.body.get("links", [])
            for rel in link.get("rel", [])
        }

    @property
    def action_names(self) -> set[str]:
        return {action["name"] for action in self.body.get("actions", [])}

    def embedded(self, *classes: str) -> list[dict]:
        wanted = set(classes)
        return [
            entity
            for entity in self.body.get("entities", [])
            if wanted.issubset(set(entity.get("class", [])))
        ]

    def embedded_properties(self, *classes: str) -> list[dict]:
        return [entity.get("properties", {}) for entity in self.embedded(*classes)]

    def assert_siren(self):
        assert self.response["Content-Type"].startswith("application/vnd.siren+json")
        return self

    def assert_problem(self):
        assert self.response["Content-Type"].startswith("application/problem+json")
        assert self.body["status"] == self.response.status_code
        return self

    def assert_classes(self, *classes: str):
        assert set(classes).issubset(set(self.body.get("class", [])))
        return self

    def assert_actions(self, names: Iterable[str]):
        assert set(names).issubset(self.action_names)
        return self


class EndpointAssertions:
    def api(self, client, auth: dict | None = None) -> ApiSession:
        return ApiSession(client, auth)

    def siren(self, response) -> SirenDocument:
        return SirenDocument(response).assert_siren()

    def problem(self, response) -> SirenDocument:
        return SirenDocument(response).assert_problem()


class RecordResourceFactory(EndpointAssertions):
    def tag_payload(self, name: str = "Endpoint API") -> dict:
        return {"name": name, "description": "Created through the HTTP API."}

    def create_tag(self, api: ApiSession, name: str = "Endpoint API") -> dict:
        return self.siren(api.post("/api/tags", self.tag_payload(name))).properties

    def section_payload(self, title: str, tag_slugs: list[str]) -> dict:
        return {
            "title": title,
            "description": "Endpoint-only test section.",
            "tag_slugs": tag_slugs,
        }

    def create_section(self, api: ApiSession, title: str = "Endpoint Docs", tag_slugs: list[str] | None = None):
        tag_slugs = tag_slugs or [self.create_tag(api, f"{title} Tag")["slug"]]
        return self.siren(api.post("/api/sections", self.section_payload(title, tag_slugs))).properties

    def content_block(self, text: str = "Endpoint body") -> dict:
        return {
            "role": "paragraph",
            "content": text,
            "language": "en",
            "metadata": {"source": "endpoint-test"},
        }

    def record_payload(self, section_slug: str, tag_slugs: list[str], title: str = "Endpoint Intro") -> dict:
        return {
            "section_slug": section_slug,
            "title": title,
            "description": "Record created through the HTTP API.",
            "sources": ["https://example.test/source"],
            "tag_slugs": tag_slugs,
            "content": [self.content_block()],
        }

    def create_record(
        self,
        api: ApiSession,
        section_slug: str,
        tag_slugs: list[str],
        title: str = "Endpoint Intro",
    ) -> dict:
        return self.siren(api.post("/api/records", self.record_payload(section_slug, tag_slugs, title))).properties


class ScaffoldingResourceFactory(EndpointAssertions):
    def create_scaffolding(self, api: ApiSession, name: str = "Endpoint Scaffolding") -> dict:
        response = api.post(
            "/api/scaffoldings",
            {
                "language_id": "python",
                "name": name,
                "description": "Created through endpoint tests.",
            },
        )
        return self.siren(response).properties

    def create_variable(self, api: ApiSession, scaffolding_id: str, *, required: bool = True) -> dict:
        response = api.post(
            "/api/variables",
            {
                "scaffolding_id": scaffolding_id,
                "name": "project_name",
                "type": "str",
                "description": "Project display name.",
                "default_value": "World",
                "required": required,
            },
        )
        return self.siren(response).properties

    def create_template(self, api: ApiSession, scaffolding_id: str) -> dict:
        response = api.post(
            "/api/templates",
            {
                "scaffolding_id": scaffolding_id,
                "relative_path": "README.md",
                "file_content": "# {{ project_name }}",
                "write_mode": "managed",
            },
        )
        return self.siren(response).properties
