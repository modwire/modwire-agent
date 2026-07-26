from typing import Any

import wireup
from modwire_hex import DjangoApplication

from modwire_agent import shared
from modwire_agent.scaffoldings import services as scaffoldings_services


class AutowiredDjangoApplication(DjangoApplication):
    def create_container(self) -> Any:
        return wireup.create_sync_container(injectables=[shared, scaffoldings_services])


application = AutowiredDjangoApplication(modules=())
