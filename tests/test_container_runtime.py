from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_reuses_the_external_database_runtime():
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text())

    assert set(compose["services"]) == {"scaffolding-api", "mcp-adapter"}
    assert "postgres" not in compose["services"]
    assert "volumes" not in compose
    assert compose["networks"]["records"] == {
        "external": True,
        "name": "modwire-records_default",
    }
    assert compose["networks"]["services"] == {"internal": True}
    assert compose["services"]["scaffolding-api"]["ports"] == [
        "127.0.0.1:${SCAFFOLDING_API_PORT:-8100}:8000",
    ]
    assert compose["services"]["scaffolding-api"]["environment"]["DATABASE_HOST"] == "postgres"
    assert compose["services"]["scaffolding-api"]["environment"]["DATABASE_PORT"] == "5432"
    assert compose["services"]["mcp-adapter"]["networks"] == ["services", "edge"]
    assert "records" not in compose["services"]["mcp-adapter"]["networks"]
    assert "volumes" not in compose["services"]["mcp-adapter"]
    assert compose["services"]["mcp-adapter"]["image"] == "modwire-mcp-adapter"
    assert compose["services"]["scaffolding-api"]["image"] == "modwire-mcp-runtime"
    assert compose["services"]["mcp-adapter"]["build"]["dockerfile"] == "Dockerfile.adapter"
    assert compose["services"]["mcp-adapter"]["ports"] == [
        "127.0.0.1:${MCP_ADAPTER_PORT:-8200}:8200",
    ]


def test_api_image_startup_does_not_apply_migrations():
    dockerfile = (ROOT / "Dockerfile").read_text()
    runtime_command = dockerfile.rsplit("CMD", maxsplit=1)[-1]

    assert "gunicorn" in runtime_command
    assert "migrate" not in runtime_command


def test_adapter_image_contains_only_the_adapter_source():
    dockerfile = (ROOT / "Dockerfile.adapter").read_text()

    assert "--only-group mcp-adapter" in dockerfile
    assert "COPY mcp_adapter ./mcp_adapter" in dockerfile
    assert "COPY . ." not in dockerfile


def test_image_build_excludes_local_secrets_and_database_artifacts():
    ignored = set((ROOT / ".dockerignore").read_text().splitlines())

    assert ".env" in ignored
    assert ".env.*" in ignored
    assert ".dev" in ignored
