from collections.abc import Callable
from typing import Any

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja.errors import HttpError


def validation_error(error: ValidationError | IntegrityError | ValueError) -> HttpError:
    return HttpError(422, str(error))


def validated(call: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return call(*args, **kwargs)
    except (ValidationError, IntegrityError, ValueError) as error:
        raise validation_error(error) from error
