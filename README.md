# New Project

Django API scaffold with JSON logs, dotenv settings, health checks, and auto-discovered Django Ninja Extra controllers.

```sh
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

## Isolated scaffolding API

The container runtime reuses the existing PostgreSQL state; it does not create
or own a database service or volume. It reuses the host `DATABASE_URL` already
in the ignored `.env` file. Compose overrides only its network address to
`postgres:5432` because the API joins the external
`modwire-records_default` Docker network. The host configuration remains on
`localhost:5433`; credentials have one source of truth.

Released runtime images are pulled from GHCR. The default is `latest`; pin both
services to one immutable release with `MODWIRE_MCP_VERSION`, for example:

```sh
MODWIRE_MCP_VERSION=0.2.0 make mcp-up
```

Each GitHub release publishes `linux/amd64` and `linux/arm64` variants of
`ghcr.io/modwire/modwire-mcp-runtime` and
`ghcr.io/modwire/modwire-mcp-adapter`. Docker selects the matching image on
Intel Linux, Intel macOS, or Apple Silicon macOS hosts. Local image builds are
an explicit development mode and never occur during normal installation:

```sh
make runtime-build-up
make mcp-build-up
```

Validate and start only the API:

```sh
make runtime-config
make runtime-up
curl --fail http://127.0.0.1:8100/health/
```

Container startup never applies migrations. Before a migration, create a
PostgreSQL backup and capture the exact Django migration plan:

```sh
make runtime-db-prepare
```

Review both paths printed by that command. Apply the reviewed plan only by
passing those same artifacts through the guarded command:

```sh
CONFIRM_EXISTING_DATABASE_MIGRATION=reviewed \
MODWIRE_DATABASE_BACKUP=.dev/database-safety/modwire-records-TIMESTAMP.dump \
MODWIRE_DATABASE_MIGRATION_PLAN=.dev/database-safety/migration-plan-TIMESTAMP.txt \
make runtime-db-migrate
```

`make runtime-down` removes the API container only. The external PostgreSQL
container, network, and `modwire-records_postgres_data` volume are untouched.

For non-container development, keep using the host `DATABASE_URL` (currently
the host-side PostgreSQL port) with the original `uv run` commands above. Its
default HTTP port remains `8000`, separate from the container runtime on
`8100`.

## MCP scaffolding adapter

The MCP adapter is a separate stateless service. It discovers the scaffolding
collection from the Siren API root and executes only actions advertised by the
canonical scaffold resource. It does not import Django or Modwire CLI modules,
mount a workspace, connect to PostgreSQL, or construct scaffolding routes.
Its image uses a separate dependency group and contains neither the Django
application nor its database dependencies.

Place a dedicated API key in the ignored file configured by
`MCP_ADAPTER_API_KEY_FILE` (the default is
`.dev/secrets/mcp-adapter-api-key`), then start both isolated services:

```sh
make mcp-up
make mcp-health
make mcp-check
```

The Streamable HTTP endpoint is `http://127.0.0.1:8200/mcp`. The health
endpoint reports the adapter version, API reachability, and the number of
relations and actions advertised at the Siren root without returning the API
key. The adapter exposes one stable tool, `modwire`, with two operations:

- `inspect` follows a path of advertised Siren relations and collection items;
- `execute` follows the same kind of path and submits values to an action
  advertised by the selected resource.

For example, inspect the scaffolding collection with:

```json
{
  "request": {
    "kind": "inspect",
    "path": [{"kind": "relation", "relation": "scaffoldings"}]
  }
}
```

The returned Siren document supplies item identities, links, actions, and
runtime field schemas. Clients inspect those controls before choosing the next
step. Adding an API capability therefore does not alter the MCP tool catalog or
require another MCP client restart or tool-schema discovery cycle.

The `services` Docker network is internal. `mcp-adapter` uses it to reach the
API and joins a separate edge bridge for its loopback-published MCP port.
`scaffolding-api` alone bridges the internal service network to the external
PostgreSQL network, so the adapter has no database route.

### Install for Codex

Run the host installer from this checkout:

```sh
make mcp-install
```

The installer verifies the existing PostgreSQL container and network, pulls
and starts the released runtime images, creates a dedicated API key only when
the ignored local secret is missing or invalid, runs the complete MCP smoke
workflow, and registers one global Codex entry named `modwire` at
`http://127.0.0.1:8200/mcp`. The key value is redirected directly into a
mode-600 ignored file and is not printed. Re-running the installer preserves
the same API identity while the secret remains valid.

Codex loads MCP configuration when a session starts. Open a new session once
after installing this one-tool adapter; subsequent API capability additions are
discovered through Siren without another session restart. Diagnose each runtime
layer independently with:

```sh
make mcp-diagnose
```

Uninstall only the Codex entry and these runtime containers with:

```sh
make mcp-uninstall
```

Uninstall never passes Docker's `--volumes` option. It preserves
`modwire-records-postgres-1`, `modwire-records_default`,
`modwire-records_postgres_data`, all scaffolding records, and the dedicated API
identity for a later reinstall.

### Future CLI runner

Workspace mutation is intentionally absent from this installation. A future
optional `cli-runner` profile will package `modwire-cli` separately and mount
only an explicitly selected workspace. The MCP adapter will call that
capability through its contract; it will not import CLI internals or gain a
workspace mount itself. Scaffolding discovery, bundles, and previews do not
depend on the CLI runner.

## Hypermedia API browser

The authenticated API entry point is `GET /api/`. Successful API responses use
the Siren media type (`application/vnd.siren+json`) and advertise the links and
actions that are valid for the current resource. Clients can start with one URL
and traverse relations instead of constructing endpoint URLs:

```sh
curl -H "apikey: $MODWIRE_API_KEY" -H "Accept: application/vnd.siren+json" http://localhost:8000/api/
```

Build the React browser and then open `http://localhost:8000/browser/`:

```sh
cd browser
npm install
npm run build
cd ..
uv run python manage.py runserver
```

For frontend development, run Django on port 8000 and `npm run dev` in
`browser/`; Vite proxies `/api` to Django. The browser prompts for an API key and
stores it only in the current tab's `sessionStorage`.
