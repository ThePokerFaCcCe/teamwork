from django.urls import reverse
from django.shortcuts import redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('team')
    return redirect("auth")
