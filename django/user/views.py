from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect
from django.contrib import messages

from user.forms import CustomUserCreationForm, CustomUserChangeForm
from user.models import CustomUser
from core.models import Order

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/profile.html')


class OrdersView(LoginRequiredMixin, ListView):
    template_name = 'user/orders.html'
    model = Order
    paginate_by = 5

    def get_queryset(self):
        queryset = Order.objects.filter(user__id=self.request.user.id)
        return queryset


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user/update_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('user:profile')


def change_passoword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('user:profile'))
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'user/change_password.html', {'form': form})