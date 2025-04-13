from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="password123"
        )
        self.other_user = User.objects.create_user(
            username="jane", password="password456"
        )

    def test_users_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("users:users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertContains(response, "jane")

    def test_user_registration(self):
        response = self.client.post(
            reverse("users:users_create"),
            {
                "username": "new_user",
                "password1": "Testpass123",
                "password2": "Testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="new_user").exists())
