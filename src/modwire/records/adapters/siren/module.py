from modwire.core.siren_module import SirenModule

from .controller import RecordsSirenController
from .sections_controller import SectionsSirenController
from .tags_controller import TagsSirenController
from .resources import RECORD_RESOURCES

SIREN_MODULE = SirenModule(
    name="records",
    resources=RECORD_RESOURCES,
    controllers=(RecordsSirenController, SectionsSirenController, TagsSirenController),
)
