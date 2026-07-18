# modwire-extraction

Return to the [ecosystem map](README.md).

## Owns

Canonical, language-aware facts about a source tree: files, logical modules,
imports and their resolution, exports, declarations, callable signatures,
calls, and dependency edges.

It supports Python, TypeScript/JavaScript/TSX, and PHP extraction. Its
`QueryableCodeMap` is the common read model for architecture analysis.

## Reuse in the agent

Use extraction as the sole source of static workspace facts. The future runner
should create a reproducible code-map snapshot before and after implementation;
the contract verifier and architecture package should consume that snapshot.

## Does not own

Extraction does not decide whether a dependency is architecturally acceptable,
whether a symbol fulfils a use case, or who owns a domain concept.
