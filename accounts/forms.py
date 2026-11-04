from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class BootstrapFormMixin:
    """Adds Bootstrap 5 classes to every widget so forms render styled."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css}".strip()


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # "role" is deliberately excluded so users cannot self-assign ADMIN.
        fields = ("username", "email", "first_name", "last_name", "course")


class BootstrapAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        # Only safe, user-editable fields: no role, username or permissions.
        fields = ("first_name", "last_name", "email", "course")
