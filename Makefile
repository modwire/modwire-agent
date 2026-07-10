INSTALL := uv sync
RUN := uv run
ADD := uv add
REMOVE := uv remove
OA_SCHEMA ?= .dev/openapi.json
MODWIRE_REPORT ?= .dev/modwire-health.json
PORT ?= 8000

.PHONY: init dev m mm mz oa add remove modwire gen

init:
	mkdir -p .dev shared
	$(INSTALL)

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
	find $(app)/migrations -type f ! -name __init__.py -delete
	find $(app)/migrations -type d -name __pycache__ -prune -exec rm -rf {} +

oa:
	mkdir -p .dev shared
	$(RUN) python -c "import json, os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); django.setup(); from core.api import api; print(json.dumps(api.get_openapi_schema()))" > $(OA_SCHEMA)
	rm -rf shared/oa
	$(RUN) openapi-python-client generate --path $(OA_SCHEMA) --config openapi-python-client.yml --output-path shared/oa --overwrite --meta none

add:
	@test -n "$(pkg)" || (echo "usage: make add pkg=<pkg>" && exit 2)
	$(ADD) $(pkg)

remove:
	@test -n "$(pkg)" || (echo "usage: make remove pkg=<pkg>" && exit 2)
	$(REMOVE) $(pkg)

modwire:
	mkdir -p .dev
	@modwire -d .modwire architecture health . python > $(MODWIRE_REPORT)
	@jq -se '[.[] | if .metadata.id == "architecture.map" then .unknown_files[]? | {source_id: ., rule_name: "unknown_file"} elif .metadata.id == "architecture.violations.flow" then .violations[] elif .metadata.id == "architecture.violations.shape" then .violations[] | select(.rule_name == "allow_optional_class_properties") | select(.source_id | startswith("shared/oa/") | not) | select(.source_id | startswith("tests/") | not) | select(.source_id | contains("/migrations/") | not) else empty end] | if length == 0 then {"status": "healthy", "report": "$(MODWIRE_REPORT)"} else {"status": "violations", "report": "$(MODWIRE_REPORT)", "violations": .}, false end' $(MODWIRE_REPORT)

gen:
	modwire scaffolding generate modules/django-api-app \
		${app} \
		--data app_name=${app} \
		--data model_name=${model}
