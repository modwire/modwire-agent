import ast
from pathlib import Path

from django.test import SimpleTestCase


class SirenTransportCoverageTests(SimpleTestCase):
    scenario_directories = (
        Path("core/functional"),
        Path("languages/functional"),
        Path("plans/functional"),
        Path("records/functional/scenarios"),
        Path("scaffoldings/functional"),
        Path("tokens/functional"),
    )
    excluded_modules = frozenset(
        {
            "tests.core.functional.test_cors",
            "tests.core.functional.test_health",
            "tests.core.functional.test_openapi",
            "tests.core.functional.test_siren_api",
        }
    )

    def test_every_eligible_rest_scenario_has_an_explicit_siren_counterpart(self) -> None:
        expected = self._rest_scenarios()
        mirrored = self._mirrored_scenarios()

        self.assertFalse(
            expected - mirrored,
            f"REST scenarios without a Siren counterpart: {sorted(expected - mirrored)}",
        )
        self.assertFalse(
            mirrored - expected,
            f"Siren counterparts without an eligible REST scenario: {sorted(mirrored - expected)}",
        )

    def _rest_scenarios(self) -> set[tuple[str, str]]:
        tests_root = self._tests_root()
        scenarios: set[tuple[str, str]] = set()
        for directory in self.scenario_directories:
            for path in (tests_root / directory).rglob("test_*.py"):
                module = self._module_name(tests_root, path)
                if module in self.excluded_modules:
                    continue
                tree = ast.parse(path.read_text())
                for node in tree.body:
                    if isinstance(node, ast.ClassDef) and any(
                        isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) and member.name.startswith("test_")
                        for member in node.body
                    ):
                        scenarios.add((module, node.name))
        return scenarios

    def _mirrored_scenarios(self) -> set[tuple[str, str]]:
        tests_root = self._tests_root()
        scenarios: set[tuple[str, str]] = set()
        for path in (tests_root / "siren" / "functional").rglob("test_*.py"):
            tree = ast.parse(path.read_text())
            imported_modules: dict[str, str] = {}
            for node in tree.body:
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("tests."):
                    imported_modules.update(
                        {alias.asname or alias.name: f"{node.module}.{alias.name}" for alias in node.names}
                    )
            for node in tree.body:
                if not isinstance(node, ast.ClassDef) or not node.name.startswith("TestSiren"):
                    continue
                for base in node.bases:
                    if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name):
                        module = imported_modules.get(base.value.id)
                        if module:
                            scenarios.add((module, base.attr))
        return scenarios

    @staticmethod
    def _tests_root() -> Path:
        return Path(__file__).parents[2]

    @staticmethod
    def _module_name(tests_root: Path, path: Path) -> str:
        return ".".join(("tests", *path.relative_to(tests_root).with_suffix("").parts))
