from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<str:category>', ProductsView.as_view(), name='products'),
]