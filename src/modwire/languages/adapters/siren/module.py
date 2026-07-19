from modwire.core.siren_module import SirenModule

from .controller import LanguagesSirenController
from .resources import LANGUAGE_RESOURCES

SIREN_MODULE = SirenModule(
    name="languages",
    resources=LANGUAGE_RESOURCES,
    controllers=(LanguagesSirenController,),
)
