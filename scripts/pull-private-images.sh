/Users/gorky/.rvm/scripts/rvm:29: operation not permitted: ps
#!/bin/sh
set -eu

command -v gh >/dev/null
command -v docker >/dev/null

registry_config="$(mktemp -d)"
trap 'rm -rf "${registry_config}"' EXIT HUP INT TERM
username="$(gh api user --jq .login)"
images="$(docker compose config --images "$@")"
docker_host="$(docker context inspect --format '{{.Endpoints.docker.Host}}')"

if ! gh auth token | DOCKER_CONFIG="${registry_config}" docker login ghcr.io \
  --username "${username}" \
  --password-stdin \
  >/dev/null 2>&1; then
  printf '%s\n' 'Unable to authenticate Docker to private GHCR packages.' >&2
  exit 1
fi
for image in ${images}; do
  DOCKER_CONFIG="${registry_config}" DOCKER_HOST="${docker_host}" \
    docker pull "${image}"
done
