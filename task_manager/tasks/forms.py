from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_("Executor"),
        required=False,
        empty_label=_("---------"),
        to_field_name="id",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label_from_instance = (
            lambda obj: f"{obj.first_name} {obj.last_name}"
        )
