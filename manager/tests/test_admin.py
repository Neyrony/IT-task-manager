import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position, TaskType, Task


class ClientAuthorization(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test_password",
            first_name="Admin",
            last_name="Test",
            email="admin@test.com",
            position=Position.objects.create(name="test1"),
        )
        self.client.force_login(self.admin)


class TestPositionAdmin(ClientAuthorization):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_position = Position.objects.create(name="test")

    def test_display_position(self):
        url = reverse("admin:manager_position_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.test_position.name)
        self.assertContains(response, "Name")


class TestTaskTypeAdmin(ClientAuthorization):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_task_type = TaskType.objects.create(name="test")

    def test_display_task_type(self):
        url = reverse("admin:manager_tasktype_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.test_task_type.name)


class TestWorkerAdmin(ClientAuthorization):
    def test_display_worker(self):
        url = reverse("admin:manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.admin.position.name)

    def test_add_worker(self):
        url = reverse("admin:manager_worker_add")
        response = self.client.get(url)
        self.assertContains(response, "Position:")

    def test_change_worker(self):
        url = reverse("admin:manager_worker_change", args=[self.admin.id])
        response = self.client.get(url)
        self.assertContains(response, self.admin.position.name)


class TestTaskAdmin(ClientAuthorization):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = Task.objects.create(
            name="test",
            deadline=datetime.datetime.now(),
            is_completed=False,
            priority=1,
            task_type=TaskType.objects.create(name="test"),
        )
        cls.task_info = [
            cls.task.name,
            cls.task.deadline,
            cls.task.is_completed,
            cls.task.priority,
            cls.task.task_type,
        ]
