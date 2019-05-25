from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import CustomUser
from user.mixins import UserFormMixin


class CustomUserCreationForm(UserFormMixin, UserCreationForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': '13',
            }
        ), label='Phone number: +375 (_ _) (_ _ _ _ _ _ _)'
    )


class CustomUserChangeForm(UserFormMixin, UserChangeForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': '13',
            }
        ), label='Phone number: +375 (_ _) (_ _ _ _ _ _ _)'
    )

    password = None
