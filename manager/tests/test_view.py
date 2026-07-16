from django.test import TestCase
from django.urls import reverse


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
