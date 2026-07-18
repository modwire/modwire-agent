from ninja_extra import ControllerBase, api_controller


@api_controller("/contents", tags=["Contents"])
class ContentController(ControllerBase):
    pass
