from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, render

from .forms import CreationForm

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("signup")
    template_name = "signup.html"
    def get_success_url(self):
        return reverse('home')
