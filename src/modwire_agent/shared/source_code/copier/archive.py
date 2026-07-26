from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from copier import run_copy

from ..renderer import CodePackageRenderer

from .manifest import CopierManifest
from ..package import CodePackage


class CopierArchive(CodePackageRenderer):
    def render(self, root: Path, code_package: CodePackage) -> None:
        with (
            TemporaryDirectory() as source_directory,
            TemporaryDirectory() as output_directory,
        ):
            source = Path(source_directory)
            output = Path(output_directory)

            self._write_to_directory(source)

            run_copy(
                str(source),
                str(output),
                data=data,
                defaults=True,
                overwrite=True,
                quiet=True,
                unsafe=bool(self.manifest.get("_jinja_extensions")),
            )

            return CodePackage(files=output)
