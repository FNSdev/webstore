from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<str:category>', ProductsView.as_view(), name='products'),
    path('product/<str:slug>', ProductDetailView.as_view(), name='product'),
    path('announcement/<str:slug>', AnnouncementDetailView.as_view(), name='announcement'),
]