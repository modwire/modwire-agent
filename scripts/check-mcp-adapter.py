import asyncio
import json
import os
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_TOOL_NAMES = frozenset(
    json.loads(
        (Path(__file__).resolve().parents[1] / "mcp_adapter" / "tool-contract.json").read_text()
    )
)


async def check():
    url = os.getenv("MCP_ADAPTER_URL", "http://127.0.0.1:8200/mcp")
    async with streamable_http_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            available = await session.list_tools()
            tool_names = {tool.name for tool in available.tools}
            if tool_names != MCP_TOOL_NAMES:
                raise RuntimeError(f"Unexpected MCP tools: {sorted(tool_names)}")

            root = await _inspect(session, [])
            collection = await _inspect(
                session,
                [{"kind": "relation", "relation": "scaffoldings"}],
            )
            scaffold = next(
                entity
                for entity in collection["entities"]
                if entity["properties"]["name"] == "Modwire Python Repository"
            )
            scaffold_id = scaffold["properties"]["id"]
            item_path = [
                {"kind": "relation", "relation": "scaffoldings"},
                {"kind": "item", "identifier": scaffold_id},
            ]
            resource = await _inspect(session, item_path)
            action_names = {action["name"] for action in resource["actions"]}
            expected_actions = {"get_scaffolding_bundle", "preview_scaffolding"}
            if not expected_actions <= action_names:
                raise RuntimeError(
                    f"Scaffolding actions are missing: {sorted(expected_actions - action_names)}"
                )

            preview = await _execute(
                session,
                item_path,
                "preview_scaffolding",
                {
                    "values": {
                        "module_name": "example",
                        "package_name": "example_package",
                    },
                    "template_overrides": [],
                },
            )
            invalid_preview = await session.call_tool(
                "modwire",
                {
                    "request": {
                        "kind": "execute",
                        "path": item_path,
                        "action": "preview_scaffolding",
                        "values": {"values": {}, "template_overrides": []},
                    }
                },
            )
            problem_text = " ".join(
                block.text for block in invalid_preview.content if hasattr(block, "text")
            )
            if not invalid_preview.isError:
                raise RuntimeError("Invalid preview unexpectedly succeeded")
            if "required_variable" not in problem_text:
                raise RuntimeError("MCP error did not preserve the API problem details")

            print(
                json.dumps(
                    {
                        "tools": sorted(tool_names),
                        "root_relations": sorted(
                            rel
                            for link in root["links"]
                            for rel in link.get("rel", [])
                        ),
                        "scaffolding_id": scaffold_id,
                        "advertised_actions": sorted(action_names),
                        "preview_paths": [
                            item["path"] for item in preview["properties"]["files"]
                        ],
                        "problem_details_preserved": True,
                    },
                    sort_keys=True,
                )
            )


async def _inspect(session: ClientSession, path: list[dict]) -> dict:
    result = await session.call_tool(
        "modwire",
        {"request": {"kind": "inspect", "path": path}},
    )
    return _document(result, "inspect")


async def _execute(
    session: ClientSession,
    path: list[dict],
    action: str,
    values: dict,
) -> dict:
    result = await session.call_tool(
        "modwire",
        {
            "request": {
                "kind": "execute",
                "path": path,
                "action": action,
                "values": values,
            }
        },
    )
    return _document(result, action)


def _document(result, operation: str) -> dict:
    if result.isError:
        raise RuntimeError(f"MCP operation '{operation}' failed: {result.content}")
    if result.structuredContent is None:
        raise RuntimeError(f"MCP operation '{operation}' returned no structured content")
    return result.structuredContent["document"]


if __name__ == "__main__":
    asyncio.run(check())
