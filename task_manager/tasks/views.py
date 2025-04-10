from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


# Список задач с фильтрацией
class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter


# Создание задачи
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.instance.labels.set(form.cleaned_data["labels"])
        messages.success(self.request, "Задача успешно создана")
        return response


# Обновление задачи
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.labels.set(form.cleaned_data["labels"])
        messages.success(self.request, "Задача успешно обновлена")
        return response

    def test_func(self):
        return True


# Удаление задачи (только автор)
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:task_list")
    raise_exception = True

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, "Задача успешно удалена")
        return super().delete(request, *args, **kwargs)


# Детали задачи
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"
