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
    WorkerDetailView,
    PositionDetailView,
    TaskTypeDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
)

urlpatterns = [
    path("", main_page, name="index"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker_create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker_update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker_delete"),
    path("task-types/", TaskTypeListView.as_view(), name="task_type_list"),
    path("task-types/<int:pk>/", TaskTypeDetailView.as_view(), name="task_type_detail"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task_type_create"),
    path(
        "task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task_type_update"
    ),
    path(
        "task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task_type_delete"
    ),
    path("positions/", PositionListView.as_view(), name="position_list"),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position_detail"),
]

app_name = "manager"
