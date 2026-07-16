from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
    def setUp(self):
        super().setUp()
        test_task_type = TaskType.objects.create(name="test")
        self.task_1 = Task.objects.create(
            name="test1",
            deadline=timezone.now(),
            is_completed=False,
            priority=1,
            task_type=test_task_type,
        )
        self.task_2 = Task.objects.create(
            name="test2",
            deadline=timezone.now(),
            is_completed=False,
            priority=1,
            task_type=test_task_type,
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("manager:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(Task.objects.all()))
        self.assertTemplateUsed(response, "manager/task_list.html")

    def test_task_detail_view(self):
        response = self.client.get(reverse("manager:task_detail", args=[self.task_1.pk]))

        self.assertContains(response, self.task_1.name)
        self.assertContains(response, self.task_1.get_priority_display())
        self.assertContains(response, self.task_1.deadline.strftime("%B %d, %Y"))
        self.assertContains(response, self.task_1.description)
        self.assertTemplateUsed(response, "manager/task_detail.html")


class WorkerViewTest(ClientAuthorization):
    def setUp(self):
        super().setUp()
        position = Position.objects.create(name="test1")
        self.worker_1 = get_user_model().objects.create_user(username="test1", password="test", first_name="first", last_name="last", email="user1@test.com", position=position)
        self.worker_2 = get_user_model().objects.create_user(username="test2", password="test", first_name="first", last_name="last", email="user2@test.com", position=position)


    def test_worker_list_view(self):
        response = self.client.get(reverse("manager:worker_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]), list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(response, "manager/worker_list.html")

    def test_worker_detail_view(self):
        response = self.client.get(reverse("manager:worker_detail", args=[self.worker_1.pk]))

        self.assertContains(response, self.worker_1.username)
        self.assertContains(response, self.worker_1.first_name + " " + self.worker_1.last_name)
        self.assertContains(response, self.worker_1.email)
        self.assertContains(response, self.worker_1.position.name)
        self.assertTemplateUsed(response, "manager/worker_detail.html")


class TaskTypeViewTest(ClientAuthorization):
    def setUp(self):
        super().setUp()
        self.task_type_1 = TaskType.objects.create(name="test1")
        self.task_type_2 = TaskType.objects.create(name="test2")

    def test_task_type_list_view(self):
        response = self.client.get(reverse("manager:task_type_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]), list(TaskType.objects.all())
        )
        self.assertTemplateUsed(response, "manager/task_type_list.html")

    def test_task_detail_view(self):
        response = self.client.get(reverse("manager:task_type_detail", args=[self.task_type_1.pk]))

        self.assertContains(response, self.task_type_1.name)
        self.assertTemplateUsed(response, "manager/task_type_detail.html")


class PositionViewTest(ClientAuthorization):
    def setUp(self):
        super().setUp()
        self.position_1 = Position.objects.create(name="test1")
        self.position_2 = Position.objects.create(name="test2")

    def test_position_list_view(self):
        response = self.client.get(reverse("manager:position_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]), list(Position.objects.all())
        )
        self.assertTemplateUsed(response, "manager/position_list.html")

    def test_task_detail_view(self):
        response = self.client.get(reverse("manager:position_detail", args=[self.position_1.pk]))

        self.assertContains(response, self.position_1.name)
        self.assertTemplateUsed(response, "manager/position_detail.html")
