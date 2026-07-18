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
5. [modwire-siren](modwire-siren.md) — Python Siren and OpenAPI integration.
6. [@modwire/siren-client](modwire-siren-client.md) — strict TypeScript Siren
   client.
7. [@modwire/siren-ui](modwire-siren-ui.md) — framework-neutral Siren UI
   engine.
8. [@modwire/siren-react](modwire-siren-react.md) — React presentation adapter.

## Planned components

[Missing capability map](missing-capabilities.md) identifies the contract,
verification, and controlled-workspace responsibilities that no existing
package owns.
