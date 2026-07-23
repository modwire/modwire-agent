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


def configure_exception_handlers(api: Any) -> None:
    api.add_exception_handler(PreviewFailed, preview_failed_response)
    api.add_exception_handler(DomainError, domain_error_response)
    api.add_exception_handler(NinjaValidationError, validation_error_response)
    api.add_exception_handler(DjangoValidationError, validation_error_response)
    api.add_exception_handler(Http404, not_found_response)
    api.add_exception_handler(LookupError, not_found_response)
    api.add_exception_handler(HttpError, http_error_response)
    api.add_exception_handler(Exception, unexpected_error_response)


def preview_failed_response(request: HttpRequest, error: PreviewFailed) -> HttpResponse:
    return response(request, {"errors": [item.as_dict() for item in error.errors]}, status=422)


def domain_error_response(request: HttpRequest, error: DomainError) -> HttpResponse:
    return response(request, {"detail": str(error)}, status=422)


def validation_error_response(request: HttpRequest, error: Exception) -> HttpResponse:
    return generic_error_response(request, error, status=422)


def not_found_response(request: HttpRequest, error: Exception) -> HttpResponse:
    return generic_error_response(request, error, status=404)


def http_error_response(request: HttpRequest, error: HttpError) -> HttpResponse:
    if isinstance(error.__cause__, DomainError):
        return domain_error_response(request, error.__cause__)
    return generic_error_response(request, error, status=error.status_code)


def unexpected_error_response(request: HttpRequest, error: Exception) -> HttpResponse:
    return generic_error_response(request, error, status=500)


def generic_error_response(request: HttpRequest, error: Exception, status: int) -> HttpResponse:
    logger.exception(
        "unhandled_api_exception",
        method=request.method,
        path=request.path,
        exception_type=type(error).__name__,
    )
    return response(request, {"detail": GENERIC_ERROR_MESSAGE}, status=status)


def response(request: HttpRequest, payload: dict[str, Any], status: int) -> HttpResponse:
    from modwire_hex.django import DjangoNinja

    return DjangoNinja.api().create_response(request, payload, status=status)
