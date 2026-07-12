from importlib import import_module
from inspect import isclass
from pkgutil import walk_packages

from django.apps import apps
from django.conf import settings
from ninja_extra import NinjaExtraAPI

from tokens.auth import ApiKeyAuth


class SirenAPI(NinjaExtraAPI):
    def get_openapi_schema(self, *args, **kwargs):
        schema = super().get_openapi_schema(*args, **kwargs)
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        components.update(
            {
                "SirenLink": {
                    "type": "object",
                    "required": ["rel", "href"],
                    "properties": {
                        "rel": {"type": "array", "items": {"type": "string"}},
                        "href": {"type": "string", "format": "uri"},
                        "title": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
                "SirenField": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["name", "type", "required"],
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "required": {"type": "boolean"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "value": {},
                        "options": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["value", "title"],
                                "properties": {"value": {}, "title": {"type": "string"}},
                            },
                        },
                        "schema": {},
                        "minimum": {"type": "number"},
                        "maximum": {"type": "number"},
                        "minLength": {"type": "integer"},
                        "maxLength": {"type": "integer"},
                        "pattern": {"type": "string"},
                    },
                },
                "SirenAction": {
                    "type": "object",
                    "required": ["name", "href", "method"],
                    "properties": {
                        "name": {"type": "string"},
                        "title": {"type": "string"},
                        "method": {"type": "string"},
                        "href": {"type": "string", "format": "uri"},
                        "type": {"type": "string"},
                        "fields": {"type": "array", "items": {"$ref": "#/components/schemas/SirenField"}},
                    },
                },
                "SirenEntity": {
                    "type": "object",
                    "required": ["class", "links"],
                    "properties": {
                        "class": {"type": "array", "items": {"type": "string"}},
                        "rel": {"type": "array", "items": {"type": "string"}},
                        "properties": {"type": "object"},
                        "links": {"type": "array", "items": {"$ref": "#/components/schemas/SirenLink"}},
                        "entities": {"type": "array", "items": {"$ref": "#/components/schemas/SirenEntity"}},
                        "actions": {"type": "array", "items": {"$ref": "#/components/schemas/SirenAction"}},
                    },
                },
                "Problem": {
                    "type": "object",
                    "required": ["type", "title", "status", "detail"],
                    "properties": {
                        "type": {"type": "string"},
                        "title": {"type": "string"},
                        "status": {"type": "integer"},
                        "detail": {},
                    },
                },
            }
        )
        for path_item in schema.get("paths", {}).values():
            for operation in path_item.values():
                if not isinstance(operation, dict) or "responses" not in operation:
                    continue
                for status, response in operation["responses"].items():
                    if status == "204":
                        continue
                    success = str(status).startswith("2")
                    media_type = "application/vnd.siren+json" if success else "application/problem+json"
                    model = "SirenEntity" if success else "Problem"
                    response["content"] = {media_type: {"schema": {"$ref": f"#/components/schemas/{model}"}}}
        return schema


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


for c in _controllers():
    api.register_controllers(c)
