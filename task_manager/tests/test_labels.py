from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class LabelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.label = Label.objects.create(name="Bug")

    def test_label_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")

    def test_create_label(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("labels:create"), {"name": "Feature"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="Feature").exists())
