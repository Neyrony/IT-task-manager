import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import TaskType, Position, Task


class ModelTest(TestCase):
    def test_task_type_str(self):
        test_task = TaskType.objects.create(name="test")
        self.assertEqual(str(test_task), test_task.name)

    def test_position_str(self):
        test_position = Position.objects.create(name="test")
        self.assertEqual(str(test_position), test_position.name)

    def test_worker_str(self):
        test_worker = get_user_model().objects.create_user(
            username="test", password="test_password"
        )
        self.assertEqual(str(test_worker), f"{test_worker.username} - No position")
        test_worker.position = Position.objects.create(name="test")
        self.assertEqual(
            str(test_worker), f"{test_worker.username} - {test_worker.position}"
        )

    def test_task_str(self):
        test_task = Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.datetime.now(),
            priority=Task.Priority.HIGH,
            task_type=TaskType.objects.create(name="test"),
        )
        self.assertEqual(
            str(test_task),
            f"{test_task.name} - {test_task.get_priority_display()} (is completed: {test_task.is_completed})",
        )
