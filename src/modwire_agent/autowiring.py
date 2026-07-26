from typing import Any

import wireup
from modwire_hex import DjangoApplication

from modwire_agent import shared


class AutowiredDjangoApplication(DjangoApplication):
    def create_container(self) -> Any:
        return wireup.create_sync_container(injectables=[shared])


application = AutowiredDjangoApplication(modules=())
