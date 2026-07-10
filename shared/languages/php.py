import json
from urllib.request import Request, urlopen

from wireup import injectable

from .base import LanguageDefinition, LanguageVersionError, PackageManagerDefinition


@injectable
class PHP(LanguageDefinition):
    name = "PHP"
    executable = "php"
    package_managers = (
        PackageManagerDefinition(
            name="Composer",
            executable="composer",
            commands={
                "init": "composer init",
                "install": "composer install",
                "add": "composer require {package}",
                "remove": "composer remove {package}",
            },
        ),
    )

    def get_current_version(self, timeout: float = 10) -> str:
        request = Request(
            "https://endoflife.date/api/php.json",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                version = json.load(response)[0]["latest"]
        except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
            raise LanguageVersionError(f"Could not obtain the current PHP version: {error}") from error
        if not isinstance(version, str) or not version:
            raise LanguageVersionError("The PHP lifecycle API returned an invalid current version.")
        return version
