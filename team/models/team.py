from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Team(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), max_length=150, null=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                related_name="owned_teams")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
