# Working rules

- Keep each Django API module under `src/enclosure` split into domain, ports, use cases, and adapters.
- Keep domain and use-case code independent of concrete adapters; let application-level autowiring bind concrete implementations to ports.
- Preserve public HTTP and OpenAPI behavior. Give every new API operation a unique, stable `operation_id` and test observable responses.
- Use documentation comments only for public REST API documentation; do not add comments or docstrings elsewhere in code.
- Do not change migrations, runtime/database configuration, or GitHub workflows unless an explicit rollout requires it.
- Keep documentation focused on readers' tasks rather than implementation inventories.
- Run local CLI commands in host mode, or with privileges equivalent to the user's environment.
