from django import forms
from django.forms import ModelForm

#from .models import Product
from core.models import Review, Product, Category
from user.models import CustomUser
import ast

class FormGenerator():
    @staticmethod
    def generate(slug, specifications):
        params = {}
     
        for key, value in specifications.items():
            if value == 'str':
                params[key] = forms.CharField(max_length=40, required=False)
            elif value == 'int':
                params[key] = forms.IntegerField(required=False)
            else:
                raise ValueError(f'Field type {value} is not supported')

        name = slug + '_form'
        form = type(name, (forms.Form,), params)
        return form



GENERATED_FORMS = {}


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'header', 'body', 'user', 'product')

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=CustomUser.objects.all(),
        disabled=True,
    )

    product = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Product.objects.all(),
        disabled=True,
    )

    rating = forms.ChoiceField(
        label='Please, rate this product',
        widget=forms.Select,
        choices=Review.RATINGS,
    )