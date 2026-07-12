from django.urls import path

from manager.views import TaskListView, main_page, TaskDetailView, TaskCreateView, TaskDeleteView

urlpatterns = [
    path("", main_page, name="index"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]

app_name = "manager"
