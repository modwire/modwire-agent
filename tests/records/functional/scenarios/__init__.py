from __future__ import annotations

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modwire_agent.core.settings")

import django

django.setup()
