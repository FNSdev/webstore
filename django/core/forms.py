from django import forms
from django.forms import ModelForm

from .models import Product


class SmartphoneFilterForm(forms.Form):
    model = forms.CharField(max_length=40, required=False)
    manufacturer = forms.CharField(max_length=40, required=False)
    release_year = forms.IntegerField(required=False)
    memory = forms.IntegerField(required=False)
    OS = forms.CharField(max_length=40, required=False)
    CPU = forms.CharField(max_length=40, required=False)
    GPU = forms.CharField(max_length=40, required=False)