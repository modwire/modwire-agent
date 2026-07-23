from importlib import import_module

from .client import SirenClient


class SirenFunctionalTestCase:
    """Run an existing functional scenario against the Siren transport."""

    @staticmethod
    def api_path(path: str) -> str:
        return SirenClient._siren_path(path)

    @staticmethod
    def load_case(module: str, name: str) -> type:
        return getattr(import_module(module), name)

    def setUp(self) -> None:
        self.client = SirenClient(self.client)
        super().setUp()
