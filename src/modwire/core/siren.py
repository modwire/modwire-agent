from dataclasses import dataclass
from functools import cache
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from modwire_siren import ModwireSirenFactory, SirenResourceSpec, inject_siren_resources
from modwire_siren.integrations.django import to_django_response
from modwire_siren.integrations.ninja_extra import NinjaExtraSirenResponse
from ninja_extra import ControllerBase, NinjaExtraAPI


@dataclass(frozen=True, slots=True)
class SirenModule:
    """One module's complete contribution to the Siren API."""

    name: str
    resources: tuple[SirenResourceSpec, ...]
    controllers: tuple[type[ControllerBase], ...]


@cache
def siren_modules() -> tuple[SirenModule, ...]:
    from modwire.languages.adapters.siren.module import SIREN_MODULE as languages
    from modwire.records.adapters.siren.module import SIREN_MODULE as records

    return languages, records


def siren_resources() -> tuple[SirenResourceSpec, ...]:
    return tuple(resource for module in siren_modules() for resource in module.resources)


def siren_controllers() -> tuple[type[ControllerBase], ...]:
    return tuple(controller for module in siren_modules() for controller in module.controllers)


class SirenNinja:
    _api: NinjaExtraAPI | None = None

    @classmethod
    def api(cls) -> NinjaExtraAPI:
        if cls._api is None:
            from modwire.core.siren_controller import SirenRootController

            configuration = dict(settings.MODWIRE["NINJA"])
            configuration.update(
                title=f"{configuration['title']} Siren",
                urls_namespace="modwire-siren",
                app_name="modwire-siren",
                openapi_url=None,
                docs_url=None,
            )
            cls._api = NinjaExtraAPI(**configuration)
            cls._api.register_controllers(SirenRootController, *siren_controllers())
        return cls._api


def project_siren(request: Any):
    schema = siren_openapi_schema()
    factory = ModwireSirenFactory.web(schema, base_url_resolver=lambda value: value.build_absolute_uri("/"))
    return factory.for_request(request)


def siren_openapi_schema() -> dict[str, Any]:
    return inject_siren_resources(SirenNinja.api().get_openapi_schema(), siren_resources())


def siren_response(document: dict[str, Any]) -> HttpResponse:
    return to_django_response(NinjaExtraSirenResponse(body=document))
