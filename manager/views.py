from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_GET
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from manager.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskForm,
)
from manager.models import Task, Worker, TaskType, Position


@require_GET
def main_page(request: HttpRequest) -> HttpResponse:
    visits_amount = request.session.get("visits_amount", 0) + 1
    request.session["visits_amount"] = visits_amount
    amount_of_workers = get_user_model().objects.all().count()
    amount_of_tasks = Task.objects.all().count()
    amount_of_task_types = TaskType.objects.all().count()
    amount_of_positions = Position.objects.all().count()

    context = {
        "visits_amount": visits_amount,
        "amount_of_workers": amount_of_workers,
        "amount_of_tasks": amount_of_tasks,
        "amount_of_task_types": amount_of_task_types,
        "amount_of_positions": amount_of_positions,
    }
    return render(request, "manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 9

    def get_queryset(self):
        return Task.objects.select_related("task_type")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task

    def get_queryset(self):
        return Task.objects.select_related("task_type").prefetch_related("assignees")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_assignees"] = Task.objects.get(
            pk=self.kwargs["pk"]
        ).assignees.all()
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task_list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse("manager:task_detail", kwargs={"pk": self.kwargs["pk"]})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task_list")


class WorkerListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    paginate_by = 9

    def get_queryset(self):
        return Worker.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()

    def get_queryset(self):
        return Worker.objects.select_related("position")


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker_list")


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse("manager:worker_detail", kwargs={"pk": self.kwargs["pk"]})


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("manager:worker_list")


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 9


class TaskTypeDetailView(LoginRequiredMixin, DetailView):
    model = TaskType
    template_name = "manager/task_type_detail.html"
    context_object_name = "task_type"


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = ("name",)
    context_object_name = "task_type"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task_type_list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = ("name",)
    context_object_name = "task_type"
    template_name = "manager/task_type_form.html"

    def get_success_url(self):
        return reverse("manager:task_type_detail", kwargs={"pk": self.kwargs["pk"]})


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("manager:task_type_list")


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    paginate_by = 9


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = ("name",)
    success_url = reverse_lazy("manager:position_list")


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = ("name",)

    def get_success_url(self):
        return reverse("manager:position_detail", kwargs={"pk": self.kwargs["pk"]})


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position_list")
