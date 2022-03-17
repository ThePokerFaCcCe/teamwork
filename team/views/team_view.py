from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, FormView

from ..models import Team
from ..querysets import get_user_teams
from ..forms import TeamCreateForm


def team_view(request):

    return render(request, 'team/team.html')


# class TeamListView(ListView):
#     queryset = Team.objects.all()
#     template_name = "team/team.html"


class TeamView(CreateView):
    success_url = '/'
    template_name = "team/team.html"
    form_class = TeamCreateForm

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = get_user_teams(self.request.user.pk)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            post = request.POST.copy()
            post.update({"creator": request.user})
            request.POST = post
        return super().post(request, *args, **kwargs)
