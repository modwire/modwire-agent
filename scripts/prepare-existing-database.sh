#!/bin/sh
set -eu

database_container="${MODWIRE_DATABASE_CONTAINER:-modwire-records-postgres-1}"
database_network="${MODWIRE_DATABASE_NETWORK:-modwire-records_default}"
artifact_directory="${MODWIRE_DATABASE_ARTIFACT_DIRECTORY:-.dev/database-safety}"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_path="${artifact_directory}/modwire-records-${timestamp}.dump"
plan_path="${artifact_directory}/migration-plan-${timestamp}.txt"

docker inspect "${database_container}" >/dev/null
docker network inspect "${database_network}" >/dev/null
mkdir -p "${artifact_directory}"

docker exec "${database_container}" sh -c \
  'exec pg_dump --format=custom --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"' \
  >"${backup_path}"

docker compose build scaffolding-api
docker compose run --rm scaffolding-api python manage.py migrate --plan \
  >"${plan_path}"

test -s "${backup_path}"
test -s "${plan_path}"

printf 'Backup: %s\nMigration plan: %s\n' "${backup_path}" "${plan_path}"
