from django import forms
from django.forms import ModelForm
from django.forms.forms import DeclarativeFieldsMetaclass

import ast
from core.models import Review, Product, Category, Order
from user.models import CustomUser


GENERATED_FORMS = {}


class MetaForm(DeclarativeFieldsMetaclass):
    def __new__(cls, clsname, bases, dct):
        params = {}
        for key, value in dct.items():
            if value == 'str':
                params[key] = forms.CharField(max_length=40, required=False)
            elif value == 'int':
                params[key] = forms.IntegerField(required=False)
            else:
                raise ValueError(f'Field type {value} is not supported') 

        return super().__new__(cls, clsname, bases, params)


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


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('status', )
