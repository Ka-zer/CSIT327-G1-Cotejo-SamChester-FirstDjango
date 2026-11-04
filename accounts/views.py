from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import (BootstrapAuthenticationForm, CustomUserCreationForm,
                    ProfileUpdateForm)


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    success_message = "Your account was created successfully. You can log in now."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    authentication_form = BootstrapAuthenticationForm


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Your profile was updated successfully."

    def get_object(self, queryset=None):
        # Always the logged-in user; there is no pk in the URL, so one user
        # can never edit another user's profile.
        return self.request.user
