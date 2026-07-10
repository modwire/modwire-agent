import json
from urllib.request import Request, urlopen

from wireup import injectable

from .base import LanguageDefinition, LanguageVersionError, PackageManagerDefinition


@injectable
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

    def get_current_version(self, timeout: float = 10) -> str:
        request = Request(
            "https://registry.npmjs.org/typescript/latest",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                version = json.load(response)["version"]
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise LanguageVersionError(f"Could not obtain the current TypeScript version: {error}") from error
        if not isinstance(version, str) or not version:
            raise LanguageVersionError("The npm registry returned an invalid current TypeScript version.")
        return version
