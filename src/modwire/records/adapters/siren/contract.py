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
