from typing import Optional
from django.urls import reverse
from django.views.generic import CreateView
from django.http import Http404
from django.utils.functional import cached_property

from task.forms import TaskCreateForm

from ..models import Member
from ..querysets import get_user_teams, get_team_with_members
from ..forms import TeamCreateForm, MemberCreateForm


class TeamView(CreateView):
    template_name = "team/team.html"
    form_class = TeamCreateForm

    def get_success_url(self) -> str:
        return reverse("team")

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = get_user_teams(self.request.user.pk)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            post = request.POST.copy()
            post.update({"creator": request.user})
            request.POST = post
        return super().post(request, *args, **kwargs)


class TeamManagementView(CreateView):
    template_name = "team/management.html"

    def get_form_class(self):
        if self.request.method == 'POST':
            if 'add_member' in self.request.POST:
                return MemberCreateForm
        return TaskCreateForm

    def __get_team_id(self) -> int:
        """Return team id that exists in url kwargs"""
        return self.kwargs.get('id', None)

    def __validate_post_team_id(self) -> bool:
        """
        Validate entered team id in form are equal to
        team id in url kwargs
        """
        team_id = self.__get_team_id()
        return self.request.POST.get("team", [None])[0] == str(team_id)

    def get_success_url(self) -> str:
        team = self.__get_team_id()
        if team is None:
            return reverse("team")
        return reverse("team-management", kwargs={"id": team})

    def get_context_data(self, **kwargs):
        """
        Sets `object` context to team object that exists in url.
        if team not found, `Http404` will be raised
        """
        obj = get_team_with_members(
            team_id=self.kwargs.get("id")
        )
        if obj is None:
            raise Http404()
        kwargs['object'] = obj
        return super().get_context_data(**kwargs)

    @cached_property
    def _member_object(self) -> Optional[Member]:
        """Returns member instance of request.user"""
        return Member.objects.filter(
            user=self.request.user,
            team_id=self.__get_team_id()
        ).first()

    def has_permissions(self):
        """
        Checks that user has permission to access to this page or not
        """
        member = self._member_object
        return member and member.rank > Member.RankChoices.NORMAL

    def post(self, request, *args, **kwargs):
        if not self.has_permissions() or not self.__validate_post_team_id():
            raise Http404()

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self._member_object:
            raise Http404()
        if not self.has_permissions():
            pass  # Should be redirected to tasks page
        return super().get(request, *args, **kwargs)
