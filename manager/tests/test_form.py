import datetime

from django.test import TestCase
from django.utils import timezone

from manager.forms import TaskCreateForm, TaskUpdateForm
from manager.models import TaskType, Task


class TestUserForm(TestCase):
    def setUp(self):
        super().setUp()
        self.task_type = TaskType.objects.create(name="test")
        self.task = Task.objects.create(
            name="test1",
            description="Some description1",
            deadline=timezone.now(),
            is_completed=False,
            priority=1,
            task_type=self.task_type,
        )
        self.data = {
            "name": "test",
            "description": "Some description",
            "deadline": timezone.now() - datetime.timedelta(days=1),
            "is_completed": False,
            "priority": 1,
            "task_type": self.task_type,
        }

    def test_task_create_form(self):
        form = TaskCreateForm(self.data)
        self.assertFalse(form.is_valid())
        self.data["deadline"] = timezone.now() + datetime.timedelta(days=1)
        form = TaskCreateForm(self.data)
        self.assertTrue(form.is_valid())

    def test_task_update_form(self):
        self.data["deadline"] = self.task.deadline
        form = TaskUpdateForm(self.data, instance=self.task)
        self.assertTrue(form.is_valid())
        self.data["deadline"] = timezone.now() - datetime.timedelta(days=1)
        form = TaskUpdateForm(self.data, instance=self.task)
        self.assertFalse(form.is_valid())
        self.data["deadline"] = timezone.now() + datetime.timedelta(days=1)
        form = TaskUpdateForm(self.data, instance=self.task)
        self.assertTrue(form.is_valid())
