from typing import Any

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.invalid import InvalidActor
from ...domain.collaboration.policy import ActorPolicy


class ActorHeaders:
    @staticmethod
    def extract(request: Any, policy: ActorPolicy) -> Actor:
        actor_id = request.headers.get("X-Actor-Id")
        actor_type = request.headers.get("X-Actor-Type")
        missing = [
            name
            for name, value in (("X-Actor-Id", actor_id), ("X-Actor-Type", actor_type))
            if not value or not value.strip()
        ]
        if missing:
            raise InvalidActor(f"Missing required actor headers: {', '.join(missing)}.")
        return policy.identify(actor_id, actor_type)
