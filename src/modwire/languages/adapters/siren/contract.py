from typing import Final

RESOURCE_NAME: Final = "language"
RESOURCE_CLASS: Final = "language"

COLLECTION_ROUTE: Final = "/languages"
COLLECTION_PATH: Final = f"/siren{COLLECTION_ROUTE}"

IDENTIFIER_PROPERTY: Final = "id"
IDENTIFIER_PARAMETER: Final = "language_id"
ENTITY_ROUTE: Final = f"/{{{IDENTIFIER_PARAMETER}}}"
ENTITY_PATH: Final = f"{COLLECTION_PATH}{ENTITY_ROUTE}"

LIST_OPERATION: Final = "list_siren_languages"
GET_OPERATION: Final = "get_siren_language"
