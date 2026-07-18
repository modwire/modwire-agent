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
            print(f"MCP adapter has {len(tool_names)} tools.")


if __name__ == "__main__":
    asyncio.run(check())
