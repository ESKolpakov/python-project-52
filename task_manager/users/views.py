from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return super().form_valid(form)


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")

    def test_func(self):
        # Разрешено редактировать только профиль самого пользователя.
        return self.request.user == self.get_object()

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно обновлён")
        return super().form_valid(form)


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    def test_func(self):
        # Разрешено удалять только профиль самого пользователя.
        return self.request.user == self.get_object()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Пользователь успешно удалён")
        return super().delete(request, *args, **kwargs)
