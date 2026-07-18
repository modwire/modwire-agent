# Missing capability map

Return to the [ecosystem map](README.md).

No current package owns the following product responsibilities.

## Contract model and lifecycle

The Modwire service must be the canonical registry for immutable
development-contract versions and acceptance history. It needs a framework-free
typed model for use cases, ownership, logic knobs, expected signatures, diagram
references, and required verification evidence. That model should become a
separate package only after it has stabilized through agent use.

## Contract verification

An adapter must compare accepted contract obligations with an extracted code map
and architecture report. It must report fulfilled, missing, unexpected, and
drifted obligations with links to the supporting code and tests.

## Controlled workspace runner

A separate runner must attach an explicitly selected workspace, snapshot it,
preview changes, apply approved work, run checks, and return evidence. It is
the only component that should gain workspace-mutation authority.

## Behavioral evidence

Use cases need proof of outcomes in addition to signature and topology checks.
The agent will need a test-evidence port that can associate accepted scenarios
with framework-specific tests without owning every test runner.
