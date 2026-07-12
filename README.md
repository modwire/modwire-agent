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
