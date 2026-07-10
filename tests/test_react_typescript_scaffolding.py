import json
from pathlib import Path

import yaml

from shared.code import CodePackage, CopierArchive

SCAFFOLDING = Path(__file__).parents[1] / "shared" / "packages" / "projects" / "react-typescript"


def render(**overrides):
    archive = CopierArchive(
        manifest=yaml.safe_load((SCAFFOLDING / "copier.yml").read_text()),
        templates=CodePackage.from_directory(SCAFFOLDING / "templates"),
    )
    return archive.render(
        {
            "project_name": "progressive-browser",
            "project_title": "Progressive Browser",
            "package_manager": "npm",
            **overrides,
        }
    )


def test_react_typescript_scaffolding_renders_complete_tested_project():
    package = render()

    expected = {
        ".env.example",
        ".gitignore",
        "README.md",
        "index.html",
        "package.json",
        "src/App.test.tsx",
        "src/App.tsx",
        "src/main.tsx",
        "src/test/setup.ts",
        "tsconfig.app.json",
        "tsconfig.json",
        "tsconfig.node.json",
        "vite.config.ts",
    }
    assert set(package.files) == expected
    assert "Progressive Browser" in package.files["src/App.tsx"]

    package_json = json.loads(package.files["package.json"])
    assert package_json["name"] == "progressive-browser"
    assert package_json["scripts"] == {
        "dev": "vite",
        "build": "tsc -b && vite build",
        "typecheck": "tsc -b --pretty false",
        "test": "vitest run",
        "test:watch": "vitest",
    }
    assert "react" in package_json["dependencies"]
    assert "vitest" in package_json["devDependencies"]


def test_react_typescript_scaffolding_uses_selected_package_manager_in_readme():
    package = render(package_manager="pnpm")

    assert "pnpm install" in package.files["README.md"]
    assert "pnpm run test" in package.files["README.md"]
