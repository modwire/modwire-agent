from dataclasses import dataclass

from .actor_kind import ActorKind


@dataclass(frozen=True, slots=True)
class Actor:
    identifier: str
    kind: ActorKind
