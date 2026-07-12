#!/bin/sh
set -eu

server_name="${MODWIRE_MCP_SERVER_NAME:-modwire}"
server_url="${MODWIRE_MCP_SERVER_URL:-http://127.0.0.1:8200/mcp}"
api_url="${MODWIRE_SCAFFOLDING_API_URL:-http://127.0.0.1:8100/api/}"
secret_path="${MCP_ADAPTER_API_KEY_FILE:-.dev/secrets/mcp-adapter-api-key}"

command -v codex >/dev/null
command -v curl >/dev/null
command -v docker >/dev/null

docker inspect modwire-records-postgres-1 >/dev/null
docker network inspect modwire-records_default >/dev/null
docker compose config --quiet
docker compose pull scaffolding-api mcp-adapter
docker compose up --detach --wait scaffolding-api

mkdir -p "$(dirname "${secret_path}")"
if ! test -s "${secret_path}" || ! curl --fail --silent --output /dev/null \
  --header "apikey: $(cat "${secret_path}" 2>/dev/null || true)" \
  --header "Accept: application/vnd.siren+json" \
  "${api_url}"; then
    temporary_secret="$(mktemp "${secret_path}.XXXXXX")"
    trap 'rm -f "${temporary_secret}"' EXIT HUP INT TERM
    docker compose exec -T scaffolding-api python manage.py shell --no-imports -c \
      'from tokens.models.api_key import ApiKey; _, key = ApiKey.generate("local-mcp-adapter"); print(key)' \
      >"${temporary_secret}"
    test -s "${temporary_secret}"
    chmod 600 "${temporary_secret}"
    mv "${temporary_secret}" "${secret_path}"
    trap - EXIT HUP INT TERM
fi

chmod 600 "${secret_path}"
docker compose up --detach --wait mcp-adapter
uv run python scripts/check-mcp-adapter.py >/dev/null

if codex mcp get "${server_name}" --json >/dev/null 2>&1; then
    codex mcp remove "${server_name}" >/dev/null
fi
codex mcp add "${server_name}" --url "${server_url}" >/dev/null

printf 'Modwire MCP is healthy at %s and registered in Codex as %s.\n' \
  "${server_url}" "${server_name}"
printf '%s\n' 'Start a new Codex session to load its tools.'
