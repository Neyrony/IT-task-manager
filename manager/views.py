from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from manager.models import Task


@require_GET
def main_page(request: HttpRequest) -> HttpResponse:
    visits_amount = request.session.get("visits_amount", 0) + 1
    request.session["visits_amount"] = visits_amount
    context = {"visits_amount": visits_amount}
    return render(request, "manager/index.html", context=context)


class TaskListView(ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.select_related("task_type")


class TaskDetailView(DetailView):
    model = Task

    def get_queryset(self):
        return Task.objects.select_related("task_type").prefetch_related("assignees")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_assignees"] = Task.objects.get(pk=self.kwargs["pk"]).assignees.all()
        return context

class TaskCreateView(CreateView):
    model = Task
    fields = "__all__"


class TaskUpdateView(UpdateView):
    model = Task
    fields = "__all__"


class TaskDeleteView(DeleteView):
    model = Task

