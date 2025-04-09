from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123456")
        self.status = Status.objects.create(name="In Progress")

    def test_status_list_requires_login(self):
        response = self.client.get(reverse("statuses:status_list"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('statuses:status_list')}"
        )

    def test_status_list_view_authenticated(self):
        self.client.login(username="testuser", password="pass123456")
        response = self.client.get(reverse("statuses:status_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "In Progress")

    def test_status_create(self):
        self.client.login(username="testuser", password="pass123456")
        response = self.client.post(
            reverse("statuses:status_create"), {"name": "New Status"}
        )
        self.assertRedirects(response, reverse("statuses:status_list"))
        self.assertTrue(Status.objects.filter(name="New Status").exists())

    def test_status_update(self):
        self.client.login(username="testuser", password="pass123456")
        response = self.client.post(
            reverse("statuses:status_update", args=[self.status.pk]),
            {"name": "Updated Status"},
        )
        self.assertRedirects(response, reverse("statuses:status_list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

    def test_status_delete(self):
        self.client.login(username="testuser", password="pass123456")
        response = self.client.post(
            reverse("statuses:status_delete", args=[self.status.pk])
        )
        self.assertRedirects(response, reverse("statuses:status_list"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
