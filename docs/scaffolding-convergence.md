# Modwire repository scaffold convergence

The production scaffold identity consumed by the architecture-dogfood train is
`brNlYVlASiK8LKLHNCv15A` (`Modwire Python Repository`). The executable contract
snapshot is stored in `tests/fixtures/modwire-python-repository.yaml`.

Convergence validates the complete scaffolding, variable, and template aggregate
before writing. A dry-run returns the same deterministic change plan without a
database mutation. Apply recalculates that plan while holding a database lock and
reconciles the aggregate in one transaction. It never receives a workspace path
and cannot modify repository files.

## Shared invariants

Every operational Python package preview contains managed `.modwire/boundaries.yaml`
and `.modwire/shape.yaml` files. Module and `shared` initializers use
`create_if_missing`, so adoption does not replace existing application source.

## Adoption deltas

| Target | Preview values | Expected delta |
| --- | --- | --- |
| Core | `modwire` / `architecture` | Both initializers and both configuration files already exist. Review the managed configuration diff; source initializers remain untouched. |
| CLI | `modwire_cli` / `application` | Add both `.modwire` files plus new `application` and `shared` package initializers. |
| Extraction | `modwire_extraction` / `code` | Add both `.modwire` files and `shared`; preserve the existing `code` initializer. |
| Mermaid | `modwire_mermaid` / `architecture` | Add both `.modwire` files and `shared`; preserve the existing `architecture` initializer. |

`modwire-agent` is the scaffolding application and MCP transport host. It is
intentionally not a target profile for this repository scaffold.

The library and CLI golden shapes are stored under `tests/golden`. Any later
workspace adoption belongs to the separate CLI capability lane and must review a
preview before applying files.
