from importlib import import_module
from inspect import isclass
from pkgutil import walk_packages

from django.apps import apps
from django.conf import settings
from modwire_siren import inject_siren_resources
from modwire_siren.openapi.response_api import enrich_siren_openapi
from ninja_extra import NinjaExtraAPI

from modwire.apps.tokens.auth import ApiKeyAuth
from modwire.shared.api.hypermedia import collect_resources, collect_siren_resources


class SirenAPI(NinjaExtraAPI):
    def get_openapi_schema(self, *args, **kwargs):
        schema = super().get_openapi_schema(*args, **kwargs)
        return inject_siren_resources(enrich_siren_openapi(schema), SIREN_RESOURCE_SPECS)


api = SirenAPI(title="Modwire Siren API", version=settings.RELEASE_VERSION, auth=ApiKeyAuth())


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
RESOURCE_SPECS = collect_resources(*CONTROLLERS)
SIREN_RESOURCE_SPECS = collect_siren_resources(*CONTROLLERS)

for c in CONTROLLERS:
    api.register_controllers(c)
