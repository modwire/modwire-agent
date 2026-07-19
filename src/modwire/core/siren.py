from functools import cache
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from modwire_siren import ModwireSirenFactory, SirenResourceSpec, inject_siren_resources
from modwire_siren.integrations.django import to_django_response
from modwire_siren.integrations.ninja_extra import NinjaExtraSirenResponse
from ninja_extra import NinjaExtraAPI

from .siren_module import SirenModule


class SirenApi:
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
            cls._api.register_controllers(SirenRootController, *cls.controllers())
        return cls._api

    @staticmethod
    @cache
    def modules() -> tuple[SirenModule, ...]:
        from modwire.languages.adapters.siren.module import SIREN_MODULE as languages
        from modwire.records.adapters.siren.module import SIREN_MODULE as records
        return languages, records

    @classmethod
    def resources(cls) -> tuple[SirenResourceSpec, ...]: return tuple(resource for module in cls.modules() for resource in module.resources)

    @classmethod
    def controllers(cls): return tuple(controller for module in cls.modules() for controller in module.controllers)

    @classmethod
    def project(cls, request: Any): return ModwireSirenFactory.web(cls.schema(), base_url_resolver=lambda value: value.build_absolute_uri("/")).for_request(request)

    @classmethod
    def schema(cls) -> dict[str, Any]: return inject_siren_resources(cls.api().get_openapi_schema(), cls.resources())

    @staticmethod
    def response(document: dict[str, Any]) -> HttpResponse: return to_django_response(NinjaExtraSirenResponse(body=document))


SirenNinja = SirenApi
siren_modules = SirenApi.modules
siren_resources = SirenApi.resources
siren_controllers = SirenApi.controllers
project_siren = SirenApi.project
siren_openapi_schema = SirenApi.schema
siren_response = SirenApi.response
