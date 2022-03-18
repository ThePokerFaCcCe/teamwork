from typing import Optional
from django.http import Http404
from django.urls import reverse
from django.views.generic import FormView
from django.utils.functional import cached_property
from django.shortcuts import get_object_or_404

from team.models import Member
from .mixins import TaskRequestObjectsMixin
from ..models import Task
from ..forms import NoteCreateForm, TaskUpdateStatusForm
from ..querysets import get_member_task


class TaskView(TaskRequestObjectsMixin, FormView):
    template_name = "task/task.html"

    def get_success_url(self) -> str:
        return reverse("task", kwargs={'id': self._get_task_id()})

    def get_form_class(self):
        if 'write_note' in self.request.POST:
            return NoteCreateForm
        return TaskUpdateStatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_member_task(self._get_task_id())
        context['task_status'] = Task.StatusChoices
        context['team_object'] = self._team_object
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'update_status' in self.request.POST:
            kwargs['instance'] = self._task_object
        return kwargs

    def has_permissions(self):
        member = self._member_object
        task = self._task_object
        return (task.member_id == member.pk
                or member.rank > member.RankChoices.NORMAL)

    @cached_property
    def _member_object(self) -> Optional[Member]:
        """
        Returns member instance of request.user and team_id kwarg
        raise `Http404` if member instance not found
        """
        return get_object_or_404(
            Member.objects.select_related("team"),
            user=self.request.user,
            team_id=self._task_object.team_id,
        )

    @cached_property
    def _task_object(self) -> Optional[Task]:
        """Return task object of task id in url kwargs"""
        return get_object_or_404(Task, pk=self._get_task_id())

    def get(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if 'write_note' in self.request.POST:
            obj = form.save(commit=False)
            obj.task_id = self._get_task_id()
            obj.member = self._member_object
            obj.save()
        else:
            print(self._get_task_id())
            form.save()
        return super().form_valid(form)
