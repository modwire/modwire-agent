from inspect import getfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Self

import yaml
from copier import run_copy
from pydantic import BaseModel

from .manifest import CopierManifest
from .package import CodePackage


class CopierArchive(BaseModel):
    manifest: dict[str, Any]
    templates: CodePackage

    @classmethod
    def load(cls, manifest_type: type[CopierManifest]) -> Self:
        archive_file = Path(getfile(manifest_type)).resolve()
        templates_directory = archive_file.parent / "templates"

        if not templates_directory.is_dir():
            raise FileNotFoundError(
                f"Templates directory not found: "
                f"{templates_directory}"
            )

        return cls(
            manifest=manifest_type.to_copier_config(),
            templates=CodePackage.from_directory(
                templates_directory
            ),
        )

    def write_to_directory(self, root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)

        subdirectory = self.manifest.get(
            "_subdirectory",
            "templates",
        )

        self.templates.write_to_directory(root / subdirectory)

        (root / "copier.yml").write_text(
            yaml.safe_dump(
                self.manifest,
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

    def render(self, data: dict[str, Any]) -> CodePackage:
        with (
            TemporaryDirectory() as source_directory,
            TemporaryDirectory() as output_directory,
        ):
            source = Path(source_directory)
            output = Path(output_directory)

            self.write_to_directory(source)

            run_copy(
                str(source),
                str(output),
                data=data,
                defaults=True,
                overwrite=True,
                quiet=True,
                unsafe=bool(
                    self.manifest.get("_jinja_extensions")
                ),
            )

            return CodePackage.from_directory(output)

"""
_min_copier_version: "9.0.0"
_templates_suffix: ".jinja"
_subdirectory: templates

project_name:
  type: str
  default: new_project
  help: Python distribution name.

project_package:
  type: str
  default: core
  help: Importable Django project package.

project_title:
  type: str
  default: New Project
  help: API title.

package_manager:
  type: str
  default: uv
  choices:
    - uv
    - poetry
    - pdm
  help: Package manager used by generated Makefile jobs.

dependencies:
  type: yaml
  when: false
  default:
    - dj-database-url
    - django
    - django-health-check
    - django-model-utils
    - django-ninja-extra
    - gunicorn
    - pgvector
    - psycopg[binary]
    - pydantic
    - python-dotenv
    - pyyaml
    - structlog
    - wireup

dev_dependencies:
  type: yaml
  when: false
  default:
    - openapi-python-client
    - pytest
    - pytest-django
    - ruff

"""