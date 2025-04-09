# task_manager/tests/test_labels.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class LabelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.client.login(username='tester', password='pass123')
        self.label = Label.objects.create(name='Bug')

    def test_labels_list_view(self):
        response = self.client.get(reverse('labels:label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug')

    def test_label_create(self):
        response = self.client.post(
            reverse('labels:label_create'),
            {'name': 'Feature'}
        )
        self.assertRedirects(response, reverse('labels:label_list'))
        self.assertTrue(Label.objects.filter(name='Feature').exists())

    def test_label_update(self):
        response = self.client.post(
            reverse('labels:label_update', args=[self.label.id]),
            {'name': 'Critical Bug'}
        )
        self.assertRedirects(response, reverse('labels:label_list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Critical Bug')

    def test_label_delete(self):
        response = self.client.post(reverse('labels:label_delete', args=[self.label.id]))
        self.assertRedirects(response, reverse('labels:label_list'))
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_protected_label_delete(self):
        status = Status.objects.create(name='Open')
        task = Task.objects.create(
            name='Fix bug',
            description='Fix this asap',
            status=status,
            author=self.user
        )
        task.labels.add(self.label)

        response = self.client.post(reverse('labels:label_delete', args=[self.label.id]))
        self.assertRedirects(response, reverse('labels:label_list'))
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
