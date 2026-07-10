from pathlib import Path
from tempfile import TemporaryDirectory

from wireup import injectable
from copier import run_copy

from .reader import QueryableCodeMapReader
from .package import CodePackage
from .writer import CodePackageWriter


@injectable(lifetime="transient")
class CodeService:
    def __init__(
        self,
        code_package_writer: CodePackageWriter,
        code_map_reader: QueryableCodeMapReader,
    ):
        self.code_package_writer = code_package_writer

    def read_source_code(self):
        pass

    def build_package(self, root: Path, data: dict) -> CodePackage:
        with TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            run_copy(
                str(root),
                str(temporary_path),
                data=data,
                defaults=True,
                overwrite=True,
                quiet=True,
            )

            files = {
                path.relative_to(temporary_path).as_posix(): path.read_text(encoding="utf-8")
                for path in temporary_path.rglob("*")
                if path.is_file()
            }

        return CodePackage(files=files)

    def write_package(self, package: CodePackage, destination: Path):
        self.code_package_writer.write(package, destination)

