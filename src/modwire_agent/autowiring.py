import fnmatch
import importlib
import inspect
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, get_origin, is_typeddict

import wireup
from modwire_hex import DjangoApplication

import modwire_agent

Lifetime = Literal["scoped", "singleton", "transient"]


@dataclass(frozen=True, slots=True)
class DiscoveryRule:
    pattern: str
    lifetime: Lifetime


DISCOVERY_RULES = (
    DiscoveryRule("modwire_agent.*.use_cases.*.*", "transient"),
    DiscoveryRule("modwire_agent.*.domain.*.*Policy", "singleton"),
    DiscoveryRule("modwire_agent.languages.domain.catalog.BuiltInLanguageCatalog", "singleton"),
    DiscoveryRule("modwire_agent.*.adapters.*.Django*", "scoped"),
    DiscoveryRule("modwire_agent.languages.adapters.*.HttpVersionReader", "singleton"),
    DiscoveryRule("modwire_agent.plans.adapters.*.JsonSchemaValidator", "singleton"),
    DiscoveryRule("modwire_agent.plans.adapters.*.RegisteredOperationCatalog", "singleton"),
    DiscoveryRule("modwire_agent.scaffoldings.adapters.convergence.*.Scaffolding*", "transient"),
    DiscoveryRule("modwire_agent.scaffoldings.adapters.preview.*.*", "transient"),
)


class AutowiredDjangoApplication(DjangoApplication):
    def create_container(self) -> Any:
        return wireup.create_sync_container(injectables=list(ServiceDiscovery.services()))


class ServiceDiscovery:
    @classmethod
    def services(cls) -> Iterable[type[Any]]:
        for service, lifetime in cls.discover():
            yield wireup.injectable(service, lifetime=lifetime, as_type=cls.port(service))

    @classmethod
    def discover(cls) -> Iterable[tuple[type[Any], Lifetime]]:
        for module in cls.modules():
            for _, service in inspect.getmembers(module, inspect.isclass):
                if service.__module__ != module.__name__ or not cls.is_service(service):
                    continue
                lifetime = cls.lifetime(module.__name__, service.__name__)
                if lifetime is not None:
                    yield service, lifetime

    @staticmethod
    def modules() -> Iterable[Any]:
        package_root = Path(next(iter(modwire_agent.__path__)))
        for source_path in package_root.rglob("*.py"):
            relative_path = source_path.relative_to(package_root).with_suffix("")
            if len(relative_path.parts) == 1 or relative_path.parts[0] == "core":
                continue
            module_parts = relative_path.parts[:-1] if relative_path.name == "__init__" else relative_path.parts
            yield importlib.import_module(f"{modwire_agent.__name__}.{'.'.join(module_parts)}")

    @staticmethod
    def is_service(candidate: type[Any]) -> bool:
        return not is_typeddict(candidate) and get_origin(candidate) is None

    @staticmethod
    def lifetime(module_name: str, service_name: str) -> Lifetime | None:
        qualified_name = f"{module_name}.{service_name}"
        for rule in DISCOVERY_RULES:
            if fnmatch.fnmatchcase(qualified_name, rule.pattern):
                return rule.lifetime
        return None

    @staticmethod
    def port(service: type[Any]) -> type[Any] | None:
        ports = [
            base
            for base in service.__mro__[1:]
            if ".ports." in base.__module__
            or base.__module__.endswith(".domain.contracts")
            and base.__name__.endswith("Catalog")
        ]
        if len(ports) > 1:
            raise ValueError(f"{service.__qualname__} implements more than one port.")
        return ports[0] if ports else None

application = AutowiredDjangoApplication(modules=())
