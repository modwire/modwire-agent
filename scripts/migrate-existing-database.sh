#!/bin/sh
set -eu

if [ "${CONFIRM_EXISTING_DATABASE_MIGRATION:-}" != "reviewed" ]; then
  printf '%s\n' 'Refusing migration. Review a backup and plan from prepare-existing-database.sh, then set CONFIRM_EXISTING_DATABASE_MIGRATION=reviewed.' >&2
  exit 2
fi

backup_path="${MODWIRE_DATABASE_BACKUP:?Set MODWIRE_DATABASE_BACKUP to the reviewed backup path}"
plan_path="${MODWIRE_DATABASE_MIGRATION_PLAN:?Set MODWIRE_DATABASE_MIGRATION_PLAN to the reviewed plan path}"

test -s "${backup_path}"
test -s "${plan_path}"

docker compose run --rm scaffolding-api python manage.py migrate --noinput
