from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tasks.models import Status, Task


class TaskTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author", password="pass"
        )
        self.other = User.objects.create_user(username="other", password="pass")
        self.status = Status.objects.create(name="In Progress")
        self.label = Label.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="My Task",
            description="A task",
            status=self.status,
            author=self.author,
            executor=self.other,
        )
        self.task.labels.add(self.label)

    def test_task_list_only_my_tasks(self):
        self.client.force_login(self.author)
        response = self.client.get(
            reverse("tasks:tasks_list"), {"only_my_tasks": "on"}
        )
        self.assertContains(response, "My Task")

        self.client.logout()
        self.client.force_login(self.other)
        response = self.client.get(
            reverse("tasks:tasks_list"), {"only_my_tasks": "on"}
        )
        self.assertNotContains(response, "My Task")

    def test_author_can_delete_task(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse("tasks:tasks_delete", args=[self.task.pk]), follow=True
        )
        self.assertRedirects(response, reverse("tasks:tasks_list"))
        self.assertContains(response, "Задача успешно удалена")

    def test_non_author_cannot_delete_task(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("tasks:tasks_delete", args=[self.task.pk]), follow=True
        )
        self.assertRedirects(response, reverse("tasks:tasks_list"))
        self.assertContains(response, "Задачу может удалить только ее автор")

    def test_any_user_can_update_task(self):
        self.client.force_login(self.other)
        response = self.client.get(
            reverse("tasks:tasks_update", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_task_sets_author(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("tasks:tasks_create"),
            {
                "name": "New Task",
                "description": "desc",
                "status": self.status.id,
                "executor": self.author.id,
            },
            follow=True,
        )
        self.assertContains(response, "Задача успешно создана")
        self.assertEqual(Task.objects.last().author, self.other)
