INSTALL := uv sync
RUN := uv run
PY_RUN := PYTHONPATH=src $(RUN)
ADD := uv add
REMOVE := uv remove
OA_SCHEMA ?= .dev/openapi.json
MODWIRE_REPORT ?= .dev/modwire-health.json
PORT ?= 8000

.PHONY: init dev m mm mz oa add remove modwire gen runtime-config runtime-up runtime-build-up runtime-down runtime-db-prepare runtime-db-migrate mcp-up mcp-build-up mcp-health mcp-check mcp-install mcp-diagnose mcp-uninstall

init:
	mkdir -p .dev src/modwire/shared
	$(INSTALL)

apikey:
	$(RUN) python manage.py apikey

dev:
	$(RUN) python manage.py runserver $(PORT)

m:
	$(RUN) python manage.py migrate

mm:
	@test -n "$(app)" || (echo "usage: make mm app=<app>" && exit 2)
	$(RUN) python manage.py makemigrations $(app)

mz:
	@test -n "$(app)" || (echo "usage: make mz app=<app>" && exit 2)
	$(RUN) python manage.py migrate $(app) zero
	find src/modwire/apps/$(app)/migrations -type f ! -name __init__.py -delete
	find src/modwire/apps/$(app)/migrations -type d -name __pycache__ -prune -exec rm -rf {} +

oa:
	mkdir -p .dev src/modwire/shared
	$(PY_RUN) python -c "import json, os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modwire.core.settings'); django.setup(); from modwire.core.api import api; print(json.dumps(api.get_openapi_schema()))" > $(OA_SCHEMA)
	rm -rf src/modwire/shared/oa
	$(RUN) openapi-python-client generate --path $(OA_SCHEMA) --config openapi-python-client.yml --output-path src/modwire/shared/oa --overwrite --meta none

add:
	@test -n "$(pkg)" || (echo "usage: make add pkg=<pkg>" && exit 2)
	$(ADD) $(pkg)

remove:
	@test -n "$(pkg)" || (echo "usage: make remove pkg=<pkg>" && exit 2)
	$(REMOVE) $(pkg)

modwire:
	@mkdir -p .dev
	@modwire -d .modwire architecture health . python > $(MODWIRE_REPORT)
	@jq -se '[.[] | if .metadata.id == "architecture.map" then .unknown_files[]? | {source_id: ., rule_name: "unknown_file"} elif .metadata.id == "architecture.violations.flow" then .violations[] elif .metadata.id == "architecture.violations.shape" then .violations[] | select(.rule_name == "allow_optional_class_properties") | select(.source_id | startswith("src/modwire/shared/oa/") | not) | select(.source_id | startswith("tests/") | not) | select(.source_id | contains("/migrations/") | not) else empty end] | if length == 0 then {"status": "healthy", "report": "$(MODWIRE_REPORT)"} else {"status": "violations", "report": "$(MODWIRE_REPORT)", "violations": .}, false end' $(MODWIRE_REPORT)

gen:
	modwire scaffolding generate modules/django-api-app \
		${app} \
		--data app_name=${app} \
		--data model_name=${model}

runtime-config:
	docker compose config --quiet

runtime-up: runtime-config
	./scripts/pull-private-images.sh scaffolding-api
	docker compose up --detach scaffolding-api

runtime-build-up: runtime-config
	docker compose -f compose.yaml -f compose.build.yaml up --build --detach scaffolding-api

runtime-down:
	docker compose down

runtime-db-prepare: runtime-config
	./scripts/prepare-existing-database.sh

runtime-db-migrate: runtime-config
	./scripts/migrate-existing-database.sh

mcp-up: runtime-config
	./scripts/pull-private-images.sh scaffolding-api mcp-adapter
	docker compose up --detach scaffolding-api mcp-adapter

mcp-build-up: runtime-config
	docker compose -f compose.yaml -f compose.build.yaml up --build --detach scaffolding-api mcp-adapter

mcp-health:
	curl --fail http://127.0.0.1:$${MCP_ADAPTER_PORT:-8200}/health

mcp-check:
	$(RUN) python scripts/check-mcp-adapter.py

mcp-install:
	./scripts/install-local-mcp.sh

mcp-diagnose:
	./scripts/diagnose-local-mcp.sh

mcp-uninstall:
	./scripts/uninstall-local-mcp.sh
