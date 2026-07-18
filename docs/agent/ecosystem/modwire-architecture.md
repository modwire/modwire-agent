# modwire-architecture

Return to the [ecosystem map](README.md).

## Owns

Deterministic architecture analysis over an extracted code map. It validates
boundary tags, dependency flow, cycles, re-entry, and configurable source-shape
rules.

It already provides topology insights for:

- path-based dependency clusters;
- file-level dependency hotspots;
- graph roots, leaves, isolated files, and external dependencies;
- callable relationships; and
- unused exported symbols.

## Reuse in the agent

Use it for generic static verification and as the evidence source for
architecture findings. Hotspot and cluster detection should be surfaced in the
agent, not reimplemented there.

## Necessary extension

An export-hub reporter can be added here as a generic graph concern. A true
SSOT violation cannot be inferred from topology alone: the contract must first
declare ownership, after which the agent can compare observed competing
authority with that declaration.
