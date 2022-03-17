from django.urls import reverse
from django.views.generic import CreateView

from ..querysets import get_user_teams
from ..forms import TeamCreateForm


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
