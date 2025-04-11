from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class StatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin", password="adminpass"
        )
        self.status = Status.objects.create(name="New")

    def test_status_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New")

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("statuses:create"), {"name": "In Progress"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="In Progress").exists())
