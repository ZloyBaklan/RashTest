from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("signup")
    template_name = "signup.html"
    def get_success_url(self):
        return reverse('home')
