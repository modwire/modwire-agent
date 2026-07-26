from uuid import NAMESPACE_URL, UUID, uuid5

from eventsourcing.application import AggregateNotFoundError, ProcessingEvent
from eventsourcing.domain import Aggregate, DomainEventProtocol, event
from eventsourcing.system import ProcessApplication


class Catalogue(Aggregate):
    identifier = uuid5(NAMESPACE_URL, "/records/catalogue")

    @event("CatalogueOpened")
    def __init__(self, id: UUID) -> None:
        self.events: list[dict[str, object]] = []

    @event
    def record(self, topic: str, payload: dict[str, object]) -> None:
        self.events.append({"topic": topic, **payload})


class RecordsProjection(ProcessApplication):
    name = "RecordsProjection"

    def catalogue(self) -> Catalogue:
        try:
            return self.repository.get(Catalogue.identifier)
        except AggregateNotFoundError:
            return Catalogue(id=Catalogue.identifier)

    def policy(self, event: DomainEventProtocol, processing_event: ProcessingEvent) -> None:
        catalogue = self.catalogue()
        catalogue.record(type(event).__qualname__, dict(vars(event)))
        processing_event.collect_events(catalogue)
