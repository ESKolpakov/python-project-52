from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as DjangoUserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Имя пользователя",
        help_text=(
            "Обязательное поле. "
            "Не более 150 символов. "
            "Только буквы, цифры и символы @/./+/-/_."
        ),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        help_text="Ваш пароль должен содержать как минимум 3 символа.",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 3:
            raise ValidationError("Пароль должен содержать минимум 3 символа.")
        return password


class UserChangeForm(DjangoUserChangeForm):
    password = None  # скрываем оригинальное поле пароля

    password1 = forms.CharField(
        label="Пароль",
        required=False,
        help_text="Ваш пароль должен содержать как минимум 3 символа.",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=False,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают.")
            if len(password1) < 3:
                raise ValidationError(
                    "Пароль должен содержать минимум 3 символа."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
