from enum import StrEnum


class ActorKind(StrEnum):
    AGENT = "agent"
    SYSTEM = "system"
    USER = "user"
