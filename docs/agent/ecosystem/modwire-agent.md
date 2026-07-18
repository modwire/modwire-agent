# modwire-agent

Return to the [ecosystem map](README.md).

## Owns

The agent is the human-facing application and intended canonical contract
registry. It
orchestrates exploration, proposal, explicit approval, implementation, and
verification without owning low-level extraction, architecture analysis,
Mermaid formatting, or generic hypermedia mechanics.

## Reuses

- `modwire-extraction` for workspace facts.
- `modwire-architecture` for policy checks and topology insights.
- `modwire-mermaid` for deterministic diagrams.
- `modwire-siren` and its TypeScript companions for discoverable API and
  workbench mechanics.

## Current boundary

The current application stores records and scaffoldings and exposes them through
a Siren API and MCP adapter. It does not yet implement the accepted-contract
registry or workspace mutation. Those future responsibilities must compose
existing packages rather than copy their logic.

See the [missing capability map](missing-capabilities.md).
