import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, ToolDefinition


@injectable(as_type=LanguageDefinition, qualifier="mermaid")
class Mermaid(LanguageDefinition):
    name = "Mermaid"
    executable = "mmdc"
    source_extensions = (".mermaid", ".mmd")
    package_managers = ()
    tools = (
        ToolDefinition(
            name="Mermaid CLI",
            roles=("diagram_renderer", "diagram_validator"),
            executable="mmdc",
            package_name="@mermaid-js/mermaid-cli",
            homepage_url="https://mermaid.js.org/",
            config_paths=("mermaid.config.json",),
            default_enabled=True,
            commands={"render": "mmdc -i {input} -o {output}"},
        ),
    )

    @property
    def version_request(self) -> Request:
        return Request(
            "https://registry.npmjs.org/mermaid/latest",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )

    def on_version_response(self, response) -> str:
        return json.load(response)["version"]
