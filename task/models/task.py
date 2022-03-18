from django.db import models
from django.utils.translation import gettext_lazy as _

from team.models import Member, Team


class Task(models.Model):
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), max_length=255,
                                   null=True, blank=True)

    class StatusChoices(models.TextChoices):
        DONE = "D", _("done")
        ON_PROGRESS = "P", _("on progress")
        SENT = "S", _("sent")
    status = models.CharField(_("status"), max_length=1,
                              choices=StatusChoices.choices,
                              default=StatusChoices.SENT)
    deadline = models.DateField(_("Deadline"))

    member = models.ForeignKey(to=Member, on_delete=models.CASCADE,
                               related_name="tasks")

    team = models.ForeignKey(to=Team, on_delete=models.CASCADE,
                             related_name="tasks")

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ['-created_at']
