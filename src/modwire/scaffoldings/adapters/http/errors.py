from collections.abc import Callable
from typing import Any

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja.errors import HttpError


class Validation:
    @staticmethod
    def validation_error(error: ValidationError | IntegrityError | ValueError) -> HttpError:
        return HttpError(422, str(error))

    def validated(self, call: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            return call(*args, **kwargs)
        except (ValidationError, IntegrityError, ValueError) as error:
            raise self.validation_error(error) from error


validation = Validation()
validation_error = validation.validation_error
validated = validation.validated
