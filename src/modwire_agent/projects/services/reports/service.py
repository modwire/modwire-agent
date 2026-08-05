from dataclasses import dataclass

from wireup import injectable

from .adapters import ArchitectureAdapter
from .model import HealthReport, InsightsReport


@injectable
@dataclass(frozen=True)
class ReportsService:
    architecture: ArchitectureAdapter

    def generate_health_report(
        self,
        architecture_root: str,
        language: str,
        boundaries_yaml: str,
        shape_yaml: str,
    ) -> HealthReport:
        reports = self.architecture.generate_reports(
            architecture_root,
            language,
            boundaries_yaml,
            shape_yaml,
        )
        health_reports = tuple(report for report in reports if "violations" in report)
        return HealthReport(
            healthy=all(not report["violations"] for report in health_reports),
            reports=health_reports,
        )

    def generate_insights_report(
        self,
        architecture_root: str,
        language: str,
        boundaries_yaml: str,
        shape_yaml: str,
    ) -> InsightsReport:
        reports = self.architecture.generate_reports(
            architecture_root,
            language,
            boundaries_yaml,
            shape_yaml,
        )
        return InsightsReport(
            reports=tuple(report for report in reports if "violations" not in report),
        )
