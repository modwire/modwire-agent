from typing import Any

from django.conf import settings
from django.http import HttpResponse
from modwire_siren import ModwireSirenFactory, SirenResourceSpec, inject_siren_resources
from modwire_siren.integrations.django import to_django_response
from modwire_siren.integrations.ninja_extra import NinjaExtraSirenResponse
from ninja_extra import NinjaExtraAPI


class SirenResourceRegistry:
    def __init__(self) -> None:
        self._resources: dict[str, SirenResourceSpec] = {}

    @property
    def resources(self) -> tuple[SirenResourceSpec, ...]:
        return tuple(self._resources.values())

    def register(self, *resources: SirenResourceSpec) -> None:
        for resource in resources:
            if resource.name in self._resources:
                raise ValueError(f"Siren resource is already registered: {resource.name}")
            self._resources[resource.name] = resource

    def enrich_openapi(self, schema: dict[str, Any]) -> dict[str, Any]:
        return inject_siren_resources(schema, self.resources)


resources = SirenResourceRegistry()


def register_module_resources() -> None:
    from modwire.languages.adapters.siren.resources import LANGUAGE_RESOURCES
    from modwire.records.adapters.siren.resources import RECORD_RESOURCES

    resources.register(*LANGUAGE_RESOURCES, *RECORD_RESOURCES)


register_module_resources()


class SirenNinja:
    _api: NinjaExtraAPI | None = None

    @classmethod
    def api(cls) -> NinjaExtraAPI:
        if cls._api is None:
            from modwire.core.siren_controller import SirenRootController
            from modwire.languages.adapters.siren.controller import LanguagesSirenController
            from modwire.records.adapters.siren.controller import RecordsSirenController

            configuration = dict(settings.MODWIRE["NINJA"])
            configuration.update(
                title=f"{configuration['title']} Siren",
                urls_namespace="modwire-siren",
                app_name="modwire-siren",
                openapi_url=None,
                docs_url=None,
            )
            cls._api = NinjaExtraAPI(**configuration)
            cls._api.register_controllers(SirenRootController, LanguagesSirenController, RecordsSirenController)
        return cls._api


def project_siren(request: Any):
    schema = siren_openapi_schema()
    factory = ModwireSirenFactory.web(schema, base_url_resolver=lambda value: value.build_absolute_uri("/"))
    return factory.for_request(request)


def siren_openapi_schema() -> dict[str, Any]:
    return resources.enrich_openapi(SirenNinja.api().get_openapi_schema())


def siren_response(document: dict[str, Any]) -> HttpResponse:
    return to_django_response(NinjaExtraSirenResponse(body=document))
