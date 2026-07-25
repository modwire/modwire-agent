from ninja import Schema

from .bundle_template import ScaffoldingBundleTemplateOut
from .bundle_variable import ScaffoldingBundleVariableOut


class ScaffoldingBundleOut(Schema):
    id: str
    name: str
    variables: list[ScaffoldingBundleVariableOut]
    templates: list[ScaffoldingBundleTemplateOut]
