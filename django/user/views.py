from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'