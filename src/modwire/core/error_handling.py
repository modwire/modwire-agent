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
    @staticmethod
    def configure(api: Any) -> None:
        api.add_exception_handler(PreviewFailed, ExceptionHandlers.preview_failed_response)
        api.add_exception_handler(DomainError, ExceptionHandlers.domain_error_response)
        api.add_exception_handler(NinjaValidationError, ExceptionHandlers.validation_error_response)
        api.add_exception_handler(DjangoValidationError, ExceptionHandlers.validation_error_response)
        api.add_exception_handler(ValueError, ExceptionHandlers.validation_error_response)
        api.add_exception_handler(Http404, ExceptionHandlers.not_found_response)
        api.add_exception_handler(LookupError, ExceptionHandlers.not_found_response)
        api.add_exception_handler(HttpError, ExceptionHandlers.http_error_response)
        api.add_exception_handler(Exception, ExceptionHandlers.unexpected_error_response)

    @staticmethod
    def preview_failed_response(request: HttpRequest, error: PreviewFailed) -> HttpResponse:
        return ExceptionHandlers.response(request, {"errors": [item.as_dict() for item in error.errors]}, status=422)

    @staticmethod
    def domain_error_response(request: HttpRequest, error: DomainError) -> HttpResponse:
        return ExceptionHandlers.response(request, {"detail": str(error)}, status=422)

    @staticmethod
    def validation_error_response(request: HttpRequest, error: Exception) -> HttpResponse:
        return ExceptionHandlers.generic_error_response(request, error, status=422)

    @staticmethod
    def not_found_response(request: HttpRequest, error: Exception) -> HttpResponse:
        return ExceptionHandlers.generic_error_response(request, error, status=404)

    @staticmethod
    def http_error_response(request: HttpRequest, error: HttpError) -> HttpResponse:
        if isinstance(error.__cause__, DomainError):
            return ExceptionHandlers.domain_error_response(request, error.__cause__)
        return ExceptionHandlers.generic_error_response(request, error, status=error.status_code)

    @staticmethod
    def unexpected_error_response(request: HttpRequest, error: Exception) -> HttpResponse:
        return ExceptionHandlers.generic_error_response(request, error, status=500)

    @staticmethod
    def generic_error_response(request: HttpRequest, error: Exception, status: int) -> HttpResponse:
        logger.exception(
            "unhandled_api_exception",
            method=request.method,
            path=request.path,
            exception_type=type(error).__name__,
        )
        return ExceptionHandlers.response(request, {"detail": GENERIC_ERROR_MESSAGE}, status=status)

    @staticmethod
    def response(request: HttpRequest, payload: dict[str, Any], status: int) -> HttpResponse:
        from modwire_hex.django import DjangoNinja

        return DjangoNinja.api().create_response(request, payload, status=status)
