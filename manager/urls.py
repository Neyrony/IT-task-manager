from django.urls import path

from manager.views import (
    TaskListView,
    main_page,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    WorkerListView,
    PositionListView,
    TaskTypeListView,
)

urlpatterns = [
    path("", main_page, name="index"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path("positions/", PositionListView.as_view(), name="position_list"),
    path("task-types/", TaskTypeListView.as_view(), name="task_type_list"),
]

app_name = "manager"
