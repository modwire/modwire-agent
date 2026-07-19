from typing import Final

RESOURCE_NAME: Final = "record"
RESOURCE_CLASS: Final = "record"

COLLECTION_ROUTE: Final = "/records"
COLLECTION_PATH: Final = f"/siren{COLLECTION_ROUTE}"

IDENTIFIER_PROPERTY: Final = "id"
IDENTIFIER_PARAMETER: Final = "record_id"
ENTITY_ROUTE: Final = f"/{{{IDENTIFIER_PARAMETER}}}"
ENTITY_PATH: Final = f"{COLLECTION_PATH}{ENTITY_ROUTE}"

LIST_OPERATION: Final = "list_siren_records"
GET_OPERATION: Final = "get_siren_record"
ASSIGN_TAGS_OPERATION: Final = "assign_siren_record_tags"
REPLACE_CONTENT_OPERATION: Final = "replace_siren_record_content"
PROPOSE_CONTENT_OPERATION: Final = "propose_siren_record_content"
PUBLISH_OPERATION: Final = "publish_siren_record"

SECTION_RESOURCE_NAME: Final = "section"
SECTION_COLLECTION_ROUTE: Final = "/sections"
SECTION_COLLECTION_PATH: Final = f"/siren{SECTION_COLLECTION_ROUTE}"
SECTION_IDENTIFIER_PARAMETER: Final = "section_id"
SECTION_ENTITY_ROUTE: Final = f"/{{{SECTION_IDENTIFIER_PARAMETER}}}"
SECTION_ENTITY_PATH: Final = f"{SECTION_COLLECTION_PATH}{SECTION_ENTITY_ROUTE}"
LIST_SECTIONS_OPERATION: Final = "list_siren_sections"
GET_SECTION_OPERATION: Final = "get_siren_section"
CREATE_SECTION_OPERATION: Final = "create_siren_section"
REPLACE_SECTION_PLACEMENTS_OPERATION: Final = "replace_siren_section_placements"
CREATE_SECTION_RECORD_OPERATION: Final = "create_siren_section_record"

TAG_RESOURCE_NAME: Final = "tag"
TAG_COLLECTION_ROUTE: Final = "/tags"
TAG_COLLECTION_PATH: Final = f"/siren{TAG_COLLECTION_ROUTE}"
LIST_TAGS_OPERATION: Final = "list_siren_tags"
CREATE_TAG_OPERATION: Final = "create_siren_tag"
