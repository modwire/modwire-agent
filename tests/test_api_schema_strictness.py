import json

import pytest
from pydantic import ValidationError

from core.api import api
from scaffoldings.api.template.schemas import TemplateIn, TemplatePatchIn
from scaffoldings.api.variable.schemas import VariableIn


def test_patch_fields_are_omittable_but_not_nullable():
    assert TemplatePatchIn().model_dump(exclude_unset=True, warnings=False) == {}
    with pytest.raises(ValidationError):
        TemplatePatchIn(relative_path=None)
    with pytest.raises(ValidationError):
        TemplatePatchIn(write_mode="overwrite")


def test_request_objects_reject_unknown_fields_and_enum_values():
    with pytest.raises(ValidationError):
        TemplateIn(
            scaffolding_id="scaffolding",
            relative_path="README.md",
            file_content="content",
            unknown=True,
        )
    with pytest.raises(ValidationError):
        VariableIn(
            scaffolding_id="scaffolding",
            name="name",
            type="yaml",
            description="description",
            default_value=[],
        )


def test_openapi_exposes_strict_objects_and_all_finite_options():
    components = api.get_openapi_schema()["components"]["schemas"]
    serialized = json.dumps(components)

    assert '"type": "null"' not in serialized
    assert '"additionalProperties": true' not in serialized
    assert components["VariableType"]["enum"] == ["str", "int", "float", "bool", "list", "dict"]
    assert components["WriteMode"]["enum"] == [
        "managed",
        "create_if_missing",
    ]
    assert "id" in components["ScaffoldingBundleVariableOut"]["required"]
    assert components["CommandResult"]["enum"] == [
        "init",
        "install",
        "add_runtime",
        "add_development",
        "add_optional",
        "add_peer",
        "remove",
        "update",
        "lock",
        "run",
        "publish",
        "audit",
    ]
    content_roles = [
        "heading",
        "subheading",
        "paragraph",
        "list",
        "markdown",
        "snippet",
        "image",
    ]
    assert components["ContentRole"]["enum"] == content_roles
    assert components["ContentIn"]["properties"]["role"]["enum"] == content_roles
