import json
from urllib.request import Request

from wireup import injectable

from .base import LanguageDefinition, PackageManagerDefinition, ToolDefinition


@injectable(as_type=LanguageDefinition, qualifier="typescript")
class Typescript(LanguageDefinition):
    name = "TypeScript"
    executable = "tsc"
    package_managers = (
        PackageManagerDefinition(
            name="NPM",
            executable="npm",
            manifest_paths=("package.json",),
            lockfile_paths=("package-lock.json",),
            registry_url="https://registry.npmjs.org",
            package_url_type="npm",
            version_constraint="semver",
            supports_workspaces=True,
            commit_lockfiles=True,
            commands={
                "init": "npm init",
                "install": "npm install",
                "add_runtime": "npm install {package}",
                "add_development": "npm install --save-dev {package}",
                "add_optional": "npm install --save-optional {package}",
                "add_peer": "npm install --save-peer {package}",
                "remove": "npm uninstall {package}",
                "update": "npm update",
                "lock": "npm install --package-lock-only",
                "run": "npm run {command}",
                "publish": "npm publish",
                "audit": "npm audit",
            },
        ),
    )
    tools = (
        ToolDefinition(
            "TypeScript",
            ("type_checker", "build"),
            "tsc",
            "typescript",
            "https://www.typescriptlang.org/",
            ("tsconfig.json",),
            True,
            {"check": "tsc --noEmit", "build": "tsc"},
        ),
        ToolDefinition(
            "ESLint",
            ("linter",),
            "eslint",
            "eslint",
            "https://eslint.org/",
            ("eslint.config.js",),
            True,
            {"check": "eslint .", "fix": "eslint . --fix"},
        ),
        ToolDefinition(
            "Prettier",
            ("formatter",),
            "prettier",
            "prettier",
            "https://prettier.io/",
            (".prettierrc",),
            True,
            {"check": "prettier . --check", "fix": "prettier . --write"},
        ),
        ToolDefinition(
            "Vitest",
            ("test_runner",),
            "vitest",
            "vitest",
            "https://vitest.dev/",
            ("vitest.config.ts",),
            True,
            {"test": "vitest run", "serve": "vitest"},
        ),
        ToolDefinition(
            "Vitest V8",
            ("coverage",),
            "vitest",
            "@vitest/coverage-v8",
            "https://vitest.dev/guide/coverage",
            ("vitest.config.ts",),
            True,
            {"coverage": "vitest run --coverage"},
        ),
        ToolDefinition(
            "tsx",
            ("development_runner",),
            "tsx",
            "tsx",
            "https://tsx.is/",
            (),
            True,
            {"serve": "tsx watch {entrypoint}"},
        ),
        ToolDefinition(
            "TypeDoc",
            ("documentation",),
            "typedoc",
            "typedoc",
            "https://typedoc.org/",
            ("typedoc.json",),
            False,
            {"build": "typedoc"},
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
