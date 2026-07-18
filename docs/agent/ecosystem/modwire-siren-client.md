# @modwire/siren-client

Return to the [ecosystem map](README.md).

## Owns

Strict TypeScript parsing, validation, relation following, action execution,
origin policy, and structured diagnostics for Siren documents.

## Reuse in the agent

The browser can use this instead of hand-written Siren parsing and URL/action
handling. The client should remain responsible for generic hypermedia behavior,
while agent-specific contract views remain application code.
