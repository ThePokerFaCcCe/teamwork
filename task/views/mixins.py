from typing import Optional
from django.utils.functional import cached_property
from django.shortcuts import get_object_or_404

from team.models import Member, Team
from ..models import Task


class TaskRequestObjectsMixin:
    def _get_team_id(self) -> int:
        """Return team id that exists in url kwargs"""
        return self.kwargs.get('team_id', None)

    def _get_task_id(self) -> int:
        """Return task id that exists in url kwargs"""
        return self.kwargs.get('id', None)

    @cached_property
    def _member_object(self) -> Optional[Member]:
        """
        Returns member instance of request.user and team_id kwarg
        raise `Http404` if member instance not found
        """
        return get_object_or_404(
            Member.objects.select_related("team"),
            user=self.request.user,
            team_id=self._get_team_id(),
        )

    @cached_property
    def _team_object(self) -> Optional[Team]:
        """
        Return team instance from member's team.
        raise `Http404` if member instance not found
        """
        return self._member_object.team
