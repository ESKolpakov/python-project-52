
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.tasks.models import Task, Status
from task_manager.labels.models import Label


class TaskFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.executor = User.objects.create_user(username="exec", password="pass")
        self.status = Status.objects.create(name="New")
        self.label = Label.objects.create(name="Feature")

        self.task = Task.objects.create(
            name="Filter Task",
            status=self.status,
            author=self.user,
            executor=self.executor,
        )
        self.task.labels.add(self.label)

    def test_filter_by_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:tasks_list"), {"status": self.status.pk})
        self.assertContains(response, "Filter Task")

    def test_filter_by_executor(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:tasks_list"), {"executor": self.executor.pk})
        self.assertContains(response, "Filter Task")

    def test_filter_by_label(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:tasks_list"), {"label": self.label.pk})
        self.assertContains(response, "Filter Task")
