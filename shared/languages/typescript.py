import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, PackageManagerDefinition


@injectable(as_type=LanguageDefinition, qualifier="typescript")
class Typescript(LanguageDefinition):
    name = "TypeScript"
    executable = "tsc"
    package_managers = (
        PackageManagerDefinition(
            name="NPM",
            executable="npm",
            commands={
                "init": "npm init",
                "install": "npm install",
                "add": "npm install {package}",
                "remove": "npm uninstall {package}",
            },
        ),
    )

    @property
    def version_request(self) -> Request:
        return Request(
            "https://registry.npmjs.org/typescript/latest",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )

    def on_version_response(self, response) -> str:
        return json.load(response)["version"]
