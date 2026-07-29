dev:
	uv run manage.py runserver

modwire:
	@uv run modwire --language python --summary

superuser:
	@uv run manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user, _ = User.objects.get_or_create(username='modwireagent', defaults={'email': 'modwireagent@localhost'}); user.email = 'modwireagent@localhost'; user.is_staff = True; user.is_superuser = True; user.set_password('modwireagent'); user.save(); print('Superuser modwireagent is ready.')"
