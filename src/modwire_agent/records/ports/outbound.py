from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from ..domain.proposal.content_proposal import ContentProposal
from ..domain.record.content_revision import ContentRevision
from ..domain.record.record import Record
from ..domain.section.section import Section
from ..domain.tag.tag import Tag


class ContentProposalStore(ABC):
    @abstractmethod
    def for_record(self, record_id: UUID) -> list[ContentProposal]:
        raise NotImplementedError

    @abstractmethod
    def get(self, proposal_id: UUID) -> ContentProposal:
        raise NotImplementedError

    @abstractmethod
    def save(self, proposal: ContentProposal) -> None:
        raise NotImplementedError


class ContentStore(ABC):
    @abstractmethod
    def for_record(self, record_id: UUID) -> list[ContentRevision]:
        raise NotImplementedError

    @abstractmethod
    def has_revision(self, record_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def next_version(self, record_id: UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    def save(self, revision: ContentRevision) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RoutedRecord:
    identifier: UUID
    title: str
    matched_tag: str | None


class KnowledgeRouter(ABC):
    @abstractmethod
    def route(self, tag_names: list[str]) -> list[RoutedRecord]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class SearchResult:
    identifier: UUID
    title: str
    reason: str


class KnowledgeSearch(ABC):
    @abstractmethod
    def semantic(self, query: str) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def text(self, query: str) -> list[SearchResult]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RecordDetails:
    identifier: UUID
    title: str
    kind: str
    status: str
    tag_names: tuple[str, ...]


class RecordDetailsReader(ABC):
    @abstractmethod
    def get(self, record_id: UUID) -> RecordDetails:
        raise NotImplementedError


class RecordStore(ABC):
    @abstractmethod
    def get(self, record_id: UUID) -> Record:
        raise NotImplementedError

    @abstractmethod
    def save(self, record: Record) -> None:
        raise NotImplementedError


class SearchProjectionStore(ABC):
    @abstractmethod
    def index(self, record: Record) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class SectionSummary:
    identifier: UUID
    title: str
    allowed_kinds: tuple[str, ...]


class SectionCatalog(ABC):
    @abstractmethod
    def list(self) -> list[SectionSummary]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class SectionRecordDetails:
    identifier: UUID
    title: str
    kind: str
    status: str


@dataclass(frozen=True, slots=True)
class SectionDetails:
    identifier: UUID
    title: str
    allowed_kinds: tuple[str, ...]
    records: tuple[SectionRecordDetails, ...]


class SectionDetailsReader(ABC):
    @abstractmethod
    def get(self, section_id: UUID) -> SectionDetails:
        raise NotImplementedError


class SectionStore(ABC):
    @abstractmethod
    def get(self, section_id: UUID) -> Section:
        raise NotImplementedError

    @abstractmethod
    def save(self, section: Section) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class TagSummary:
    identifier: UUID
    name: str


class TagCatalog(ABC):
    @abstractmethod
    def list(self) -> list[TagSummary]:
        raise NotImplementedError


class TagStore(ABC):
    @abstractmethod
    def has_all(self, tag_ids: list[UUID]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save(self, tag: Tag) -> None:
        raise NotImplementedError
