from typing import Any

import structlog
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse

from .errors import DomainError

logger = structlog.get_logger(__name__)


class ExceptionHandlers:
    def configure(self, api: Any) -> None:
        api.add_exception_handler(ObjectDoesNotExist, self.not_found_response)
        api.add_exception_handler(DomainError, self.domain_error_response)
        api.add_exception_handler(Exception, self.unexpected_error_response)

    def not_found_response(self, request: HttpRequest, error: ObjectDoesNotExist) -> HttpResponse:
        return self.response(request, {"detail": "Resource not found."}, status=404)

    def domain_error_response(self, request: HttpRequest, error: DomainError) -> HttpResponse:
        return self.response(request, {"detail": str(error)}, status=422)

    def unexpected_error_response(self, request: HttpRequest, error: Exception) -> HttpResponse:
        return self.response(request, {"detail": str(error)}, status=500)

    @staticmethod
    def response(request: HttpRequest, payload: dict[str, Any], status: int) -> HttpResponse:
        from modwire_hex.django import DjangoNinja

        return DjangoNinja.api().create_response(request, payload, status=status)
