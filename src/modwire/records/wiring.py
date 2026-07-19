from modwire_hex import Module, Providers

from .adapters.record.django_content_store import DjangoContentStore
from .adapters.proposal.django_content_proposal_store import DjangoContentProposalStore
from .adapters.record.django_knowledge_router import DjangoKnowledgeRouter
from .adapters.record.django_record_store import DjangoRecordStore
from .adapters.record.django_record_details_reader import DjangoRecordDetailsReader
from .adapters.section.django_section_store import DjangoSectionStore
from .adapters.section.django_section_details_reader import DjangoSectionDetailsReader
from .adapters.section.django_section_catalog import DjangoSectionCatalog
from .adapters.tag.django_tag_store import DjangoTagStore
from .adapters.tag.django_tag_catalog import DjangoTagCatalog
from .adapters.record.django_knowledge_search import DjangoKnowledgeSearch
from .adapters.record.django_search_projection_store import DjangoSearchProjectionStore
from .domain.record.content_schema_policy import ContentSchemaPolicy
from .domain.record.policy import RecordPolicy
from .domain.collaboration.policy import ActorPolicy
from .domain.proposal.policy import ContentProposalPolicy
from .domain.section.policy import SectionPolicy
from .domain.section.placement_policy import SectionPlacementPolicy
from .ports.record.content_store import ContentStore
from .ports.proposal.content_proposal_store import ContentProposalStore
from .ports.record.knowledge_router import KnowledgeRouter
from .ports.record.record_store import RecordStore
from .ports.record.record_details_reader import RecordDetailsReader
from .domain.tag.policy import TagPolicy
from .ports.section.section_store import SectionStore
from .ports.section.section_details_reader import SectionDetailsReader
from .ports.section.section_catalog import SectionCatalog
from .ports.tag.tag_store import TagStore
from .ports.tag.tag_catalog import TagCatalog
from .ports.record.knowledge_search import KnowledgeSearch
from .ports.record.search_projection_store import SearchProjectionStore
from .use_cases.record.create_record import CreateRecord
from .use_cases.section.create_section import CreateSection
from .use_cases.tag.create_tag import CreateTag
from .use_cases.tag.assign_tags import AssignTags
from .use_cases.record.build_knowledge_route import BuildKnowledgeRoute
from .use_cases.record.replace_content import ReplaceContent
from .use_cases.record.publish_record import PublishRecord
from .use_cases.section.reorder_section import ReorderSection
from .use_cases.record.list_content_revisions import ListContentRevisions
from .use_cases.proposal.propose_content import ProposeContent
from .use_cases.proposal.resolve_content_proposal import ResolveContentProposal
from .use_cases.record.get_record_details import GetRecordDetails
from .use_cases.section.get_section_details import GetSectionDetails
from .use_cases.proposal.list_content_proposals import ListContentProposals
from .use_cases.record.rename_record import RenameRecord
from .use_cases.section.list_sections import ListSections
from .use_cases.tag.list_tags import ListTags
from .use_cases.record.archive_record import ArchiveRecord
from .use_cases.record.search_records import SearchRecords


records = Module.auto(
    "records",
    roots=(CreateSection, CreateTag, CreateRecord, ReplaceContent, PublishRecord, AssignTags, BuildKnowledgeRoute, ReorderSection, ListContentRevisions, ProposeContent, ResolveContentProposal, GetRecordDetails, GetSectionDetails, ListContentProposals, RenameRecord, ListSections, ListTags, ArchiveRecord, SearchRecords),
    bindings=(
        Providers.bind(ContentStore, DjangoContentStore, "scoped", None),
        Providers.bind(ContentProposalStore, DjangoContentProposalStore, "scoped", None),
        Providers.bind(KnowledgeRouter, DjangoKnowledgeRouter, "scoped", None),
        Providers.bind(RecordStore, DjangoRecordStore, "scoped", None),
        Providers.bind(RecordDetailsReader, DjangoRecordDetailsReader, "scoped", None),
        Providers.bind(SectionStore, DjangoSectionStore, "scoped", None),
        Providers.bind(SectionDetailsReader, DjangoSectionDetailsReader, "scoped", None),
        Providers.bind(SectionCatalog, DjangoSectionCatalog, "scoped", None),
        Providers.bind(TagStore, DjangoTagStore, "scoped", None),
        Providers.bind(TagCatalog, DjangoTagCatalog, "scoped", None),
        Providers.bind(KnowledgeSearch, DjangoKnowledgeSearch, "scoped", None),
        Providers.bind(SearchProjectionStore, DjangoSearchProjectionStore, "scoped", None),
        Providers.singleton(ContentSchemaPolicy, None),
        Providers.singleton(ContentProposalPolicy, None),
        Providers.singleton(ActorPolicy, None),
        Providers.singleton(RecordPolicy, None),
        Providers.singleton(SectionPolicy, None),
        Providers.singleton(SectionPlacementPolicy, None),
        Providers.singleton(TagPolicy, None),
    ),
)
