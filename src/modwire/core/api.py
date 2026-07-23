from modwire_hex.django import DjangoNinja

from .error_handling import configure_exception_handlers

api = DjangoNinja.api()
configure_exception_handlers(api)
