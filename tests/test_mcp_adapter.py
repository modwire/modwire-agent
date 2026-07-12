import asyncio
import json

import httpx
import pytest
from modwire_siren import SirenClientError

from mcp_adapter.contracts import MCP_TOOL_NAMES
from mcp_adapter.hypermedia import (
    ExecuteRequest,
    InspectRequest,
    ItemStep,
    ModwireHypermedia,
    RelationStep,
)
from mcp_adapter.server import create_server
from mcp_adapter.settings import AdapterSettings
from mcp_adapter.transport import HttpxSirenTransport


def test_one_tool_discovers_and_executes_a_new_advertised_action(tmp_path):
    requests = []

    def handler(request: httpx.Request):
        requests.append((request.method, str(request.url), request.content))
        documents = {
            ("GET", "http://api.test/root"): {
                "links": [{"rel": ["widgets"], "href": "/widgets"}],
            },
            ("GET", "http://api.test/widgets"): {
                "entities": [
                    {
                        "properties": {"id": "example"},
                        "links": [{"rel": ["self"], "href": "/widgets/example"}],
                    }
                ],
            },
            ("GET", "http://api.test/widgets/example"): {
                "properties": {"id": "example"},
                "actions": [
                    {
                        "name": "new_capability",
                        "method": "POST",
                        "href": "/widgets/example/commands",
                        "fields": [{"name": "enabled", "type": "checkbox"}],
                    }
                ],
            },
            ("POST", "http://api.test/widgets/example/commands"): {
                "properties": {"id": "example", "enabled": True},
                "links": [{"rel": ["self"], "href": "/widgets/example"}],
            },
        }
        key = request.method, str(request.url)
        if key == ("POST", "http://api.test/widgets/example/commands"):
            assert json.loads(request.content) == {"enabled": True}
        return httpx.Response(200, json=documents[key])

    hypermedia = driver(handler)
    path = (
        RelationStep(kind="relation", relation="widgets"),
        ItemStep(kind="item", identifier="example"),
    )

    inspected = asyncio.run(
        hypermedia.handle(InspectRequest(kind="inspect", path=path))
    )
    executed = asyncio.run(
        hypermedia.handle(
            ExecuteRequest(
                kind="execute",
                path=path,
                action="new_capability",
                values={"enabled": True},
            )
        )
    )

    assert inspected.document["actions"][0]["name"] == "new_capability"
    assert executed.document["properties"] == {"id": "example", "enabled": True}
    assert requests[-1][:2] == (
        "POST",
        "http://api.test/widgets/example/commands",
    )


def test_hypermedia_preserves_complete_api_problem_details():
    def handler(request: httpx.Request):
        if request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "actions": [
                        {
                            "name": "create_widget",
                            "method": "POST",
                            "href": "/widgets",
                        }
                    ]
                },
            )
        return httpx.Response(
            422,
            json={
                "title": "Validation failed",
                "detail": "name is required",
                "errors": [{"field": "name", "code": "required"}],
            },
        )

    with pytest.raises(SirenClientError) as raised:
        asyncio.run(
            driver(handler).handle(
                ExecuteRequest(
                    kind="execute",
                    action="create_widget",
                    values={},
                )
            )
        )

    assert raised.value.as_dict() == {
        "kind": "remote-problem",
        "detail": "name is required",
        "status": 422,
        "title": "Validation failed",
        "body": {
            "title": "Validation failed",
            "detail": "name is required",
            "errors": [{"field": "name", "code": "required"}],
        },
    }


def test_http_transport_rejects_non_object_json():
    transport = HttpxSirenTransport(
        "secret",
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json=["not", "a", "document"])
        ),
    )

    async def request():
        async with transport:
            return await transport.request("GET", "http://api.test/root")

    with pytest.raises(SirenClientError) as raised:
        asyncio.run(request())

    assert raised.value.kind == "invalid-transport-response"


def test_http_transport_represents_successful_no_content_response():
    transport = HttpxSirenTransport(
        "secret",
        transport=httpx.MockTransport(lambda _: httpx.Response(204)),
    )

    async def request():
        async with transport:
            return await transport.request("DELETE", "http://api.test/widgets/example")

    response = asyncio.run(request())

    assert response.status_code == 204
    assert response.document == {
        "class": ["result"],
        "properties": {"status": 204},
        "links": [],
        "actions": [],
    }


def test_server_exposes_one_stable_discriminated_tool(tmp_path):
    key_file = tmp_path / "api-key"
    key_file.write_text("secret")
    server = create_server(
        AdapterSettings(
            api_url="http://api.test/root",
            api_key_file=key_file,
        ),
        transport_factory=factory(
            lambda _: httpx.Response(200, json={"links": [], "actions": []})
        ),
    )

    tools = {tool.name: tool for tool in asyncio.run(server.list_tools())}

    assert set(tools) == MCP_TOOL_NAMES == {"modwire"}
    schema = tools["modwire"].inputSchema
    assert set(schema["properties"]) == {"request"}
    assert schema["required"] == ["request"]
    request_schema = schema["properties"]["request"]
    assert request_schema["discriminator"]["propertyName"] == "kind"
    assert len(request_schema["oneOf"]) == 2


def driver(handler) -> ModwireHypermedia:
    return ModwireHypermedia("http://api.test/root", factory(handler))


def factory(handler):
    transport = httpx.MockTransport(handler)
    return lambda: HttpxSirenTransport("secret", transport=transport)
