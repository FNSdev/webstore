from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': '9',
            }
        ), label='Phone number: +375 (_ _) (_ _ _ _ _ _ _)'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'city', 'address', 'phone_number')

    def clean_phone_number(self):
        correct_codes = ('33', '44', '29', '24', '25')
        data = self.cleaned_data['phone_number']
        code = data[:2]
        if not data.isnumeric() or len(data) != 9 or code not in correct_codes:
            raise forms.ValidationError('Please, provide a correct phone number')
        data = '+375' + data
        return data


class CustomUserChangeForm(UserChangeForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': '9',
            }
        ), label='Phone number: +375 (_ _) (_ _ _ _ _ _ _)'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'city', 'address', 'phone_number')

    def clean_phone_number(self):
        correct_codes = ('33', '44', '29', '24', '25')
        data = self.cleaned_data['phone_number']
        code = data[:2]
        if not data.isnumeric() or len(data) != 9 or code not in correct_codes:
            raise forms.ValidationError('Please, provide a correct phone number')
        data = '+375' + data
        return data