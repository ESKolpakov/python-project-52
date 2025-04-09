# task_manager/tasks/filters.py
import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус",
        empty_label="Любой",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
        empty_label="Любой",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label="Метка",
        empty_label="Любая",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_by_author",
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def filter_by_author(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
