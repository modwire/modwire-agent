from ninja_extra import ControllerBase, api_controller


@api_controller("/variables", tags=["Variables"])
class VariableController(ControllerBase):
    pass
