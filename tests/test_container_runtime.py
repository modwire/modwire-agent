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
    assert compose["services"]["mcp-adapter"]["image"] == (
        "ghcr.io/modwire/modwire-mcp-adapter:${MODWIRE_MCP_VERSION:-latest}"
    )
    assert compose["services"]["scaffolding-api"]["image"] == (
        "ghcr.io/modwire/modwire-mcp-runtime:${MODWIRE_MCP_VERSION:-latest}"
    )
    assert "build" not in compose["services"]["mcp-adapter"]
    assert "build" not in compose["services"]["scaffolding-api"]
    assert compose["services"]["mcp-adapter"]["ports"] == [
        "127.0.0.1:${MCP_ADAPTER_PORT:-8200}:8200",
    ]


def test_api_image_startup_does_not_apply_migrations():
    dockerfile = (ROOT / "Dockerfile").read_text()
    runtime_command = dockerfile.rsplit("CMD", maxsplit=1)[-1]

    assert "gunicorn" in runtime_command
    assert "migrate" not in runtime_command


def test_local_image_builds_require_the_explicit_override():
    compose = yaml.safe_load((ROOT / "compose.build.yaml").read_text())

    assert compose["services"]["scaffolding-api"]["build"] == {"context": "."}
    assert compose["services"]["mcp-adapter"]["build"] == {
        "context": ".",
        "dockerfile": "Dockerfile.adapter",
    }


def test_release_publishes_both_images_for_intel_and_arm_hosts():
    workflow = yaml.load(
        (ROOT / ".github" / "workflows" / "publish-containers.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    publish = workflow["jobs"]["publish"]

    assert workflow["on"]["release"]["types"] == ["published"]
    assert workflow["permissions"] == {
        "contents": "read",
        "packages": "write",
        "attestations": "write",
        "id-token": "write",
    }
    assert publish["strategy"]["matrix"]["include"] == [
        {"dockerfile": "Dockerfile", "image": "modwire-mcp-runtime"},
        {
            "dockerfile": "Dockerfile.adapter",
            "image": "modwire-mcp-adapter",
        },
    ]
    build = next(
        step for step in publish["steps"] if step["name"] == "Build and push image"
    )
    assert build["with"]["platforms"] == "linux/amd64,linux/arm64"
    assert build["with"]["push"] == "true"
    assert build["with"]["sbom"] == "true"
    metadata = next(
        step
        for step in publish["steps"]
        if step["name"] == "Derive release tags and labels"
    )
    assert "value=${{ github.event.release.tag_name }}" in metadata["with"]["tags"]


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


def test_local_installer_keeps_the_api_key_out_of_output():
    installer = (ROOT / "scripts" / "install-local-mcp.sh").read_text()

    assert "shell --no-imports" in installer
    assert '>"${temporary_secret}"' in installer
    assert "chmod 600" in installer
    assert 'codex mcp add "${server_name}" --url "${server_url}"' in installer
    assert "docker compose pull scaffolding-api mcp-adapter" in installer
    assert "docker compose build" not in installer
    assert "--build" not in installer


def test_local_uninstaller_never_removes_volumes():
    uninstaller = (ROOT / "scripts" / "uninstall-local-mcp.sh").read_text()

    assert "docker compose down --remove-orphans" in uninstaller
    assert "--volumes" not in uninstaller
