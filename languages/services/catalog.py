from collections.abc import Sequence
from dataclasses import dataclass

from django.db import transaction
from wireup import injectable

from shared.languages.base import LanguageDefinition

from .command import CommandService
from .language import LanguageService
from .package_manager import PackageManagerService


@dataclass(frozen=True)
class CatalogSyncResult:
    languages: int = 0
    package_managers: int = 0
    commands: int = 0


@injectable
class LanguageCatalogService:
    def __init__(
        self,
        definitions: Sequence[LanguageDefinition],
        languages: LanguageService,
        package_managers: PackageManagerService,
        commands: CommandService,
    ):
        self.definitions = tuple(sorted(definitions, key=lambda definition: definition.name))
        self.languages = languages
        self.package_managers = package_managers
        self.commands = commands

    def sync(self, timeout: float = 10) -> CatalogSyncResult:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        names = [definition.name for definition in self.definitions]
        if len(names) != len(set(names)):
            raise ValueError("language definitions must have unique names")

        resolved = tuple(
            (definition, definition.get_current_version(timeout))
            for definition in self.definitions
        )

        with transaction.atomic():
            for definition, version in resolved:
                self._sync_language(definition, version)

        return CatalogSyncResult(
            languages=len(self.definitions),
            package_managers=sum(len(item.package_managers) for item in self.definitions),
            commands=sum(
                len(manager.commands)
                for item in self.definitions
                for manager in item.package_managers
            ),
        )

    def _sync_language(self, definition: LanguageDefinition, version: str) -> None:
        language = self.languages.upsert(
            name=definition.name,
            executable=definition.executable,
            stable_version=version,
        )
        for manager_definition in definition.package_managers:
            manager = self.package_managers.upsert(
                language=language,
                name=manager_definition.name,
                executable=manager_definition.executable,
            )
            for result, cmd in manager_definition.commands.items():
                self.commands.upsert(
                    package_manager=manager,
                    result=result,
                    cmd=cmd,
                )
