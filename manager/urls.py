from django.urls import path

from manager.views import TaskListView, main_page

urlpatterns = [
    path("", main_page, name="index"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
]

app_name = "manager"
