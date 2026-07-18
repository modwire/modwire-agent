from modwire.shared.api.hypermedia import CollectionController

from .resource import language


@CollectionController(language)
class LanguageController:
    pass
