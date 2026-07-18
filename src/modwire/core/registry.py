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
    LocalApp("languages", "modwire.apps.languages", "LanguagesConfig"),
    LocalApp("records", "modwire.apps.records", "RecordsConfig"),
    LocalApp("scaffoldings", "modwire.apps.scaffoldings", "ScaffoldingsConfig"),
    LocalApp("scrapers", "modwire.apps.scrapers", "ScrapersConfig"),
    LocalApp("tokens", "modwire.apps.tokens", "TokensConfig"),
)

SHARED_INJECTABLES = ("modwire.shared.languages",)


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
