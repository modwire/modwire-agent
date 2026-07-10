import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, PackageManagerDefinition


@injectable(as_type=LanguageDefinition, qualifier="python")
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

    @property
    def version_request(self) -> Request:
        return Request(
            "https://endoflife.date/api/python.json",
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )

    def on_version_response(self, response) -> str:
        return json.load(response)[0]["latest"]
