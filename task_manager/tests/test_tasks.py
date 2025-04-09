# task_manager/tasks/tests/test_tasks.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskCRUDTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="testpass")
        self.executor = User.objects.create_user(
            username="executor", password="testpass"
        )
        self.other_user = User.objects.create_user(
            username="other", password="testpass"
        )
        self.status = Status.objects.create(name="Open")

        self.task = Task.objects.create(
            name="Initial Task",
            description="Description here",
            status=self.status,
            author=self.author,
            executor=self.executor,
        )

    def test_task_list_view_requires_login(self):
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 302)

    def test_task_create(self):
        self.client.login(username="author", password="testpass")
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "name": "New Task",
                "description": "New task description",
                "status": self.status.id,
                "executor": self.executor.id,
            },
        )
        self.assertRedirects(response, reverse("tasks:task_list"))
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_by_author(self):
        self.client.login(username="author", password="testpass")
        response = self.client.post(
            reverse("tasks:task_update", args=[self.task.pk]),
            {
                "name": "Updated Task",
                "description": "Updated desc",
                "status": self.status.id,
                "executor": self.executor.id,
            },
        )
        self.assertRedirects(response, reverse("tasks:task_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_by_author(self):
        self.client.login(username="author", password="testpass")
        response = self.client.post(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertRedirects(response, reverse("tasks:task_list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author_denied(self):
        self.client.login(username="other", password="testpass")
        response = self.client.post(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_detail_view(self):
        self.client.login(username="author", password="testpass")
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Initial Task")
