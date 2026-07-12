from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_reuses_the_external_database_runtime():
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text())

    assert set(compose["services"]) == {"scaffolding-api"}
    assert compose["networks"] == {
        "records": {
            "external": True,
            "name": "modwire-records_default",
        },
    }
    assert compose["services"]["scaffolding-api"]["ports"] == [
        "127.0.0.1:${SCAFFOLDING_API_PORT:-8100}:8000",
    ]
    assert compose["services"]["scaffolding-api"]["environment"]["DATABASE_HOST"] == "postgres"
    assert compose["services"]["scaffolding-api"]["environment"]["DATABASE_PORT"] == "5432"


def test_api_image_startup_does_not_apply_migrations():
    dockerfile = (ROOT / "Dockerfile").read_text()
    runtime_command = dockerfile.rsplit("CMD", maxsplit=1)[-1]

    assert "gunicorn" in runtime_command
    assert "migrate" not in runtime_command


def test_image_build_excludes_local_secrets_and_database_artifacts():
    ignored = set((ROOT / ".dockerignore").read_text().splitlines())

    assert ".env" in ignored
    assert ".env.*" in ignored
    assert ".dev" in ignored
