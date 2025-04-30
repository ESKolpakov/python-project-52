from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserForm, UserChangeForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("DEBUG: Messages in UserListView:", list(messages.get_messages(self.request)))
        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("User was successfully registered")


class UserUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = User
    form_class = UserChangeForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:users_list")
    success_message = _("User was successfully updated")

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("You are not authenticated! Please log in."))
            return redirect("login")
        messages.error(self.request, _("You don't have permission to edit another user."))
        return redirect("users:users_list")


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:users_list")

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("You are not authenticated! Please log in."))
            return redirect("login")
        messages.error(self.request, _("You don't have permission to delete another user."))
        return redirect("users:users_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, _("User was successfully deleted"))
        return super().post(request, *args, **kwargs)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
