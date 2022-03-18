from django.urls import path

from . import views

urlpatterns = [
    path('list/<int:team_id>/', views.TasksListView.as_view(), name='tasks'),
    path('<int:id>/', views.TaskView.as_view(), name='task'),
]
