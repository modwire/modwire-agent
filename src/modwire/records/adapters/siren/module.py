from modwire.core.siren_module import SirenModule

from .controller import RecordsSirenController
from .sections_controller import SectionsSirenController
from .tags_controller import TagsSirenController
from .record_search_controller import RecordSearchSirenController
from .proposals_controller import ContentProposalsSirenController
from .revisions_controller import ContentRevisionsSirenController
from .resources import RECORD_RESOURCES

SIREN_MODULE = SirenModule(
    name="records",
    resources=RECORD_RESOURCES,
    controllers=(RecordsSirenController, RecordSearchSirenController, ContentProposalsSirenController, ContentRevisionsSirenController, SectionsSirenController, TagsSirenController),
)
