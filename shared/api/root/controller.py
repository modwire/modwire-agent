from ninja_extra import ControllerBase, api_controller, route

from shared.siren import SIREN_TYPE

COLLECTIONS = (
    "records",
    "sections",
    "tags",
    "contents",
    "scaffoldings",
    "templates",
    "variables",
    "languages",
    "package_managers",
    "commands",
    "tools",
    "tool_commands",
    "api_keys",
)


@api_controller("", tags=["Root"])
class RootController(ControllerBase):
    @route.get("/", response=dict, operation_id="get_api_root", summary="Discover the API.")
    def get(self):
        request = self.context.request
        absolute = request.build_absolute_uri
        return {
            "class": ["api", "entry-point"],
            "properties": {"title": "Modwire API", "version": "1.0.0"},
            "links": [
                {"rel": ["self"], "href": absolute("/api/")},
                *(
                    {
                        "rel": [name.replace("_", "-")],
                        "href": absolute(f"/api/{name}"),
                        "title": name.replace("_", " ").title(),
                    }
                    for name in COLLECTIONS
                ),
                {
                    "rel": ["service-desc"],
                    "href": absolute("/api/openapi.json"),
                    "type": "application/vnd.oai.openapi+json;version=3.1",
                },
                {"rel": ["browser"], "href": absolute("/browser/")},
            ],
            "actions": [],
            "mediaType": SIREN_TYPE,
        }
