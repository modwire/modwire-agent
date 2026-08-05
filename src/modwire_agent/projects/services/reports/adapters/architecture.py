from dataclasses import dataclass
from pathlib import Path
from typing import Any

from modwire_architecture import ArchitectureConfig, Modwire
from wireup import injectable

from modwire_agent.shared import SourceCodeService


@injectable
@dataclass(frozen=True)
class ArchitectureAdapter:
    source_code: SourceCodeService

    def generate_reports(
        self,
        architecture_root: str,
        language: str,
        boundaries_yaml: str,
        shape_yaml: str,
    ) -> tuple[dict[str, Any], ...]:
        config = ArchitectureConfig.from_yaml("\n".join((boundaries_yaml, shape_yaml)))
        code_map = self.source_code.read_map(Path(architecture_root), language)
        reports = Modwire().architecture(config).report(code_map)
        return tuple(report.to_dict(mode="json") for report in reports)
