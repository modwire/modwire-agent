from enum import Enum


class CommandResult(str, Enum):
    ADD_DEVELOPMENT = "add_development"
    ADD_OPTIONAL = "add_optional"
    ADD_PEER = "add_peer"
    ADD_RUNTIME = "add_runtime"
    AUDIT = "audit"
    INIT = "init"
    INSTALL = "install"
    LOCK = "lock"
    PUBLISH = "publish"
    REMOVE = "remove"
    RUN = "run"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
