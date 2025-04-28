from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = "---------"
        self.fields['executor'].empty_label = "---------"
        self.fields['labels'].required = False

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "executor": forms.Select(attrs={"class": "form-select"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
        help_texts = {
            "labels": "Удерживайте Ctrl для выбора нескольких меток",
        }
