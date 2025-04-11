from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.tasks.models import Task, Status


class TaskTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author", password="pass"
        )
        self.status = Status.objects.create(name="Open")
        self.client.force_login(self.author)

    def test_create_task(self):
        response = self.client.post(
            reverse("tasks:create"),
            {
                "name": "Fix login bug",
                "description": "Some description",
                "status": self.status.pk,
                "author": self.author.pk,
                "executor": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Fix login bug").exists())
