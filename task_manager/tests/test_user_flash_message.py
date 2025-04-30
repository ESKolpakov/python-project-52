from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class UserFlashMessageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Имя",
            last_name="Фамилия",
        )
        self.client.login(username="testuser", password="testpass123")

    def test_flash_message_on_update(self):
        url = reverse("users:users_update", args=[self.user.id])
        data = {
            "username": "testuser",
            "first_name": "НовоеИмя",
            "last_name": "НоваяФамилия",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message_texts = [str(m) for m in messages]

        self.assertIn("Пользователь успешно изменен", message_texts)
