import hashlib
from pathlib import Path

import pytest
import yaml

from languages.models.language import Language
from scaffoldings.services.convergence import ScaffoldingConvergenceService
from scaffoldings.services.convergence.planner import ScaffoldingConvergencePlanner
from scaffoldings.services.convergence.validator import ScaffoldingAggregateValidator
from scaffoldings.services.convergence.writer import ScaffoldingAggregateWriter
from scaffoldings.services.highlighter import SyntaxHighlightingService
from scaffoldings.services.preview import ScaffoldingPreviewService
from scaffoldings.services.renderer import SandboxedTemplateRenderer
from scaffoldings.services.scaffolding import ScaffoldingService
from scaffoldings.services.variable_validation import VariableValidationService

ROOT = Path(__file__).parent
CONTRACT_PATH = ROOT / "fixtures" / "modwire-python-repository.yaml"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def convergence_service() -> ScaffoldingConvergenceService:
    return ScaffoldingConvergenceService(
        validator=ScaffoldingAggregateValidator(),
        planner=ScaffoldingConvergencePlanner(),
        writer=ScaffoldingAggregateWriter(),
    )


def preview_service() -> ScaffoldingPreviewService:
    return ScaffoldingPreviewService(
        scaffoldings=ScaffoldingService(),
        validation=VariableValidationService(),
        renderer=SandboxedTemplateRenderer(),
        highlighter=SyntaxHighlightingService(),
    )


def install_contract(language: Language) -> tuple[dict, str]:
    contract = load_yaml(CONTRACT_PATH)
    convergence_service().converge(
        language_id=language.id,
        name=contract["name"],
        description=contract["description"],
        variables=contract["variables"],
        templates=contract["templates"],
        dry_run=False,
    )
    scaffolding = ScaffoldingService().list().get(name=contract["name"])
    return contract, scaffolding.id


def rendered_files(scaffolding_id: str, values: dict[str, str]) -> list[dict[str, str]]:
    rendered = preview_service().preview(scaffolding_id, values, [])
    return [
        {
            "path": item["path"],
            "write_mode": item["write_mode"],
            "sha256": hashlib.sha256(item["source"].encode()).hexdigest(),
        }
        for item in rendered["files"]
    ]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("target", "expected_paths"),
    [
        ("core", ["src/modwire/architecture/__init__.py", "src/modwire/shared/__init__.py"]),
        ("cli", ["src/modwire_cli/application/__init__.py", "src/modwire_cli/shared/__init__.py"]),
        ("extraction", ["src/modwire_extraction/code/__init__.py", "src/modwire_extraction/shared/__init__.py"]),
        ("mermaid", ["src/modwire_mermaid/architecture/__init__.py", "src/modwire_mermaid/shared/__init__.py"]),
        ("siren", ["src/modwire_siren/client/__init__.py", "src/modwire_siren/shared/__init__.py"]),
    ],
)
def test_operational_package_previews_share_invariants(target: str, expected_paths: list[str]):
    language = Language.objects.create(name=f"{target} Python", executable="python", stable_version="3.14")
    contract, scaffolding_id = install_contract(language)

    first = rendered_files(scaffolding_id, contract["targets"][target])
    second = rendered_files(scaffolding_id, contract["targets"][target])

    assert first == second
    assert [(item["path"], item["write_mode"]) for item in first[:2]] == [
        (".modwire/boundaries.yaml", "managed"),
        (".modwire/shape.yaml", "managed"),
    ]
    assert [item["path"] for item in first[2:]] == expected_paths


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("target", "golden_name"),
    [("core", "modwire-repository-library.yaml"), ("cli", "modwire-repository-cli.yaml")],
)
def test_library_and_cli_renders_match_golden_shapes(target: str, golden_name: str):
    language = Language.objects.create(name=f"Golden {target}", executable="python", stable_version="3.14")
    contract, scaffolding_id = install_contract(language)

    assert {"files": rendered_files(scaffolding_id, contract["targets"][target])} == load_yaml(
        ROOT / "golden" / golden_name
    )


@pytest.mark.django_db
def test_preview_never_writes_application_source(tmp_path: Path):
    sentinel = tmp_path / "application.py"
    sentinel.write_text("owned by the application\n")
    language = Language.objects.create(name="Read-only Python", executable="python", stable_version="3.14")
    contract, scaffolding_id = install_contract(language)

    rendered_files(scaffolding_id, contract["targets"]["core"])

    assert sentinel.read_text() == "owned by the application\n"
    assert list(tmp_path.iterdir()) == [sentinel]


def test_contract_publishes_identity_and_excludes_the_scaffolding_host():
    contract = load_yaml(CONTRACT_PATH)

    assert contract["identity"] == "brNlYVlASiK8LKLHNCv15A"
    assert set(contract["targets"]) == {"core", "cli", "extraction", "mermaid", "siren"}
    assert "mcp" not in contract["targets"]
