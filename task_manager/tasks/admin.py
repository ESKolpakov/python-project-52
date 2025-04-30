from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "executor", "status")
    list_filter = (
        ("status", admin.FieldListFilter),
        ("author", admin.FieldListFilter),
        ("executor", admin.FieldListFilter),
    )
    search_fields = ("name", "description")
