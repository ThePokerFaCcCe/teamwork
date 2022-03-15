import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[A-Za-z]{1,}[_]?[A-Za-z0-9]{1,}$'
    message = _(
        'Invalid username! it must start with English letters '
        'and only can contain English letters, digits and one underscore( _ )'
    )
    flags = re.ASCII
