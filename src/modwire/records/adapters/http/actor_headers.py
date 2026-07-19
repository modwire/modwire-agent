from typing import Any

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy


class ActorHeaders:
    @staticmethod
    def extract(request: Any, policy: ActorPolicy) -> Actor:
        return policy.identify(request.headers.get("X-Actor-Id"), request.headers.get("X-Actor-Type"))
