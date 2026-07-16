import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import TaskType, Task, Position
from manager.tests.test_base import ClientAuthorization


class AccessViewTest(TestCase):
    def test_login_redirect_no_pk_url(self):
        urls = [
            "task_list",
            "task_create",
            "worker_list",
            "worker_create",
            "task_type_list",
            "task_type_create",
            "position_list",
            "position_create",
        ]

        login_url = reverse("login")

        for path in urls:
            with self.subTest(info=path):
                target_url = reverse("manager:" + path)
                response = self.client.get(target_url)
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, f"{login_url}?next={target_url}")

    def test_login_redirect_pk_url(self):
        urls = [
            "task_detail",
            "task_update",
            "task_delete",
            "task_type_detail",
            "task_type_update",
            "task_status_update",
            "task_type_delete",
            "worker_detail",
            "worker_update",
            "worker_delete",
            "position_detail",
            "position_update",
            "position_delete",
        ]

        login_url = reverse("login")

        for path in urls:
            with self.subTest(info=path):
                target_url = reverse("manager:" + path, args=[1])
                response = self.client.get(target_url)
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, f"{login_url}?next={target_url}")

    def test_index_access(self):
        response = self.client.get(reverse("manager:index"))
        self.assertEqual(response.status_code, 200)


class TaskViewTest(ClientAuthorization):
    def test_task_list_view(self):
        test_task_type = TaskType.objects.create(name="test")
        Task.objects.create(
            name="test1",
            deadline=datetime.datetime.now(),
            is_completed=False,
            priority=1,
            task_type=test_task_type,
        )
        Task.objects.create(
            name="test2",
            deadline=datetime.datetime.now(),
            is_completed=False,
            priority=1,
            task_type=test_task_type,
        )

        response = self.client.get(reverse("manager:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(Task.objects.all()))
        self.assertTemplateUsed(response, "manager/task_list.html")


class WorkerViewTest(ClientAuthorization):
    def test_worker_list_view(self):
        get_user_model().objects.create_user(username="test1", password="test")
        get_user_model().objects.create_user(username="test2", password="test")

        response = self.client.get(reverse("manager:worker_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["worker_list"]), list(get_user_model().objects.all()))
        self.assertTemplateUsed(response, "manager/worker_list.html")


class TaskTypeViewTest(ClientAuthorization):
    def test_task_type_list_view(self):
        TaskType.objects.create(name="test1")
        TaskType.objects.create(name="test2")

        response = self.client.get(reverse("manager:task_type_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_type_list"]), list(TaskType.objects.all()))
        self.assertTemplateUsed(response, "manager/task_type_list.html")


class PositionViewTest(ClientAuthorization):
    def test_position_list_view(self):
        Position.objects.create(name="test1")
        Position.objects.create(name="test2")

        response = self.client.get(reverse("manager:position_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["position_list"]), list(Position.objects.all()))
        self.assertTemplateUsed(response, "manager/position_list.html")
