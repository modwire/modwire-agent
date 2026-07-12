import asyncio
import json

import httpx
import pytest

from mcp_adapter.scaffoldings import ScaffoldingCapabilities
from mcp_adapter.server import create_server
from mcp_adapter.settings import AdapterSettings
from mcp_adapter.siren import AdapterError

SCAFFOLDING_ID = "brNlYVlASiK8LKLHNCv15A"
LANGUAGE_ID = "2lURS3VRR-SRV5ye7CGTzA"


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
    }
    preview_schema = tools["preview_scaffolding"].inputSchema
    assert set(preview_schema["properties"]) == {
        "scaffolding_id",
        "values",
        "template_overrides",
    }
    assert preview_schema["properties"]["scaffolding_id"]["pattern"] == "^[A-Za-z0-9_-]{22}$"
    assert preview_schema["properties"]["template_overrides"]["type"] == "array"
