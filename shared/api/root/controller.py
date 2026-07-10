from ninja_extra import ControllerBase, api_controller, route

from shared.api.siren import SIREN_TYPE, api_root_document


@api_controller("", tags=["Root"])
class RootController(ControllerBase):
    @route.get("/", response=dict, operation_id="get_api_root", summary="Discover the API.")
    def get(self):
        return {**api_root_document(self.context.request), "mediaType": SIREN_TYPE}
