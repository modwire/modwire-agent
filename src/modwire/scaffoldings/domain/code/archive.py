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
            raise FileNotFoundError(f"Templates directory not found: {templates_directory}")

        return cls(
            manifest=manifest_type.to_copier_config(),
            templates=CodePackage.from_directory(templates_directory),
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
                unsafe=bool(self.manifest.get("_jinja_extensions")),
            )

            return CodePackage.from_directory(output)
