import json
import runpy
from importlib import import_module
from pathlib import Path

import pytest
from django.core.exceptions import ValidationError as DjangoValidationError
from django.test import RequestFactory
from pydantic import TypeAdapter, ValidationError

from core.api import api
from records.api.content.schemas import ContentIn
from records.api.schemas.content import ContentBlock
from records.models.content import Content
from records.services.record import RecordService
from scaffoldings.api.template.schemas import TemplateIn, TemplatePatchIn
from scaffoldings.api.variable.schemas import VariableIn
from scaffoldings.models.template import Template
from scaffoldings.models.variable import Variable
from shared.api.siren import _actions
from shared.oa.models.content_block import ContentBlock as GeneratedContentBlock
from shared.oa.models.record_out import RecordOut as GeneratedRecordOut


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


def test_variable_model_accepts_empty_defaults_before_type_validation():
    field = Variable._meta.get_field("default_value")

    assert field.clean("", None) == ""
    assert field.clean([], None) == []
    assert field.clean({}, None) == {}


def test_template_model_accepts_empty_initializer_content():
    field = Template._meta.get_field("file_content")

    assert field.clean("", None) == ""
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
    content_roles = [role.value for role in Content.Role]
    assert components["ContentRole"]["enum"] == content_roles
    assert components["ContentIn"]["properties"]["role"]["$ref"].endswith("/ContentRole")
    assert components["ContentOut"]["properties"]["role"]["$ref"].endswith("/ContentRole")
    assert components["ContentBlock"]["properties"]["content"]["anyOf"] == [
        {"type": "string"},
        {"items": {"type": "string"}, "type": "array"},
    ]
    assert components["ContentBlock"]["allOf"][0]["if"]["properties"]["role"]["const"] == Content.Role.LIST
    assert components["ContentBlock"]["properties"]["language"]["minLength"] == 1
    assert set(components["ContentMetadata"]["properties"]) == {
        "source",
        "source_url",
        "alt",
        "title",
        "format",
        "accepted_on",
    }


def test_content_blocks_enforce_role_specific_content_shapes():
    adapter = TypeAdapter(ContentBlock)
    common = {"language": "en", "metadata": {}}

    assert adapter.validate_python(
        {"role": Content.Role.LIST, "content": ["One", "Two"], **common}
    ).content == ["One", "Two"]
    with pytest.raises(ValidationError):
        adapter.validate_python({"role": Content.Role.LIST, "content": "One\nTwo", **common})
    with pytest.raises(ValidationError):
        adapter.validate_python({"role": Content.Role.PARAGRAPH, "content": ["One"], **common})
    with pytest.raises(ValidationError):
        adapter.validate_python(
            {"role": Content.Role.SNIPPET, "content": "print('hello')", "language": "", "metadata": {}}
        )

    resource = TypeAdapter(ContentIn).validate_python(
        {
            "record_slug": "section/record",
            "position": 0,
            "role": Content.Role.LIST,
            "content": ["One", "Two"],
            **common,
        }
    )
    assert resource.content == ["One", "Two"]
    accepted = adapter.validate_python(
        {
            "role": Content.Role.PARAGRAPH,
            "content": "Accepted governance",
            "language": "en",
            "metadata": {"source": "owner-directive", "accepted_on": "2026-07-12"},
        }
    )
    assert accepted.metadata.accepted_on == "2026-07-12"


def test_persistence_contract_rejects_role_content_mismatches():
    valid_list = Content(
        record_id="section/record",
        position=0,
        role=Content.Role.LIST,
        content=["One", "Two"],
        language="en",
        metadata={},
    )
    valid_list.clean()

    valid_list.content = "One\nTwo"
    with pytest.raises(DjangoValidationError):
        valid_list.clean()

    valid_list.role = Content.Role.PARAGRAPH
    valid_list.content = ["One"]
    with pytest.raises(DjangoValidationError):
        valid_list.clean()

    assert RecordService.content_text(["One", "Two"]) == "One\nTwo"


def test_content_migration_is_reversible_for_every_content_shape():
    migration = import_module("records.migrations.0002_content_json")

    list_source = "One\nTwo"
    list_value = migration.encode_content(Content.Role.LIST, list_source)
    assert list_value == ["One", "Two"]
    assert migration.decode_content(list_value) == list_source

    source = "print('hello')"
    value = migration.encode_content(Content.Role.SNIPPET, source)
    assert value == source
    assert migration.decode_content(value) == source


def test_siren_actions_bundle_complex_schemas_without_openapi_references():
    request = RequestFactory().get("/api/records", HTTP_HOST="localhost")
    action = next(
        item for item in _actions(request, "/records", None) if item["name"] == "create_record"
    )
    field = next(item for item in action["fields"] if item["name"] == "content")
    serialized = json.dumps(field["schema"])

    assert field["type"] == "json"
    assert "$ref" not in serialized
    item_schema = field["schema"]["items"]
    assert item_schema["properties"]["role"]["enum"] == [role.value for role in Content.Role]
    assert item_schema["allOf"][0]["then"]["properties"]["content"]["type"] == "array"


def test_generated_client_deserializes_the_discriminated_content_variant():
    record = GeneratedRecordOut.from_dict(
        {
            "slug": "section/record",
            "local_slug": "record",
            "section_slug": "section",
            "title": "Record",
            "description": "Description",
            "sources": [],
            "tag_slugs": [],
            "content": [
                {
                    "role": Content.Role.LIST,
                    "content": ["First item", "Second item"],
                    "language": "en",
                    "metadata": {},
                }
            ],
        }
    )

    assert isinstance(record.content[0], GeneratedContentBlock)
    assert record.content[0].content == ["First item", "Second item"]


def test_browser_content_roles_are_generated_from_the_model_enum():
    root = Path(__file__).resolve().parents[1]
    generator = runpy.run_path(str(root / "scripts/generate-browser-content-roles.py"))
    generated = root / "browser/src/models/recordContent.generated.ts"

    assert generated.read_text() == generator["render"]()


def test_public_json_schemas_are_generated_with_github_ids():
    root = Path(__file__).resolve().parents[1]
    generator = runpy.run_path(str(root / "scripts/generate-json-schemas.py"))

    for name, expected in generator["render"]().items():
        schema = json.loads(expected)
        assert schema["$id"] == (
            f"https://raw.githubusercontent.com/modwire/modwire-mcp/main/schemas/{name}"
        )
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert (root / "schemas" / name).read_text() == expected
