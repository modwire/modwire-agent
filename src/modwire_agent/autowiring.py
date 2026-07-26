import fnmatch
import importlib
import inspect
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, get_origin, is_typeddict

import wireup
from modwire_hex import DjangoApplication
from pydantic import BaseModel

import modwire_agent

Lifetime = Literal["scoped", "singleton", "transient"]


@dataclass(frozen=True, slots=True)
class DiscoveryRule:
    pattern: str
    lifetime: Lifetime


DISCOVERY_RULES = (
    DiscoveryRule("modwire_agent.shared.*", "singleton"),
)

class AutowiredDjangoApplication(DjangoApplication):
    def create_container(self) -> Any:
        return wireup.create_sync_container(injectables=list(ServiceDiscovery.services()))


application = AutowiredDjangoApplication(modules=())
