from ...ports.operation.operation_catalog import OperationCatalog
from ...ports.operation.operation_handler import OperationHandler


class RegisteredOperationCatalog(OperationCatalog):
    def resolve(self, extension_key: str, extension_version: int) -> OperationHandler:
        raise LookupError(f"No operation is registered for {extension_key!r} v{extension_version}.")
