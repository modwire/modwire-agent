from modwire_hex.django import DjangoNinja

from .error_handling import ExceptionHandlers

api = DjangoNinja.api()
ExceptionHandlers().configure(api)
