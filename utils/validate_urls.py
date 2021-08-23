from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def is_string_an_url(url_string: str) -> bool:
    validate_url = URLValidator()

    try:
        validate_url(url_string)
    except ValidationError:
        return False

    return True
