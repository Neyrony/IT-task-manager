from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from manager.models import Task


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

