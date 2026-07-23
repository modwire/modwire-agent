# modwire-agent

## Architecture

- This is a Django API organised as modules under `src/modwire`.
- Keep domain, ports, use cases, and adapters separate. Depend on ports from
  use cases; bind concrete adapters only in a module's `wiring.py`.
- Preserve the public HTTP/OpenAPI contract. Give every new API operation a
  unique, stable `operation_id` and test observable responses.

## Checks

Run the relevant checks before handing off:

```sh
uv run ruff check .
uv run pytest
```

Run `make modwire` when changing module boundaries, imports, or wiring.

## Safety

- Do not change migrations, runtime/database configuration, or GitHub
  workflows without an explicit rollout need.
- Keep `AGENTS.md` concise and change it only when the task explicitly calls
  for instruction updates.
