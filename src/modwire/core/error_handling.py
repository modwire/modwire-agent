from typing import Any

import structlog
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404, HttpRequest, HttpResponse
from modwire_hex import DomainError
from ninja.errors import HttpError
from ninja.errors import ValidationError as NinjaValidationError

from modwire.scaffoldings.domain.preview import PreviewFailed

GENERIC_ERROR_MESSAGE = "Request failed."

logger = structlog.get_logger(__name__)


class ExceptionHandlers:
    def configure(self, api: Any) -> None:
        api.add_exception_handler(PreviewFailed, self.preview_failed_response)
        api.add_exception_handler(DomainError, self.domain_error_response)
        api.add_exception_handler(NinjaValidationError, self.validation_error_response)
        api.add_exception_handler(DjangoValidationError, self.validation_error_response)
        api.add_exception_handler(ValueError, self.validation_error_response)
        api.add_exception_handler(Http404, self.not_found_response)
        api.add_exception_handler(LookupError, self.not_found_response)
        api.add_exception_handler(HttpError, self.http_error_response)
        api.add_exception_handler(Exception, self.unexpected_error_response)

    def preview_failed_response(self, request: HttpRequest, error: PreviewFailed) -> HttpResponse:
        return self.response(request, {"errors": [item.as_dict() for item in error.errors]}, status=422)

    def domain_error_response(self, request: HttpRequest, error: DomainError) -> HttpResponse:
        return self.response(request, {"detail": str(error)}, status=422)

    def validation_error_response(self, request: HttpRequest, error: Exception) -> HttpResponse:
        return self.generic_error_response(request, error, status=422)

    def not_found_response(self, request: HttpRequest, error: Exception) -> HttpResponse:
        return self.generic_error_response(request, error, status=404)

    def http_error_response(self, request: HttpRequest, error: HttpError) -> HttpResponse:
        if isinstance(error.__cause__, DomainError):
            return self.domain_error_response(request, error.__cause__)
        return self.generic_error_response(request, error, status=error.status_code)

    def unexpected_error_response(self, request: HttpRequest, error: Exception) -> HttpResponse:
        return self.generic_error_response(request, error, status=500)

    def generic_error_response(self, request: HttpRequest, error: Exception, status: int) -> HttpResponse:
        logger.exception(
            "unhandled_api_exception",
            method=request.method,
            path=request.path,
            exception_type=type(error).__name__,
        )
        return self.response(request, {"detail": GENERIC_ERROR_MESSAGE}, status=status)

    @staticmethod
    def response(request: HttpRequest, payload: dict[str, Any], status: int) -> HttpResponse:
        from modwire_hex.django import DjangoNinja

        return DjangoNinja.api().create_response(request, payload, status=status)
