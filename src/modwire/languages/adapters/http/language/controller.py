from ninja_extra import ControllerBase, api_controller


@api_controller("/languages", tags=["Languages"])
class LanguageController(ControllerBase):
    pass
