from ninja_extra import ControllerBase, api_controller


@api_controller("/tags", tags=["Tags"])
class TagController(ControllerBase):
    pass
