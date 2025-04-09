# task_manager/tests/test_filters.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilterTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")

        self.status = Status.objects.create(name="In Progress")
        self.label = Label.objects.create(name="Bug")

        self.task1 = Task.objects.create(
            name="Task One",
            status=self.status,
            author=self.user1,
            executor=self.user2,
        )
        self.task1.labels.set([self.label])

        self.task2 = Task.objects.create(
            name="Task Two",
            status=self.status,
            author=self.user2,
            executor=self.user1,
        )

        self.client.login(username="user1", password="pass1")

    def test_filter_by_status(self):
        response = self.client.get(
            reverse("tasks:task_list"), {"status": self.status.pk}
        )
        self.assertContains(response, "Task One")
        self.assertContains(response, "Task Two")

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse("tasks:task_list"), {"executor": self.user2.pk}
        )
        self.assertContains(response, "Task One")
        self.assertNotContains(response, "Task Two")

    def test_filter_by_label(self):
        response = self.client.get(reverse("tasks:task_list"), {"label": self.label.pk})
        self.assertContains(response, "Task One")
        self.assertNotContains(response, "Task Two")

    def test_filter_by_own_tasks_only(self):
        response = self.client.get(reverse("tasks:task_list"), {"self_tasks": "on"})
        self.assertContains(response, "Task One")
        self.assertNotContains(response, "Task Two")
