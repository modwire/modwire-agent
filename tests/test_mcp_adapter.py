import asyncio
import json

import httpx
import pytest

from mcp_adapter.scaffoldings import (
    ScaffoldingCapabilities,
    ScaffoldingCreate,
    ScaffoldingUpdate,
    TemplateCreate,
    TemplateUpdate,
    VariableCreate,
)
from mcp_adapter.server import create_server
from mcp_adapter.settings import AdapterSettings
from mcp_adapter.siren import AdapterError

SCAFFOLDING_ID = "brNlYVlASiK8LKLHNCv15A"
LANGUAGE_ID = "2lURS3VRR-SRV5ye7CGTzA"
TEMPLATE_ID = "t3mPLatE00000000000000"


def test_adapter_traverses_advertised_links_and_actions():
    requested = []

    def handler(request: httpx.Request):
        requested.append((request.method, str(request.url)))
        documents = {
            "http://api.test/root": {
                "links": [{"rel": ["scaffoldings"], "href": "http://api.test/catalog"}],
            },
            "http://api.test/catalog": {
                "properties": {"count": 1},
                "entities": [
                    {
                        "properties": {
                            "id": SCAFFOLDING_ID,
                            "language": LANGUAGE_ID,
                            "name": "Modwire Python Package",
                            "description": "Package boundaries.",
                        },
                        "links": [{"rel": ["self"], "href": "http://api.test/items/modwire"}],
                    }
                ],
                "actions": [
                    {
                        "name": "list_scaffoldings",
                        "method": "GET",
                        "href": "http://api.test/catalog",
                    }
                ],
            },
            "http://api.test/items/modwire": {
                "properties": {"id": SCAFFOLDING_ID},
                "actions": [
                    {
                        "name": "get_scaffolding_schema",
                        "method": "GET",
                        "href": "http://api.test/forms/modwire",
                    },
                    {
                        "name": "get_scaffolding_bundle",
                        "method": "GET",
                        "href": "http://api.test/archives/modwire",
                    },
                    {
                        "name": "preview_scaffolding",
                        "method": "POST",
                        "href": "http://api.test/render/modwire",
                    },
                ],
            },
            "http://api.test/forms/modwire": {
                "properties": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {
                        "package_name": {
                            "type": "string",
                            "description": "Import package.",
                            "default": "",
                        }
                    },
                    "required": ["package_name"],
                    "additionalProperties": False,
                }
            },
        }
        if str(request.url) == "http://api.test/render/modwire":
            assert json.loads(request.content) == {
                "values": {"package_name": "example"},
                "template_overrides": [],
            }
            return httpx.Response(
                200,
                json={
                    "properties": {
                        "files": [
                            {
                                "template_id": SCAFFOLDING_ID,
                                "path": "src/example/__init__.py",
                                "source": "",
                                "html": "\n",
                                "language": "python",
                                "write_mode": "managed",
                            }
                        ]
                    }
                },
            )
        return httpx.Response(200, json=documents[str(request.url)])

    capabilities = ScaffoldingCapabilities(
        "http://api.test/root",
        "secret",
        transport_factory=lambda: httpx.MockTransport(handler),
    )

    listed = asyncio.run(capabilities.list_scaffoldings())
    schema = asyncio.run(capabilities.schema(SCAFFOLDING_ID))
    preview = asyncio.run(capabilities.preview(SCAFFOLDING_ID, {"package_name": "example"}, []))
    advertised = asyncio.run(capabilities.advertised_capabilities())

    assert listed.scaffoldings[0].name == "Modwire Python Package"
    assert schema.required == ["package_name"]
    assert preview.files[0].path == "src/example/__init__.py"
    assert advertised == [
        "list_scaffoldings",
        "get_scaffolding_schema",
        "get_scaffolding_bundle",
        "preview_scaffolding",
    ]
    assert ("GET", "http://api.test/forms/modwire") in requested
    assert ("POST", "http://api.test/render/modwire") in requested


