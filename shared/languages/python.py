import json
from urllib.request import Request, urlopen

from wireup import injectable

from .base import LanguageDefinition, LanguageVersionError, PackageManagerDefinition


@injectable
class Python(LanguageDefinition):
    name = "Python"
    executable = "python"
    package_managers = (
        PackageManagerDefinition(
            name="UV",
            executable="uv",
            commands={
                "init": "uv init",
                "install": "uv sync",
                "add": "uv add {package}",
                "remove": "uv remove {package}",
            },
        ),
    )

    def get_current_version(self, timeout: float = 10) -> str:
        request = Request(
            "https://endoflife.date/api/python.json",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                version = json.load(response)[0]["latest"]
        except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
            raise LanguageVersionError(f"Could not obtain the current Python version: {error}") from error
        if not isinstance(version, str) or not version:
            raise LanguageVersionError("The Python lifecycle API returned an invalid current version.")
        return version
