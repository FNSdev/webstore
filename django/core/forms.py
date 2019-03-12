from django import forms
from django.forms import ModelForm

from .models import Product


class SmartphoneFilterForm(forms.Form):
    model = forms.CharField(max_length=40, required=False)
    manufacturer = forms.CharField(max_length=40, required=False)
    year = forms.IntegerField(required=False)
    memory = forms.IntegerField(required=False)
    os = forms.CharField(max_length=40, required=False, label='OS')
    cpu = forms.CharField(max_length=40, required=False, label='CPU')
    gpu = forms.CharField(max_length=40, required=False, label='GPU')