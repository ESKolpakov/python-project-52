import json
from pathlib import Path
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()
BASE_FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures"


class FixtureClientTests(TestCase):
    def setUp(self):
        self.client = self.client

        # Регистрация пользователей
        with open(BASE_FIXTURE_PATH / "users.json") as f:
            users = json.load(f)
            for user in users:
                self.client.post(reverse("users:users_create"), data=user)

        # Логин первым пользователем (Elbert Abshire)
        self.client.post(
            reverse("login"),
            {"username": "elbert-abshire", "password": "HQN7mD9mbM"},
        )

        # Загрузка статусов
        with open(BASE_FIXTURE_PATH / "task_statuses.json") as f:
            statuses = json.load(f)
            for status in statuses:
                self.client.post(reverse("statuses:status_create"), data=status)

        # Загрузка меток
        with open(BASE_FIXTURE_PATH / "labels.json") as f:
            labels = json.load(f)
            for label in labels:
                self.client.post(reverse("labels:labels_create"), data=label)

    def assertFlashMessage(self, response, expected_text):
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(expected_text in str(m) for m in messages),
            f"'{expected_text}' not found in flash messages: {messages}",
        )

    def test_create_task_from_test_data(self):
        with open(BASE_FIXTURE_PATH / "test_data.json") as f:
            data = json.load(f)
            task = data["tasks"]["first"]

            from task_manager.statuses.models import Status

            status = Status.objects.get(name=task["status"])

            executor = User.objects.get(
                first_name=task["executor"].split()[0],
                last_name=task["executor"].split()[1],
            )

            from task_manager.labels.models import Label

            label_ids = [
                Label.objects.get(name=name).id
                for name in task.get("labels", {}).values()
            ]

            response = self.client.post(
                reverse("tasks:tasks_create"),
                data={
                    "name": task["name"],
                    "description": task["description"],
                    "status": status.id,
                    "executor": executor.id,
                    "labels": label_ids,
                },
                follow=True,
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Задача успешно создана")
            self.assertFlashMessage(response, "Задача успешно создана")

    def test_update_label(self):
        from task_manager.labels.models import Label

        label = Label.objects.get(name="second label name")
        response = self.client.post(
            reverse("labels:labels_update", args=[label.id]),
            {"name": "Обновлённая метка"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Метка успешно обновлена")
        self.assertFlashMessage(response, "Метка успешно обновлена")

    def test_delete_status(self):
        from task_manager.statuses.models import Status

        status = Status.objects.get(name="third status name")
        response = self.client.post(
            reverse("statuses:status_delete", args=[status.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Статус успешно удалён")
        self.assertFlashMessage(response, "Статус успешно удалён")
