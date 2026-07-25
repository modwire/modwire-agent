# Architecture configuration

`architecture.yaml` describes the source-tree boundaries and structural limits that Modwire checks. In this project it covers the Django API under `src/modwire`.

## Tags

Each tag gives a source-tree pattern a meaningful name. Here, `module` matches operational modules such as `records`, `plans`, `languages`, `scaffoldings`, and `tokens`; `core` is shared application infrastructure; and `modwire_hex` is the framework dependency.

The configuration separates each module into `domain`, `ports`, `use_cases`, `adapters`, and `wiring`. It maps the current bounded contexts explicitly: `languages`, `plans`, `records`, `scaffoldings`, and `tokens`.

| Source | Allowed dependencies |
| --- | --- |
| Any operational module | Its own module, `core`, and the framework |
| `scaffoldings` | The above, plus `languages` |
| `core` | The framework and the `scaffoldings` preview error used by the API error boundary |
| Root wiring | The framework and each operational context |
| `manage.py` and `tests/` | The framework and application contexts needed to bootstrap and exercise public behavior |

All other cross-context imports are denied. The `module-boundaries` analyzer enforces this map; add a narrow, documented allowance only when a new integration is intentional.

The Django entry point and `tests/` are mapped as support realms. Their explicit allowances let them bootstrap and exercise the API without widening production context boundaries.

## Rules and flow

The project flow orders layers as `wiring`, `adapters`, `use_cases`, `ports`, then `domain`. Keep dependencies moving inward: domain code is framework-free, use cases depend on ports, and adapters implement those ports. Bind concrete adapters only in a module's `wiring.py`.

When adding a module, add its boundary tags and preserve the same layer layout before relying on it from root wiring. Run `make modwire` whenever imports, wiring, or module boundaries change. The `shape` section is maintained by Modwire; do not edit the marked managed block manually.
