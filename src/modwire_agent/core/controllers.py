from django.conf import settings
from ninja_extra import ControllerBase, api_controller, route


@api_controller("", tags=["Root"])
class RootController(ControllerBase):
    @route.get("/", response=dict, operation_id="get_api_root", summary="Discover the API.")
    def get(self):
        """Return links to the API's public entry points."""
        return {
            "title": "Modwire API",
            "version": settings.RELEASE_VERSION,
        }
