# Plans QA progress ledger

This is the acceptance map for a generic, database-authored planning runtime. The
functional tests are black-box HTTP contracts. The roadmap tests are deliberately
skipped until their capability exists; removing a skip means implementing the
stated safety property, not merely changing the test.

## P0: protocol integrity

| Contract | Status |
| --- | --- |
| Publish, start, advance, and complete a terminal plan | covered |
| Linear progression only through declared successors | covered |
| Start and submission payloads respect JSON Schema | covered |
| Bad protocol graph (names, stages, transitions, reachability) is rejected | covered |
| Gate evidence is scoped to current stage and schema | covered |
| All gates block until all are satisfied | covered |
| Completed runs reject extra submissions | covered |
| Reject malformed JSON Schemas at publication | covered |
| Validate next-stage input before persisting a submission | covered |
| Require a declared terminal path; reject unbounded cycles | covered |
| Reject incompatible adjacent stage contracts or require a mapping | covered |
| Unknown gate / operation stays a controlled 422, never 500 | covered |
| Immutable named versions; each run pins and reproduces its version | covered |

## P0: trusted workflow facts

| Attack | Expected result |
| --- | --- |
| Gate from another stage or definition | 422 and no evidence saved |
| Repeat gate satisfaction | covered: identical retry is idempotent; conflicting evidence is rejected |
| Evidence on run A | covered: cannot unlock run B |
| Invalid evidence followed by valid retry | failed evidence is absent; valid retry unlocks only its gate |
| Definition deletion with runs | protocol history remains protected |

## P0: opaque operation seam

| Contract | Expected result |
| --- | --- |
| Unknown extension key/version | publish rejects it without persisting a definition |
| Handler configuration, input, and output | each validates against its declared schema |
| Stage operation | only current-stage operation can execute; required operations block submission |
| Retry/concurrency | declared idempotency semantics; no accidental duplicate side effect |
| Typed artifact declaration | covered: producer, consumer IDs, output schemas, and compatibility are versioned with the definition |
| Typed artifact persistence and dependency | pending: operation output becomes an immutable typed artifact consumable by a later operation |

The artifact dependency is the key end-state: an owner module can define an
architecture/Mermaid contract operation and a code-map conformance operation,
while `plans` sees only typed operation and artifact contracts.

## P1: hostile input, persistence, and operational safety

- Invalid UUIDs, unknown IDs, malformed JSON, missing fields, wrong JSON types,
  whitespace IDs, and overlong identifiers return controlled 4xx responses.
- JSON Schema has an explicit policy for scalar documents, `$ref`, `format`, and
  deeply nested/oversized values. External references must never be fetched.
- Every state change is transactional: validation, submission, and run advance
  commit together or none do.
- Concurrent submissions, gate satisfactions, and operations have deterministic
  uniqueness/idempotency semantics, tested with `TransactionTestCase` workers.
- Repositories round-trip all protocol/run fields and protect definitions used by
  runs; migrations preserve history.
- Authentication, tenant ownership, actor audit trail, and safe 5xx handler
  failures are required before exposure outside a trusted environment.
- Architectural checks ensure domain/use-cases know no Django, Mermaid,
  architecture, or code-map vocabulary, and handlers are reached only through
  operation ports.
