# Quality loop

1. Read the relevant local guidance and inspect the affected module before changing code.
2. Make the smallest coherent change that preserves the HTTP/OpenAPI contract.
3. Run `uv run ruff check .` and the relevant `uv run pytest` coverage.
4. Run `make modwire` when changing module boundaries, imports, or autowiring; resolve reported violations before review.

The Make target runs Modwire against `src` with the Python language configuration. Use host mode for local commands when the environment offers it.
