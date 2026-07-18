from importlib import import_module
from inspect import isclass
from pkgutil import walk_packages

from django.apps import apps
from django.conf import settings
from ninja_extra import NinjaExtraAPI

from modwire.apps.tokens.auth import ApiKeyAuth

api = NinjaExtraAPI(title="Modwire API", version=settings.RELEASE_VERSION, auth=ApiKeyAuth())


def _import(name, root):
    try:
        return import_module(name)
    except ModuleNotFoundError as e:
        if e.name == name or e.name.startswith(root + "."):
            return None
        raise


def _mods(pkg, root):
    yield pkg
    if hasattr(pkg, "__path__"):
        for m in walk_packages(pkg.__path__, pkg.__name__ + "."):
            if mod := _import(m.name, root):
                yield mod


def _controllers():
    for app in apps.get_app_configs():
        pkg = _import(f"{app.name}.api", app.name)
        if not pkg:
            continue
        for mod in _mods(pkg, app.name):
            yield from (
                v
                for v in vars(mod).values()
                if isclass(v) and v.__module__ == mod.__name__ and v.__name__.endswith("Controller")
            )


CONTROLLERS = tuple(_controllers())

for c in CONTROLLERS:
    api.register_controllers(c)
