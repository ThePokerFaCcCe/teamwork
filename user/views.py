from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.generic import FormView

from .models import User
from user.forms import UserSignupForm, UserLoginForm


class AuthView(FormView):
    template_name = 'user/auth.html'

    def get_success_url(self) -> str:
        return reverse("team")

    def get_form_class(self):
        if 'login' in self.request.POST:
            return UserLoginForm
        return UserSignupForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if 'login' in self.request.POST:
            print(username, password, sep='\n--\n')
            user = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if not user:
                form.errors['password'] = ["password doesn't match"]
                return self.form_invalid(form)
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            if not user:
                return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)
