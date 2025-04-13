import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name="status__id")
    executor = django_filters.NumberFilter(field_name="executor__id")
    label = django_filters.NumberFilter(method="filter_by_label")
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks", label="Только мои задачи"
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def filter_by_label(self, queryset, name, value):
        return queryset.filter(labels__id=value)

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
