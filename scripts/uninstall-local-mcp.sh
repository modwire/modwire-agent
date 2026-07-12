#!/bin/sh
set -eu

server_name="${MODWIRE_MCP_SERVER_NAME:-modwire}"

if codex mcp get "${server_name}" --json >/dev/null 2>&1; then
    codex mcp remove "${server_name}"
fi

docker compose down --remove-orphans

printf '%s\n' 'Removed the Codex entry and runtime containers.'
printf '%s\n' 'The PostgreSQL container, external network, volume, data, and dedicated API identity were preserved.'
