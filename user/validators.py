import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[A-Za-z]{1,}[_]?[A-Za-z0-9]{1,}$'
    message = _(
        'Must start with English letters. '
        'can contain digits and one "_"'
    )
    flags = re.ASCII
