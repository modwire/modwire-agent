from dataclasses import dataclass

from django.db import transaction
from wireup import injectable

from shared.languages import PHP, Python, Typescript

from ..models.command import Command
from ..models.language import Language
from ..models.package_manager import PackageManager


@dataclass(frozen=True)
class CatalogSyncResult:
    languages: int = 0
    package_managers: int = 0
    commands: int = 0


@injectable
class LanguageCatalogService:
    def __init__(self, python: Python, php: PHP, typescript: Typescript):
        self.definitions = (python, php, typescript)

    def sync(self, timeout: float = 10) -> CatalogSyncResult:
        versions = {
            definition.name: definition.get_current_version(timeout)
            for definition in self.definitions
        }

        with transaction.atomic():
            for definition in self.definitions:
                language, _ = Language.objects.update_or_create(
                    name=definition.name,
                    defaults={
                        "executable": definition.executable,
                        "stable_version": versions[definition.name],
                    },
                )
                for manager_definition in definition.package_managers:
                    manager, _ = PackageManager.objects.update_or_create(
                        language=language,
                        name=manager_definition.name,
                        defaults={"executable": manager_definition.executable},
                    )
                    for result, cmd in manager_definition.commands.items():
                        Command.objects.update_or_create(
                            package_manager=manager,
                            result=result,
                            defaults={"cmd": cmd},
                        )

        return CatalogSyncResult(
            languages=len(self.definitions),
            package_managers=sum(len(item.package_managers) for item in self.definitions),
            commands=sum(
                len(manager.commands)
                for item in self.definitions
                for manager in item.package_managers
            ),
        )
