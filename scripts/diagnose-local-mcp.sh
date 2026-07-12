#!/bin/sh
set -eu

secret_path="${MCP_ADAPTER_API_KEY_FILE:-.dev/secrets/mcp-adapter-api-key}"
api_url="${MODWIRE_SCAFFOLDING_API_URL:-http://127.0.0.1:8100/api/}"

docker inspect modwire-records-postgres-1 >/dev/null
printf '%s\n' 'container/database: PostgreSQL container exists'

docker compose exec -T scaffolding-api python manage.py shell --no-imports -c \
  'from django.db import connection; cursor = connection.cursor(); cursor.execute("SELECT 1"); assert cursor.fetchone() == (1,)' \
  >/dev/null
printf '%s\n' 'database: connection is healthy'

curl --fail --silent --output /dev/null http://127.0.0.1:8100/health/
printf '%s\n' 'scaffolding-api: health endpoint is reachable'

test -s "${secret_path}"
curl --fail --silent --output /dev/null \
  --header "apikey: $(cat "${secret_path}")" \
  --header "Accept: application/vnd.siren+json" \
  "${api_url}"
printf '%s\n' 'api-authentication: dedicated key is accepted'

curl --fail --silent --output /dev/null http://127.0.0.1:8200/health
printf '%s\n' 'siren-adapter: API traversal and capability discovery are healthy'

uv run python scripts/check-mcp-adapter.py >/dev/null
printf '%s\n' 'mcp-transport: all four tools pass the protocol smoke workflow'

codex mcp get "${MODWIRE_MCP_SERVER_NAME:-modwire}" --json >/dev/null
printf '%s\n' 'codex-config: Modwire MCP server is registered'
