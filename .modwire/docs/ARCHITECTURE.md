# Architecture configuration

`architecture.yaml` describes the source-tree boundaries and structural limits that Modwire checks. In this project it covers the Django API under `src/enclosure`.

## Tags

Each tag gives a source-tree pattern a meaningful name. `module` matches every operational module directly below `src/enclosure`, excluding only the root package files and technical `core` package. Adding a module therefore requires no configuration change.

The configuration separates every module into `domain`, `ports`, `use_cases`, and `adapters`. Dependency registration is discovered from the application-level `autowiring.py`; it is not an architectural layer or module realm.

| Source | Allowed dependencies |
| --- | --- |
| Domain | May not depend on ports, use cases, or adapters |
| Ports | May not depend on use cases or adapters |
| Use cases | May not depend on adapters |
| Adapters | May depend inward through the layered flow |
| `manage.py` and `tests/` | The framework and application contexts needed to bootstrap and exercise public behavior |

The `backward-flow`, cycle, and re-entry analyzers enforce the generic module and layer map. Keep any cross-module integration narrow and explicit in code.

The Django entry point, application autowiring, and `tests/` are mapped as support realms. Their explicit allowances let them bootstrap and exercise the API without widening production context boundaries.

## Rules and flow

The project flow orders layers as `adapters`, `use_cases`, `ports`, then `domain`. Keep dependencies moving inward: domain code is framework-free, use cases depend on ports, and adapters implement those ports. The application-level discovery rules bind concrete adapters to their ports.

When adding a module, preserve the same layer layout; matching services are discovered automatically. Run `make modwire` whenever imports, autowiring, or module boundaries change. The `shape` section is maintained by Modwire; do not edit the marked managed block manually.
