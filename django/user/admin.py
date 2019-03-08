from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'first_name', 'last_name', 'city', 'address', 'phone_number', 'basket'),
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'city', 'address', 'phone_number', 'basket']

admin.site.register(CustomUser, CustomUserAdmin)

