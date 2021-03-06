from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from user.forms import CustomUserCreationForm, CustomUserChangeForm
from user.models import CustomUser
from core.models import Order, ProductInOrder, Review


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'


class ProfileView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def get(self, request, *args, **kwargs):
        return render(request, 'user/profile.html')


class OrdersView(LoginRequiredMixin, ListView):
    template_name = 'user/orders.html'
    model = Order
    paginate_by = 10
    login_url = '/user/login'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class ReviewsView(LoginRequiredMixin, ListView):
    template_name = 'user/reviews.html'
    model = Review
    paginate_by = 5
    login_url = '/user/login'

    def get_queryset(self):
        queryset = Review.objects.filter(user=self.request.user)
        return queryset


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user/update_profile.html'
    login_url = '/user/login'

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


class OrderDetailsView(LoginRequiredMixin, View):
    login_url = '/user/login'

    def get(self, request, *args, **kwargs):
        order_id = kwargs['pk']
  
        order = get_object_or_404(Order, id=order_id)

        if order.user == request.user:
            products = ProductInOrder.objects.filter(order__id=order_id)
            return render(request, 'user/order_details.html', {'order': order, 'products_in_order': products})
        else:
            raise PermissionDenied()