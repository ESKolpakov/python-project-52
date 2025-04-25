from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserForm, UserChangeForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['request'] = self.request
#        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:users_list")
    success_message = "Пользователь успешно изменен"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        print(">>> FLASH MESSAGE SENT <<<")  # Для отладки в CI
        return response

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return redirect("login")
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users:users_list")


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:users_list")

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return redirect("login")
        messages.error(
            self.request, "У вас нет прав для удаления другого пользователя."
        )
        return redirect("users:users_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Пользователь успешно удален")
        return super().post(request, *args, **kwargs)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
