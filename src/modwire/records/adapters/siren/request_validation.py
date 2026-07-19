from dataclasses import dataclass
from typing import Any

from modwire_hex.django import DjangoRequest
from ninja.errors import HttpError

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.invalid import InvalidActor
from ...domain.collaboration.policy import ActorPolicy


@dataclass(frozen=True, slots=True)
class SirenValidationReport:
    status_code: int
    detail: str
    actor: Actor | None = None

    @property
    def accepted(self) -> bool:
        return self.status_code < 400

    def require_actor(self) -> Actor:
        if self.actor is None:
            raise HttpError(self.status_code, self.detail)
        return self.actor


class SirenRequestValidator:
    def validate_actor_headers(self, request: Any, policy: ActorPolicy) -> SirenValidationReport:
        actor_id = request.headers.get("X-Actor-Id")
        actor_type = request.headers.get("X-Actor-Type")
        missing = [
            name
            for name, value in (("X-Actor-Id", actor_id), ("X-Actor-Type", actor_type))
            if not value or not value.strip()
        ]
        if missing:
            return SirenValidationReport(422, f"Missing required actor headers: {', '.join(missing)}.")
        try:
            return SirenValidationReport(200, "OK", policy.identify(actor_id, actor_type))
        except InvalidActor as error:
            return SirenValidationReport(422, str(error))


def validated_siren_actor(request: Any) -> Actor:
    validator = DjangoRequest.resolve(request, SirenRequestValidator)
    policy = DjangoRequest.resolve(request, ActorPolicy)
    return validator.validate_actor_headers(request, policy).require_actor()
