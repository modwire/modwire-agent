# Testing

Tests live under `tests/`, grouped by module. Functional API scenarios cover the Django REST endpoints, while `tests/siren/functional` covers the Siren representation.

Test public interfaces and observable outcomes: HTTP status, payload, headers, OpenAPI operations, files, or exit codes. When adding an API operation, cover its public response and keep its `operation_id` stable.

Organize scenarios in Auntie order where it helps: attacks, invariants, interruption, cleanup, recovery, then happy paths. Run focused tests while developing, then run `uv run pytest` before handoff. Run `uv run ruff check .` alongside the test suite.
