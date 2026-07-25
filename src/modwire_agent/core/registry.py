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

    @staticmethod
    def installed_apps() -> list[str]:
        return [app.config for app in LOCAL_APPS]

    @staticmethod
    def service_modules(apps_root: Path) -> list[str]:
        modules = list(SHARED_INJECTABLES)
        for app in LOCAL_APPS:
            services_dir = apps_root / app.label / "services"
            if services_dir.is_dir():
                modules.append(f"{app.package}.services")
                modules.extend(
                    f"{app.package}.services.{path.stem}"
                    for path in sorted(services_dir.glob("*.py"))
                    if path.name != "__init__.py"
                )
        return modules


LOCAL_APPS = (
    LocalApp("languages", "modwire_agent.languages.adapters.http", "LanguagesHttpConfig"),
    LocalApp("records", "modwire_agent.records.adapters.http", "RecordsHttpConfig"),
    LocalApp("plans", "modwire_agent.plans.adapters.http", "PlansHttpConfig"),
    LocalApp("scaffoldings", "modwire_agent.scaffoldings.adapters.http", "ScaffoldingsHttpConfig"),
)

SHARED_INJECTABLES: tuple[str, ...] = ()


installed_apps = LocalApp.installed_apps
service_modules = LocalApp.service_modules
