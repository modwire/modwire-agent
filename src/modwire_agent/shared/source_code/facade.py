from dataclasses import dataclass
from pathlib import Path

from ..languages import LanguagesService
from .package import SourceCodePackage
from .reader import CodePackageReader


@dataclass(frozen=True)
class SourceCodeService:
    reader: CodePackageReader
    languages: LanguagesService

    def read(self, root: Path, language: str) -> SourceCodePackage:
        extensions = self.languages.get_extensions(language)
        package = self.reader.read_package(root, extensions)
        return SourceCodePackage(language=language, package=package)
