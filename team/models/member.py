from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import task
from .team import Team
User = settings.AUTH_USER_MODEL


class Member(models.Model):
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE,
                             related_name="members")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name="team_members")

    class RankChoices(models.IntegerChoices):
        OWNER = 2, _("Creator")
        MANAGER = 1, _("Manager")
        NORMAL = 0, _("Normal")

    rank = models.IntegerField(_("rank"), choices=RankChoices.choices,
                               default=RankChoices.NORMAL)

    class Meta:
        unique_together = ['user', 'team']

    @property
    def tasks_done(self) -> int:
        """Return the number of tasks that their status is DONE"""
        status = task.models.Task.StatusChoices
        return len([t for t in self.tasks.all()
                    if t.status == status.DONE])

    @property
    def tasks_status(self) -> str:
        """Return a string that says how much tasks of all tasks are DONE"""
        all_tasks = len(self.tasks.all())
        return f"{self.tasks_done}/{all_tasks} DONE"
