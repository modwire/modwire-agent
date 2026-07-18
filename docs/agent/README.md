# Modwire agent architecture

This is a collection of small, linked documents. Each document owns one
concept; it should link to prerequisites rather than duplicate their content.

## Structure

- [`foundation/`](foundation/README.md) defines the collaboration model and
  shared language.
- [`ecosystem/`](ecosystem/README.md) maps one Modwire package or planned
  component per file.
- Future `contracts/` documents will hold accepted change contracts; they will
  not be mixed with the stable architecture reference.

## Reading order

1. [Operating model](foundation/operating-model.md) — the human–agent
   collaboration loop and the approval boundary.
2. [Shared vocabulary](foundation/shared-vocabulary.md) — the meanings used
   consistently in later contracts and diagrams.
3. [Ecosystem map](ecosystem/README.md) — existing packages, their boundaries,
   and the product capabilities still missing.

## Planned additions

- Development contract — the contents of a reviewable proposed change.
- Diagram guide — which Mermaid diagram answers which kind of question.
- Verification model — how contract-to-code drift is identified and resolved.

**Enclosure** remains deferred. It will gain its own document only when a
concrete, distinct use case establishes its role.
