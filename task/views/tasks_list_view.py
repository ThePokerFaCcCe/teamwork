from django.views.generic import ListView

from .mixins import TaskRequestObjectsMixin
from ..models import Task


class TasksListView(TaskRequestObjectsMixin, ListView):
    template_name = "task/tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(member=self._member_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_object'] = self._team_object
        context['task_status'] = Task.StatusChoices
        return context
