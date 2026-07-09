from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja.errors import HttpError


def validation_error(error: ValidationError | IntegrityError) -> HttpError:
    return HttpError(422, str(error))
