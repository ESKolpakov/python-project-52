from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Если нужно изменить отображение, можно отрегулировать класс UserAdmin.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
