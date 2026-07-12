from django.urls import path

from manager.views import (
    TaskListView,
    main_page,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
)

urlpatterns = [
    path("", main_page, name="index"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
]

app_name = "manager"
