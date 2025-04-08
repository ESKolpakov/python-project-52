from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users_list')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users_list')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk
