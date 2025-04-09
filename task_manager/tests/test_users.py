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
        response = self.client.get(reverse("users:users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertContains(response, "jane")

    def test_user_registration(self):
        response = self.client.post(
            reverse("users:user_create"),
            {
                "username": "new_user",
                "password1": "Testpass123",
                "password2": "Testpass123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_user_update_self(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(
            reverse("users:user_update", args=[self.user.pk]),
            {
                "username": "john_updated",
                "password1": "Newpass123",
                "password2": "Newpass123",
            },
        )
        self.assertRedirects(response, reverse("users:users_list"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "john_updated")

    def test_user_update_other_denied(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(
            reverse("users:user_update", args=[self.other_user.pk]),
            {
                "username": "unauthorized_change",
                "password1": "Nope12345",
                "password2": "Nope12345",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_user_delete_self(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(
            reverse("users:user_delete", args=[self.user.pk])
        )
        self.assertRedirects(response, reverse("users:users_list"))
        self.assertFalse(User.objects.filter(username="john").exists())

    def test_user_delete_other_denied(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(
            reverse("users:user_delete", args=[self.other_user.pk])
        )
        self.assertEqual(response.status_code, 403)
