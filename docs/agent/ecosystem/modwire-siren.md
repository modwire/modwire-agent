# modwire-siren

Return to the [ecosystem map](README.md).

## Owns

Typed Siren documents projected from OpenAPI, plus a Python client for following
advertised relations and executing advertised actions. Its optional UI profile
publishes presentation metadata without coupling the API to a browser
framework.

## Reuse in the agent

Expose contract, approval, verification, and finding transitions as advertised
controls. Clients should discover permitted transitions from each resource,
rather than reproduce API route knowledge.

## Does not own

Siren does not define the contract domain, make authorization decisions, or
render the user interface.
