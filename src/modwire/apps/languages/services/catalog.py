from collections.abc import Sequence
from dataclasses import asdict, dataclass

from django.db import transaction
from wireup import injectable

from modwire.shared.languages.base import LanguageDefinition

from .command import CommandService
from .language import LanguageService
from .package_manager import PackageManagerService
from .tool import ToolService
from .tool_command import ToolCommandService


@dataclass(frozen=True)
class CatalogSyncResult:
    languages: int = 0
    package_managers: int = 0
    commands: int = 0
    tools: int = 0
    tool_commands: int = 0


@injectable
class LanguageCatalogService:
    def __init__(
        self,
        definitions: Sequence[LanguageDefinition],
        languages: LanguageService,
        package_managers: PackageManagerService,
        commands: CommandService,
        tools: ToolService,
        tool_commands: ToolCommandService,
    ):
        self.definitions = tuple(sorted(definitions, key=lambda definition: definition.name))
        self.languages = languages
        self.package_managers = package_managers
        self.commands = commands
        self.tools = tools
        self.tool_commands = tool_commands

    def sync(self, timeout: float = 10) -> CatalogSyncResult:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        names = [definition.name for definition in self.definitions]
        if len(names) != len(set(names)):
            raise ValueError("language definitions must have unique names")

        resolved = tuple((definition, definition.get_current_version(timeout)) for definition in self.definitions)

        with transaction.atomic():
            for definition, version in resolved:
                self._sync_language(definition, version)

        return CatalogSyncResult(
            languages=len(self.definitions),
            package_managers=sum(len(item.package_managers) for item in self.definitions),
            commands=sum(len(manager.commands) for item in self.definitions for manager in item.package_managers),
            tools=sum(len(item.tools) for item in self.definitions),
            tool_commands=sum(len(tool.commands) for item in self.definitions for tool in item.tools),
        )

    def _sync_language(self, definition: LanguageDefinition, version: str) -> None:
        language = self.languages.upsert(
            name=definition.name,
            executable=definition.executable,
            stable_version=version,
        )
        for manager_definition in definition.package_managers:
            manager_data = asdict(manager_definition)
            commands = manager_data.pop("commands")
            manager = self.package_managers.upsert(
                language=language,
                **manager_data,
            )
            for result, cmd in commands.items():
                self.commands.upsert(
                    package_manager=manager,
                    result=result,
                    cmd=cmd,
                )
        for tool_definition in definition.tools:
            tool_data = asdict(tool_definition)
            commands = tool_data.pop("commands")
            tool = self.tools.upsert(
                language=language,
                **tool_data,
            )
            for capability, cmd in commands.items():
                self.tool_commands.upsert(tool=tool, capability=capability, cmd=cmd)
