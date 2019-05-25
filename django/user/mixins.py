from django import forms
from django.forms import Form
from user.models import CustomUser


class UserFormMixin:
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'city', 'address', 'phone_number')

    # TODO use regular expressions
    def clean_phone_number(self):
        correct_codes = ('+37533', '+37544', '+37529', '+37524', '+37525')
        data = self.cleaned_data['phone_number']
        code = data[:6]
        if not data[6:].isnumeric() or len(data) != 13 or code not in correct_codes:
            raise forms.ValidationError('Please, provide a correct phone number')
        return data