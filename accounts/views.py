<<<<<<< HEAD
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class SignUpView(CreateView) :
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 7282921dbbc84e60689a6e34b99624bc5b84393f
