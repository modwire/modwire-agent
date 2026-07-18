import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, PackageManagerDefinition, ToolDefinition


@injectable(as_type=LanguageDefinition, qualifier="python")
class Python(LanguageDefinition):
    name = "Python"
    executable = "python"
    source_extensions = (".py",)
    package_managers = (
        PackageManagerDefinition(
            name="UV",
            executable="uv",
            manifest_paths=("pyproject.toml",),
            lockfile_paths=("uv.lock",),
            registry_url="https://pypi.org/simple",
            package_url_type="pypi",
            version_constraint="pep440",
            supports_workspaces=True,
            commit_lockfiles=True,
            commands={
                "init": "uv init",
                "install": "uv sync",
                "add_runtime": "uv add {package}",
                "add_development": "uv add --dev {package}",
                "add_optional": "uv add --optional {group} {package}",
                "remove": "uv remove {package}",
                "update": "uv lock --upgrade",
                "lock": "uv lock",
                "run": "uv run {command}",
                "publish": "uv publish",
            },
        ),
    )
    tools = (
        ToolDefinition(
            "Ruff",
            ("formatter", "linter"),
            "ruff",
            "ruff",
            "https://docs.astral.sh/ruff/",
            (),
            True,
            {"check": "ruff check . && ruff format --check .", "fix": "ruff check --fix . && ruff format ."},
        ),
        ToolDefinition(
            "basedpyright",
            ("type_checker",),
            "basedpyright",
            "basedpyright",
            "https://docs.basedpyright.com/",
            ("pyrightconfig.json",),
            True,
            {"check": "basedpyright"},
        ),
        ToolDefinition(
            "pytest",
            ("test_runner",),
            "pytest",
            "pytest",
            "https://docs.pytest.org/",
            ("pyproject.toml",),
            True,
            {"test": "pytest"},
        ),
        ToolDefinition(
            "coverage.py",
            ("coverage",),
            "coverage",
            "coverage",
            "https://coverage.readthedocs.io/",
            (".coveragerc", "pyproject.toml"),
            True,
            {"coverage": "coverage run -m pytest && coverage report"},
        ),
        ToolDefinition(
            "build",
            ("build",),
            "python",
            "build",
            "https://build.pypa.io/",
            ("pyproject.toml",),
            True,
            {"build": "python -m build"},
        ),
        ToolDefinition(
            "MkDocs",
            ("documentation",),
            "mkdocs",
            "mkdocs",
            "https://www.mkdocs.org/",
            ("mkdocs.yml",),
            False,
            {"build": "mkdocs build", "serve": "mkdocs serve"},
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
