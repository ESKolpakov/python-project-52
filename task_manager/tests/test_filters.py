from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.tasks.models import Task, Status


class TaskFilterTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Pending")
        self.user = User.objects.create_user(
            username="executor", password="123"
        )
        self.client.force_login(self.user)
        Task.objects.create(
            name="Filter test", status=self.status, author=self.user
        )

    def test_filter_by_status(self):
        response = self.client.get("/tasks/?status=" + str(self.status.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Filter test")