def test_adapter_preserves_api_problem_details():
    def handler(_: httpx.Request):
        return httpx.Response(
            422,
            json={
                "type": "https://modwire.dev/problems/preview",
                "title": "Preview failed",
                "detail": "A required variable is missing.",
                "errors": [{"code": "required_variable", "message": "package_name is required"}],
            },
        )

    capabilities = ScaffoldingCapabilities(
        "http://api.test/root",
        "secret",
        transport_factory=lambda: httpx.MockTransport(handler),
    )

    with pytest.raises(AdapterError) as raised:
        asyncio.run(capabilities.list_scaffoldings())

    assert raised.value.payload["status"] == 422
    assert raised.value.payload["body"]["errors"][0]["code"] == "required_variable"


def test_adapter_updates_scaffolding_and_owned_template_through_advertised_actions():
    def handler(request: httpx.Request):
        url = str(request.url)
        if url == "http://api.test/root":
            return httpx.Response(
                200,
                json={
                    "links": [
                        {"rel": ["scaffoldings"], "href": "http://api.test/scaffoldings"},
                        {"rel": ["templates"], "href": "http://api.test/templates"},
                    ]
                },
            )
        if url == "http://api.test/scaffoldings":
            return httpx.Response(
                200,
                json={
                    "entities": [
                        {
                            "properties": {
                                "id": SCAFFOLDING_ID,
                                "language": LANGUAGE_ID,
                            },
                            "links": [{"rel": ["self"], "href": "http://api.test/scaffoldings/modwire"}],
                        }
                    ]
                },
            )
        if url == "http://api.test/scaffoldings/modwire" and request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "properties": {"id": SCAFFOLDING_ID, "language": LANGUAGE_ID},
                    "actions": [
                        {
                            "name": "update_scaffolding",
                            "method": "PUT",
                            "href": "http://api.test/scaffoldings/modwire",
                        }
                    ],
                },
            )
        if url == "http://api.test/scaffoldings/modwire" and request.method == "PUT":
            assert json.loads(request.content) == {
                "language_id": LANGUAGE_ID,
                "name": "Modwire Python Repository",
                "description": "Canonical repository architecture.",
            }
            return httpx.Response(
                200,
                json={
                    "properties": {
                        "id": SCAFFOLDING_ID,
                        "language": LANGUAGE_ID,
                        "name": "Modwire Python Repository",
                        "description": "Canonical repository architecture.",
                    }
                },
            )
        if url == "http://api.test/templates":
            return httpx.Response(
                200,
                json={
                    "entities": [
                        {
                            "properties": {"id": TEMPLATE_ID},
                            "links": [{"rel": ["self"], "href": "http://api.test/templates/config"}],
                        }
                    ]
                },
            )
        if url == "http://api.test/templates/config" and request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "properties": {
                        "id": TEMPLATE_ID,
                        "scaffolding": SCAFFOLDING_ID,
                    },
                    "actions": [
                        {
                            "name": "update_template",
                            "method": "PUT",
                            "href": "http://api.test/templates/config",
                        }
                    ],
                },
            )
        assert request.method == "PUT"
        assert json.loads(request.content) == {
            "scaffolding_id": SCAFFOLDING_ID,
            "relative_path": ".modwire/boundaries.yaml",
            "file_content": "rules: []\n",
            "write_mode": "managed",
        }
        return httpx.Response(
            200,
            json={
                "properties": {
                    "id": TEMPLATE_ID,
                    "scaffolding": SCAFFOLDING_ID,
                    "relative_path": ".modwire/boundaries.yaml",
                    "file_content": "rules: []\n",
                    "write_mode": "managed",
                }
            },
        )

    capabilities = ScaffoldingCapabilities(
        "http://api.test/root",
        "secret",
        transport_factory=lambda: httpx.MockTransport(handler),
    )

    scaffolding = asyncio.run(
        capabilities.update(
            SCAFFOLDING_ID,
            ScaffoldingUpdate(
                name="Modwire Python Repository",
                description="Canonical repository architecture.",
            ),
        )
    )
    template = asyncio.run(
        capabilities.update_template(
            TemplateUpdate(
                scaffolding_id=SCAFFOLDING_ID,
                template_id=TEMPLATE_ID,
                relative_path=".modwire/boundaries.yaml",
                file_content="rules: []\n",
                write_mode="managed",
            )
        )
    )

    assert scaffolding.name == "Modwire Python Repository"
    assert template.write_mode == "managed"


