from typing import Any

from django.conf import settings
from django.http import JsonResponse
from ninja_extra import ControllerBase, api_controller, route

from .siren import project_siren, siren_openapi_schema, siren_response


@api_controller("", tags=["Siren"])
class SirenRootController(ControllerBase):
    @route.get("/", response=dict, operation_id="get_siren_root")
    def get(self, request: Any):
        document = project_siren(request).root(
            self_href=request.build_absolute_uri(),
            title="Modwire Siren API",
            version=settings.RELEASE_VERSION,
            service_desc_href=request.build_absolute_uri("/siren/openapi.json"),
        )
        return siren_response(document)

    @route.get("/openapi.json", response=dict, operation_id="get_siren_openapi")
    def openapi(self, request: Any) -> JsonResponse:
        return JsonResponse(
            siren_openapi_schema(),
            content_type="application/vnd.oai.openapi+json;version=3.1",
        )
