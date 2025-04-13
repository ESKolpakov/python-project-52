"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# task_manager/urls.py
from django.contrib import admin
from django.urls import include, path

from task_manager.users.views import CustomLogoutView
from task_manager.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/logout/", CustomLogoutView.as_view(), name="logout"),
    path("auth/", include("django.contrib.auth.urls")),
    path("", index, name="index"),
    path(
        "users/",
        include(("task_manager.users.urls", "users"), namespace="users"),
    ),
    path(
        "tasks/",
        include(("task_manager.tasks.urls", "tasks"), namespace="tasks"),
    ),
    path(
        "statuses/",
        include(
            ("task_manager.statuses.urls", "statuses"), namespace="statuses"
        ),
    ),
    path(
        "labels/",
        include(("task_manager.labels.urls", "labels"), namespace="labels"),
    ),
]
