from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from manager.models import Position


class ClientAuthorization(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test_password",
            first_name="Admin",
            last_name="Test",
            email="admin@test.com",
            position=Position.objects.create(name="test"),
        )
        self.client.force_login(self.admin)
