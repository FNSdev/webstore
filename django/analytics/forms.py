from django import forms
from django.forms import ModelForm

from analytics.models import DataSample


class DataSampleForm(ModelForm):
    class Meta:
        model = DataSample
        exclude = tuple()


class PredictForm(ModelForm):
    class Meta:
        model = DataSample
        exclude = ('profit', )
