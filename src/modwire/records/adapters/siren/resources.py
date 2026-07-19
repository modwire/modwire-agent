from modwire_siren import SirenResourceSpec

from .contract import (
    ENTITY_PATH,
    GET_OPERATION,
    IDENTIFIER_PARAMETER,
    IDENTIFIER_PROPERTY,
    LIST_OPERATION,
    RESOURCE_CLASS,
    RESOURCE_NAME,
)

RECORD_RESOURCES = (
    SirenResourceSpec(
        name=RESOURCE_NAME,
        path=ENTITY_PATH,
        resource_class=RESOURCE_CLASS,
        identifier=IDENTIFIER_PROPERTY,
        path_parameters={IDENTIFIER_PARAMETER: IDENTIFIER_PROPERTY},
        relations={},
        operations=(GET_OPERATION,),
        collection_operations=(LIST_OPERATION,),
    ),
)
