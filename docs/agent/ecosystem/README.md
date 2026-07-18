# Modwire ecosystem map

Part of the [Modwire agent architecture](../README.md) collection.

Each package has its own document. Package documents state what that package
owns, what the agent may reuse, and what must remain outside its boundary.

## Existing packages

1. [modwire-agent](modwire-agent.md) — contract-facing application and
   orchestrator.
2. [modwire-extraction](modwire-extraction.md) — canonical code facts and
   dependency graph.
3. [modwire-architecture](modwire-architecture.md) — architecture rules and
   deterministic topology insights.
4. [modwire-mermaid](modwire-mermaid.md) — typed, deterministic diagram source.

## Planned components

[Missing capability map](missing-capabilities.md) identifies the contract,
verification, and controlled-workspace responsibilities that no existing
package owns.
