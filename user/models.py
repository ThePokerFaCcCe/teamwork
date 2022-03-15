from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import UsernameValidator


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=36,
        unique=True,
        help_text=_(
            "Required. 36 characters or fewer. "
            "English Letters, digits and one underscore _ only."
        ),
        validators=[UsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        db_index=True,
    )
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
