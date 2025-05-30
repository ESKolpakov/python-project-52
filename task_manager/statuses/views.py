from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:statuses_list")

    def form_valid(self, form):
        messages.success(self.request, _("Status was successfully created"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:statuses_list")

    def form_valid(self, form):
        messages.success(self.request, _("Status was successfully updated"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:statuses_list")
    context_object_name = "status"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            messages.error(
                request,
                _("Cannot delete the status because it is in use"),
            )
            return redirect(self.success_url)

        messages.success(request, _("Status was successfully deleted"))
        return super().post(request, *args, **kwargs)
