from modwire.core.siren import SirenModule

from .controller import RecordsSirenController
from .resources import RECORD_RESOURCES

SIREN_MODULE = SirenModule(
    name="records",
    resources=RECORD_RESOURCES,
    controllers=(RecordsSirenController,),
)
