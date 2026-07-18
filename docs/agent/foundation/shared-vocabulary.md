# Shared vocabulary

These terms are intentionally conceptual. They describe the collaboration and
design model without fixing a database schema, API, workspace mechanism, or
implementation framework.

## Collaboration

- **Agent facade** — the human-facing collaborator that explores, plans,
  implements, and verifies a change.
- **Human intent** — the outcome, problem, and constraints expressed by the
  human.
- **Development contract** — the explicit, reviewable architectural design for
  one bounded change.
- **Accepted contract** — the specific version of a development contract the
  human has authorized for implementation.

## Architecture and implementation

- **Use case** — one user-meaningful capability with a clear outcome, such as
  `cart.application.add_product`.
- **Architecture map** — the agreed modules, layers, ownership, and permitted
  relationships in a system.
- **Logic knob** — a named piece of domain-specific decision logic that needs
  focused reasoning beyond repeatable generated structure, such as
  `cart.domain.promotion_calculator`.
- **Scaffolding** — reusable, repeatable code structure generated from a known
  architectural pattern.

## Verification

- **Drift** — a meaningful mismatch between an accepted contract and the
  implemented code, especially in public signatures, ownership, or structural
  relationships.
- **Verification** — the post-implementation comparison of code against the
  accepted contract.
- **Evidence** — a traceable fact supporting a contract obligation or finding,
  such as an extracted symbol, architecture report, test result, or diagram.
- **Architecture finding** — deterministic evidence that deserves human
  architectural judgment; it is not automatically a violation.
- **Topology insight** — an observation derived from code structure and
  dependencies, such as a hotspot, cluster, root, leaf, or unused export.
- **Export hub** — a module or package through which many consumers reach
  capabilities. It can be a deliberate facade or a boundary concern.
- **SSOT candidate** — evidence of possible competing authority over one
  concept. It becomes a violation only when compared with declared ownership.

## Deferred

- **Enclosure** — a deferred concept. It previously consumed capabilities from
  `modwire-extraction`, but Modwire has absorbed some of that responsibility.
  It will be defined only if a distinct use case requires it.

For the collaboration lifecycle in which these terms are used, see the
[operating model](operating-model.md).
