from django.urls import path

from . import views

urlpatterns = [
    path('', views.TeamView.as_view(), name='team'),
    path('management/<int:id>/', views.TeamManagementView.as_view(), name='team-management'),
]
