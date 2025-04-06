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
from django.urls import path
from task_manager.views import (
    index,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='users_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path(
        'users/<int:pk>/update/',
        UserUpdateView.as_view(),
        name='user_update'
        ),
    path(
        'users/<int:pk>/delete/',
        UserDeleteView.as_view(),
        name='user_delete'
        ),
    path(
        'login/',
        LoginView.as_view(template_name='login.html'),
        name='login'
        ),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