def test_adapter_creates_complete_scaffolding_through_collection_actions():
    requests = []

    def handler(request: httpx.Request):
        url = str(request.url)
        if url == "http://api.test/root":
            return httpx.Response(
                200,
                json={
                    "links": [
                        {"rel": ["scaffoldings"], "href": "http://api.test/scaffoldings"},
                        {"rel": ["variables"], "href": "http://api.test/variables"},
                        {"rel": ["templates"], "href": "http://api.test/templates"},
                    ]
                },
            )
        if request.method == "GET":
            action = {
                "http://api.test/scaffoldings": "create_scaffolding",
                "http://api.test/variables": "create_variable",
                "http://api.test/templates": "create_template",
            }[url]
            return httpx.Response(
                200,
                json={"actions": [{"name": action, "method": "POST", "href": url}]},
            )
        payload = json.loads(request.content)
        requests.append((url, payload))
        if url.endswith("/scaffoldings"):
            properties = {
                "id": SCAFFOLDING_ID,
                "language": LANGUAGE_ID,
                "name": payload["name"],
                "description": payload["description"],
            }
        elif url.endswith("/variables"):
            properties = {
                "id": TEMPLATE_ID,
                "scaffolding": SCAFFOLDING_ID,
                **{key: value for key, value in payload.items() if key != "scaffolding_id"},
            }
        else:
            properties = {
                "id": TEMPLATE_ID,
                "scaffolding": SCAFFOLDING_ID,
                **{key: value for key, value in payload.items() if key != "scaffolding_id"},
            }
        return httpx.Response(200, json={"properties": properties})

    capabilities = ScaffoldingCapabilities(
        "http://api.test/root",
        "secret",
        transport_factory=lambda: httpx.MockTransport(handler),
    )

    created = asyncio.run(
        capabilities.create(
            ScaffoldingCreate(
                language_id=LANGUAGE_ID,
                name="Modwire Python Repository",
                description="Canonical repository architecture.",
            )
        )
    )
    variable = asyncio.run(
        capabilities.create_variable(
            VariableCreate(
                scaffolding_id=SCAFFOLDING_ID,
                name="package_name",
                type="str",
                description="Import package.",
                default_value="",
                required=True,
            )
        )
    )
    template = asyncio.run(
        capabilities.create_template(
            TemplateCreate(
                scaffolding_id=SCAFFOLDING_ID,
                relative_path=".modwire/shape.yaml",
                file_content="{}\n",
            )
        )
    )

    assert created.id == SCAFFOLDING_ID
    assert variable.name == "package_name"
    assert template.write_mode == "managed"
    assert tuple(url for url, _ in requests) == (
        "http://api.test/scaffoldings",
        "http://api.test/variables",
        "http://api.test/templates",
    )


def test_server_exposes_only_typed_scaffolding_tools(tmp_path):
    key_file = tmp_path / "api-key"
    key_file.write_text("secret")
    server = create_server(
        AdapterSettings(
            api_url="http://api.test/root",
            api_key_file=key_file,
        )
    )

    tools = {tool.name: tool for tool in asyncio.run(server.list_tools())}

    assert set(tools) == {
        "list_scaffoldings",
        "get_scaffolding_schema",
        "get_scaffolding_bundle",
        "preview_scaffolding",
        "update_scaffolding",
        "update_scaffolding_template",
        "create_scaffolding",
        "create_scaffolding_variable",
        "create_scaffolding_template",
    }
    preview_schema = tools["preview_scaffolding"].inputSchema
    assert set(preview_schema["properties"]) == {
        "scaffolding_id",
        "values",
        "template_overrides",
    }
    assert preview_schema["properties"]["scaffolding_id"]["pattern"] == "^[A-Za-z0-9_-]{22}$"
    assert preview_schema["properties"]["template_overrides"]["type"] == "array"
