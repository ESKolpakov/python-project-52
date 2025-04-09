from django import forms

from task_manager.labels.models import Label

from .models import Task


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(),
        required=False,
        label="Метки",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
