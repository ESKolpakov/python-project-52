from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:labels_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:labels_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно обновлена")
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:labels_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверка: метка используется в задачах?
        if self.object.tasks.exists():
            messages.error(
                request, "Невозможно удалить метку, потому что она используется"
            )
            return redirect(self.success_url)

        self.object.delete()
        messages.success(request, "Метка успешно удалена")
        return redirect(self.success_url)
