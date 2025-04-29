from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.all()

        status_id = self.request.GET.get("status")
        executor_id = self.request.GET.get("executor")
        label_id = self.request.GET.get("label")
        only_self = self.request.GET.get("only_my_tasks")

        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        if only_self:
            queryset = queryset.filter(author=self.request.user)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()
        context["filter_params"] = self.request.GET
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:tasks_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:tasks_list")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:tasks_list")

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
            return redirect("login")
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks:tasks_list")

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Задача успешно удалена")
        return super().post(request, *args, **kwargs)
