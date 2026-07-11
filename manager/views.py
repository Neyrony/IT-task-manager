from django.views.generic import ListView

from manager.models import Task


class TaskListView(ListView):
    model = Task
    paginate_by = 10
