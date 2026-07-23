dev:
	uv run manage.py runserver

modwire:
	@uv run modwire --architecture-root src --language python --summary
