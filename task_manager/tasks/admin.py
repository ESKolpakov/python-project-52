from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "executor", "status")
    list_filter = ("status", "author", "executor")
    search_fields = ("name", "description")
