from modwire_hex.django import DjangoNinja

from .controllers import RootController
from .error_handling import ExceptionHandlers

api = DjangoNinja.api()
ExceptionHandlers().configure(api)
api.register_controllers(RootController)
