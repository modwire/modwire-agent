from modwire_hex import Module

from .use_cases.api_key import ApiKeyService


tokens = Module.auto("tokens", roots=(ApiKeyService,), bindings=())
