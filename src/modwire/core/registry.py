from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalApp:
    label: str
    package: str
    config_class: str

    @property
    def config(self) -> str:
        return f"{self.package}.apps.{self.config_class}"


LOCAL_APPS = (
    LocalApp("languages", "modwire.languages.adapters.http", "LanguagesHttpConfig"),
    LocalApp("records", "modwire.records.adapters.http", "RecordsHttpConfig"),
    LocalApp("plans", "modwire.plans.adapters.http", "PlansHttpConfig"),
    LocalApp("scaffoldings", "modwire.scaffoldings.adapters.http", "ScaffoldingsHttpConfig"),
    LocalApp("tokens", "modwire.tokens.adapters.http", "TokensHttpConfig"),
)

SHARED_INJECTABLES: tuple[str, ...] = ()


def installed_apps() -> list[str]:
    return [app.config for app in LOCAL_APPS]


def service_modules(apps_root: Path) -> list[str]:
    modules = list(SHARED_INJECTABLES)
    for app in LOCAL_APPS:
        services_dir = apps_root / app.label / "services"
        if not services_dir.is_dir():
            continue

        modules.append(f"{app.package}.services")
        modules.extend(
            f"{app.package}.services.{path.stem}"
            for path in sorted(services_dir.glob("*.py"))
            if path.name != "__init__.py"
        )
    return modules
