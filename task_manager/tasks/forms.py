from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"id": "id_name"}),
            "description": forms.Textarea(attrs={"id": "id_description"}),
            "status": forms.Select(attrs={"id": "id_status"}),
            "executor": forms.Select(attrs={"id": "id_executor"}),
            "labels": forms.SelectMultiple(attrs={"id": "id_labels"}),
        }
