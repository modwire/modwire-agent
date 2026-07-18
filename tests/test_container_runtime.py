import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_compose_reuses_the_external_database_runtime():
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text())

    assert set(compose["services"]) == {"scaffolding-api", "mcp-adapter"}
    assert compose["name"] == "modwire-agent"
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
        "ghcr.io/modwire/modwire-agent-adapter:${MODWIRE_MCP_VERSION:-latest}"
    )
    assert compose["services"]["scaffolding-api"]["image"] == (
        "ghcr.io/modwire/modwire-agent-runtime:${MODWIRE_MCP_VERSION:-latest}"
    )
    assert "build" not in compose["services"]["mcp-adapter"]
    assert "build" not in compose["services"]["scaffolding-api"]
    assert compose["services"]["mcp-adapter"]["ports"] == [
        "127.0.0.1:${MCP_ADAPTER_PORT:-8200}:8200",
    ]


def test_declares_exact_direct_modwire_dependencies():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    dependencies = project["project"]["dependencies"]
    modwire_dependencies = sorted(dependency for dependency in dependencies if dependency.startswith("modwire-"))

    assert modwire_dependencies == [
        "modwire-architecture>=6.0.0,<7",
        "modwire-mermaid>=1.0.1,<2",
        "modwire-siren>=1.2.0,<2",
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
        "artifact-metadata": "write",
        "id-token": "write",
    }
    assert publish["strategy"]["matrix"]["include"] == [
        {"dockerfile": "Dockerfile", "image": "modwire-agent-runtime"},
        {
            "dockerfile": "Dockerfile.adapter",
            "image": "modwire-agent-adapter",
        },
    ]
    build = next(
        step for step in publish["steps"] if step["name"] == "Build and push image"
    )
    assert build["with"]["platforms"] == "linux/amd64,linux/arm64"
    assert build["with"]["push"] == "true"
    assert build["with"]["sbom"] == "true"
    assert build["with"]["cache-to"] == (
        "type=gha,mode=max,scope=${{ matrix.image }},timeout=2m,ignore-error=true"
    )
    assert build["with"]["build-args"] == (
        "MODWIRE_MCP_VERSION=${{ steps.metadata.outputs.version }}"
    )
    metadata = next(
        step
        for step in publish["steps"]
        if step["name"] == "Derive release tags and labels"
    )
    assert "value=${{ github.event.release.tag_name }}" in metadata["with"]["tags"]


def test_release_does_not_deploy_the_existing_coolify_application():
    workflow = yaml.load(
        (ROOT / ".github" / "workflows" / "publish-containers.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    assert "deploy-scaffolding-api" not in workflow["jobs"]


def test_adapter_image_contains_only_the_adapter_source():
    dockerfile = (ROOT / "Dockerfile.adapter").read_text()
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())

    assert "--only-group mcp-adapter" in dockerfile
    assert "COPY mcp_adapter ./mcp_adapter" in dockerfile
    assert "COPY . ." not in dockerfile
    assert "modwire-siren>=1.2.0,<2" in project["dependency-groups"]["mcp-adapter"]


def test_build_caches_are_kept_outside_both_runtime_copy_roots():
    api_dockerfile = (ROOT / "Dockerfile").read_text()
    adapter_dockerfile = (ROOT / "Dockerfile.adapter").read_text()

    assert "UV_CACHE_DIR=/tmp/uv-cache" in api_dockerfile
    assert "UV_CACHE_DIR=/tmp/uv-cache" in adapter_dockerfile
    assert "COPY --from=builder /app /app" in api_dockerfile
    assert "COPY --from=builder /app /app" in adapter_dockerfile


def test_browser_builder_runs_once_on_the_native_build_platform():
    dockerfile = (ROOT / "Dockerfile").read_text()

    assert "FROM --platform=$BUILDPLATFORM node:22-alpine AS browser-builder" in dockerfile


def test_release_version_is_embedded_in_both_runtime_images():
    api_dockerfile = (ROOT / "Dockerfile").read_text()
    adapter_dockerfile = (ROOT / "Dockerfile.adapter").read_text()

    assert "ARG MODWIRE_MCP_VERSION=0.0.0+dev" in api_dockerfile
    assert 'MODWIRE_MCP_VERSION="$MODWIRE_MCP_VERSION"' in api_dockerfile
    assert "ARG MODWIRE_MCP_VERSION=0.0.0+dev" in adapter_dockerfile
    assert 'MCP_ADAPTER_VERSION="$MODWIRE_MCP_VERSION"' in adapter_dockerfile


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
    assert "./scripts/pull-private-images.sh scaffolding-api mcp-adapter" in installer
    assert "docker compose build" not in installer
    assert "--build" not in installer


def test_private_image_pull_uses_disposable_docker_credentials():
    puller = (ROOT / "scripts" / "pull-private-images.sh").read_text()

    assert "gh auth token" in puller
    assert 'DOCKER_CONFIG="${registry_config}"' in puller
    assert "docker login ghcr.io" in puller
    assert 'docker compose config --images "$@"' in puller
    assert "docker context inspect" in puller
    assert 'DOCKER_HOST="${docker_host}"' in puller
    assert 'docker pull "${image}"' in puller
    assert "mktemp -d" in puller
    assert "rm -rf" in puller


def test_local_uninstaller_never_removes_volumes():
    uninstaller = (ROOT / "scripts" / "uninstall-local-mcp.sh").read_text()

    assert "docker compose down --remove-orphans" in uninstaller
    assert "--volumes" not in uninstaller
