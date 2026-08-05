from dataclasses import dataclass

from wireup import injectable

from enclosure.shared import FilesPackage, FilesystemService


@injectable
@dataclass(frozen=True)
class FilesystemAdapter:
    filesystem: FilesystemService

    def read_files_package(self, root_dir: str) -> FilesPackage:
        return self.filesystem.read_directory(root_dir)
