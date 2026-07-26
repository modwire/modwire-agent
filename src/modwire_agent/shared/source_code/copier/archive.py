from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from copier import run_copy
from wireup import injectable

from ..code_map import QueryableCodeMapReader, SourceCodeMap
from ..package import SourceCodePackage
from ..renderer import SourceCodeRenderer
from ..writer import CodePackageWriter


@injectable(as_type=SourceCodeRenderer)
@dataclass(frozen=True)
class CopierArchive(SourceCodeRenderer):
    writer: CodePackageWriter
    code_map_reader: QueryableCodeMapReader

    def render(
        self,
        source: SourceCodePackage,
        data: Mapping[str, object],
    ) -> SourceCodeMap:
        with TemporaryDirectory() as template_directory, TemporaryDirectory() as output_directory:
            template = Path(template_directory)
            root = Path(output_directory)
            self.writer.write(source.package, template, overwrite=True)
            run_copy(
                str(template),
                str(root),
                data=dict(data),
                defaults=True,
                overwrite=True,
                quiet=True,
            )
            return SourceCodeMap(
                source=source,
                code_map=self.code_map_reader.read(root, source.language),
            )
