from dataclasses import dataclass

from wireup import injectable

from .adapters import FilesystemAdapter, LanguagesAdapter
from .model import DetectedStack


@injectable
@dataclass(frozen=True)
class StackDetector:
    languages: LanguagesAdapter
    filesystem: FilesystemAdapter

    def detect(self, project_root: str) -> DetectedStack:
        files_package = self.filesystem.read_files_package(project_root)
        return self.languages.sniff_project(files_package)
