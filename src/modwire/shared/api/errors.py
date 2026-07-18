from collections.abc import Callable
from typing import Any

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja.errors import HttpError


def validation_error(error: ValidationError | IntegrityError) -> HttpError:
    return HttpError(400, str(error))


def validated(call: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return call(*args, **kwargs)
    except (ValidationError, IntegrityError) as error:
        raise validation_error(error) from error
