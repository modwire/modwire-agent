import asyncio

import pytest

from languages.models.language import Language
from mcp_adapter.hypermedia import ExecuteRequest, InspectRequest, ItemStep, ModwireHypermedia, RelationStep
from mcp_adapter.transport import HttpxSirenTransport
from scaffoldings.models.scaffolding import Scaffolding
from scaffoldings.models.template import Template
from scaffoldings.services.convergence import ScaffoldingConvergenceService
from scaffoldings.services.convergence.planner import ScaffoldingConvergencePlanner
from scaffoldings.services.convergence.validator import ScaffoldingAggregateValidator
from scaffoldings.services.convergence.writer import ScaffoldingAggregateWriter
from tokens.models.api_key import ApiKey


def aggregate(language_id, *, dry_run=True):
    return {
        "language_id": language_id,
        "name": "Convergent Repository",
        "description": "A deterministic repository scaffold.",
        "variables": [
            {
                "name": "empty_mapping",
                "type": "dict",
                "description": "Optional mapping",
                "default_value": {},
                "required": False,
            },
            {
                "name": "empty_sequence",
                "type": "list",
                "description": "Optional sequence",
                "default_value": [],
                "required": False,
            },
            {
                "name": "package_name",
                "type": "str",
                "description": "Import package",
                "default_value": "example_package",
                "required": True,
            },
        ],
        "templates": [
            {
                "relative_path": "src/{{ package_name }}/__init__.py",
                "file_content": "",
                "write_mode": "create_if_missing",
            },
            {
                "relative_path": "src/{{ package_name }}/settings.py",
                "file_content": "SETTINGS = {{ empty_mapping }}\nPLUGINS = {{ empty_sequence }}\n",
                "write_mode": "managed",
            },
        ],
        "dry_run": dry_run,
    }


def convergence_service():
    return ScaffoldingConvergenceService(
        validator=ScaffoldingAggregateValidator(),
        planner=ScaffoldingConvergencePlanner(),
        writer=ScaffoldingAggregateWriter(),
    )


@pytest.mark.django_db
def test_convergence_dry_run_apply_and_repeat_are_deterministic():
    language = Language.objects.create(name="Convergence Python", executable="python", stable_version="3.14")
    service = convergence_service()

    dry_run = service.converge(**aggregate(language.id))
    assert dry_run == {
        "name": "Convergent Repository",
        "dry_run": True,
        "changed": True,
        "plan": {
            "scaffolding": "create",
            "variables": {
                "create": ["empty_mapping", "empty_sequence", "package_name"],
                "update": [],
                "delete": [],
            },
            "templates": {
                "create": [
                    "src/{{ package_name }}/__init__.py",
                    "src/{{ package_name }}/settings.py",
                ],
                "update": [],
                "delete": [],
            },
        },
    }
    assert not Scaffolding.objects.filter(name="Convergent Repository").exists()

    applied = service.converge(**aggregate(language.id, dry_run=False))
    repeated = service.converge(**aggregate(language.id, dry_run=False))

    assert applied["changed"] is True
    assert repeated["changed"] is False
    assert repeated["plan"]["scaffolding"] == "unchanged"
    assert repeated["plan"]["variables"] == {"create": [], "update": [], "delete": []}
    assert repeated["plan"]["templates"] == {"create": [], "update": [], "delete": []}
    scaffold = Scaffolding.objects.get(name="Convergent Repository")
    assert scaffold.variables.get(name="empty_sequence").default_value == []
    assert scaffold.variables.get(name="empty_mapping").default_value == {}
    assert scaffold.templates.get(relative_path__endswith="__init__.py").file_content == ""


@pytest.mark.django_db(transaction=True)
def test_convergence_rolls_back_the_complete_aggregate(monkeypatch):
    language = Language.objects.create(name="Rollback Python", executable="python", stable_version="3.14")
    original_save = Template.save

    def fail_second_template(instance, *args, **kwargs):
        if instance.relative_path.endswith("settings.py"):
            raise RuntimeError("forced write failure")
        return original_save(instance, *args, **kwargs)

    monkeypatch.setattr(Template, "save", fail_second_template)

    with pytest.raises(RuntimeError, match="forced write failure"):
        convergence_service().converge(**aggregate(language.id, dry_run=False))

    assert not Scaffolding.objects.filter(name="Convergent Repository").exists()
    assert not Template.objects.exists()


@pytest.mark.django_db(transaction=True)
def test_mcp_converges_and_previews_against_the_live_api(live_server):
    language = Language.objects.create(name="MCP Python", executable="python", stable_version="3.14")
    _, key = ApiKey.generate("convergence-mcp-test")
    hypermedia = ModwireHypermedia(
        f"{live_server.url}/api/",
        lambda: HttpxSirenTransport(key),
    )
    collection_path = (RelationStep(kind="relation", relation="scaffoldings"),)

    collection = asyncio.run(hypermedia.handle(InspectRequest(kind="inspect", path=collection_path))).document
    assert "converge_scaffolding" in {action["name"] for action in collection["actions"]}

    dry_run = asyncio.run(
        hypermedia.handle(
            ExecuteRequest(
                kind="execute",
                path=collection_path,
                action="converge_scaffolding",
                values=aggregate(language.id),
            )
        )
    ).document
    assert dry_run["properties"]["dry_run"] is True
    assert not Scaffolding.objects.filter(name="Convergent Repository").exists()

    applied = asyncio.run(
        hypermedia.handle(
            ExecuteRequest(
                kind="execute",
                path=collection_path,
                action="converge_scaffolding",
                values=aggregate(language.id, dry_run=False),
            )
        )
    ).document
    assert applied["properties"]["changed"] is True

    scaffold = Scaffolding.objects.get(name="Convergent Repository")
    item_path = (*collection_path, ItemStep(kind="item", identifier=scaffold.id))
    preview_request = ExecuteRequest(
        kind="execute",
        path=item_path,
        action="preview_scaffolding",
        values={"values": {"package_name": "example_package"}, "template_overrides": []},
    )
    first = asyncio.run(hypermedia.handle(preview_request)).document
    second = asyncio.run(hypermedia.handle(preview_request)).document

    assert first == second
    files = first["properties"]["files"]
    assert [item["path"] for item in files] == [
        "src/example_package/__init__.py",
        "src/example_package/settings.py",
    ]
    assert files[0]["source"] == ""
    assert files[0]["write_mode"] == "create_if_missing"
