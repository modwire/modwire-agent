import json
from pathlib import Path

MCP_TOOL_NAMES = frozenset(
    json.loads(Path(__file__).with_name("tool-contract.json").read_text())
)
