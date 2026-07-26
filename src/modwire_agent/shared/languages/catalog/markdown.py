from ..base import Language, PackageManager, Tool, VersionProvider

@inject()
class Markdown(Language):
    id: str = "markdown"
    name: str = "Markdown"
    executable: str = "md"
    source_extensions: tuple[str, ...] = (".md",)
    aliases: tuple[str, ...] = ()
    package_managers: tuple[PackageManager, ...] = ()
    tools: tuple[Tool, ...] = ()
    stable_version: str = ""
    version_provider: VersionProvider = VersionProvider(
        kind="npm",
        url="https://registry.npmjs.org/mermaid/latest",
        result_path=("version",),
    )
