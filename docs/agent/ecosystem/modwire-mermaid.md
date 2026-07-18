# modwire-mermaid

Return to the [ecosystem map](README.md).

## Owns

Typed, immutable Mermaid diagram contracts and deterministic Mermaid-source
compilation. It includes architecture, class, event-modeling, file-tree,
flowchart, mindmap, sequence, state, swimlane, timeline, and user-journey
diagrams.

## Reuse in the agent

The agent should project accepted contract data into these typed diagrams rather
than assemble Mermaid strings in prompts or application code. Markdown and a
chosen renderer own preview and rendering; this package owns valid source.

## Does not own

It does not decide which diagram a use case needs, maintain Markdown document
navigation, or infer architecture from a repository.
