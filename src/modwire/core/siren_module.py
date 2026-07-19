from dataclasses import dataclass

from modwire_siren import SirenResourceSpec
from ninja_extra import ControllerBase


@dataclass(frozen=True, slots=True)
class SirenModule:
    name: str
    resources: tuple[SirenResourceSpec, ...]
    controllers: tuple[type[ControllerBase], ...]
