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

            listed = await session.call_tool("list_scaffoldings")
            _require_success(listed, "list_scaffoldings")
            scaffoldings = listed.structuredContent["scaffoldings"]
            modwire = next(
                item for item in scaffoldings if item["name"] == "Modwire Python Package"
            )

            schema = await session.call_tool(
                "get_scaffolding_schema",
                {"scaffolding_id": modwire["id"]},
            )
            bundle = await session.call_tool(
                "get_scaffolding_bundle",
                {"scaffolding_id": modwire["id"]},
            )
            preview = await session.call_tool(
                "preview_scaffolding",
                {
                    "scaffolding_id": modwire["id"],
                    "values": {
                        "module_name": "example",
                        "package_name": "example_package",
                    },
                },
            )
            invalid_preview = await session.call_tool(
                "preview_scaffolding",
                {
                    "scaffolding_id": modwire["id"],
                    "values": {},
                },
            )
            for name, result in (
                ("get_scaffolding_schema", schema),
                ("get_scaffolding_bundle", bundle),
                ("preview_scaffolding", preview),
            ):
                _require_success(result, name)
            problem_text = " ".join(
                block.text for block in invalid_preview.content if hasattr(block, "text")
            )
            if not invalid_preview.isError:
                raise RuntimeError("Invalid preview unexpectedly succeeded")
            if '"kind": "api-problem"' not in problem_text or "required_variable" not in problem_text:
                raise RuntimeError("MCP error did not preserve the API problem details")

            print(
                json.dumps(
                    {
                        "tools": sorted(tool_names),
                        "scaffolding_id": modwire["id"],
                        "required_values": schema.structuredContent["required"],
                        "bundle_templates": len(bundle.structuredContent["templates"]),
                        "preview_paths": [
                            item["path"] for item in preview.structuredContent["files"]
                        ],
                        "problem_details_preserved": True,
                    },
                    sort_keys=True,
                )
            )


def _require_success(result, tool_name: str) -> None:
    if result.isError:
        raise RuntimeError(f"MCP tool '{tool_name}' failed: {result.content}")
    if result.structuredContent is None:
        raise RuntimeError(f"MCP tool '{tool_name}' returned no structured content")


if __name__ == "__main__":
    asyncio.run(check())
