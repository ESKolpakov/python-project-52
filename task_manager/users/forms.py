from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as DjangoUserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First name"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label=_("Username"),
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label=_("Password"),
        help_text=_("Your password must contain at least 3 characters."),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        help_text=_("Enter the same password as before, for verification."),
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
            raise ValidationError(_("The password must contain at least 3 characters."))
        return password


class UserChangeForm(DjangoUserChangeForm):
    password = None  # Hide the original password field

    password1 = forms.CharField(
        label=_("Password"),
        required=False,
        help_text=_("Your password must contain at least 3 characters."),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        required=False,
        help_text=_("Enter the same password as before, for verification."),
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
                raise ValidationError(_("Passwords do not match."))
            if len(password1) < 3:
                raise ValidationError(
                    _("The password must contain at least 3 characters.")
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
