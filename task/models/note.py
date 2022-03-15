from django.db import models
from django.utils.translation import gettext_lazy as _

from team.models import Member
from .task import Task


class Note(models.Model):
    text = models.TextField(_("text"), max_length=255)

    member = models.ForeignKey(to=Member, on_delete=models.CASCADE,
                               related_name="sent_notes")
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE,
                             related_name="notes")

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
