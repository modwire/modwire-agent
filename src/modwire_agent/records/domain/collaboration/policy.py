from dataclasses import dataclass

from .actor import Actor
from .actor_kind import ActorKind
from .invalid import InvalidActor


@dataclass(frozen=True, slots=True)
class ActorPolicy:
    def identify(self, identifier: str | None, kind: str | None) -> Actor:
        if not identifier or not identifier.strip():
            raise InvalidActor("Actor identity is required.")
        try:
            return Actor(identifier=identifier, kind=ActorKind(kind))
        except ValueError as error:
            raise InvalidActor("Actor kind must be user or agent.") from error

    def allow_reordering(self, actor: Actor) -> None:
        if actor.kind not in (ActorKind.USER, ActorKind.AGENT):
            raise InvalidActor("Actor cannot reorder section placements.")

    def allow_contributing(self, actor: Actor) -> None:
        if actor.kind not in (ActorKind.USER, ActorKind.AGENT):
            raise InvalidActor("Actor cannot contribute to records.")

    def allow_editing(self, actor: Actor) -> None:
        if actor.kind not in (ActorKind.USER, ActorKind.AGENT):
            raise InvalidActor("Actor cannot edit record content.")

    def allow_proposing(self, actor: Actor) -> None:
        if actor.kind is not ActorKind.AGENT:
            raise InvalidActor("Only an agent can create content proposals.")

    def allow_resolving_proposals(self, actor: Actor) -> None:
        if actor.kind is not ActorKind.USER:
            raise InvalidActor("Only a user can resolve content proposals.")
