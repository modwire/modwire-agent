# modwire-agent

Return to the [ecosystem map](README.md).

## Owns

The agent is the human-facing application and intended canonical contract
registry. It
orchestrates exploration, proposal, explicit approval, implementation, and
verification without owning low-level extraction, architecture analysis,
or Mermaid formatting.

## Reuses

- `modwire-extraction` for workspace facts.
- `modwire-architecture` for policy checks and topology insights.
- `modwire-mermaid` for deterministic diagrams.

## Current boundary

The current application stores records and scaffoldings and exposes a Django
Ninja API. The accepted-contract registry and MCP traversal layer are pending a
fresh design.

See the [missing capability map](missing-capabilities.md).
