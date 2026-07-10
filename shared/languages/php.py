import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, PackageManagerDefinition


@injectable(as_type=LanguageDefinition, qualifier="php")
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

    @property
    def version_request(self) -> Request:
        return Request(
            "https://endoflife.date/api/php.json",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )

    def on_version_response(self, response) -> str:
        return json.load(response)[0]["latest"]
