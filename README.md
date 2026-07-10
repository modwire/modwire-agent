# New Project

Django API scaffold with JSON logs, dotenv settings, health checks, and auto-discovered Django Ninja Extra controllers.

```sh
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

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
