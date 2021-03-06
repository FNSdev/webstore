from django.urls import path

from core.views import *


app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('add-to-basket/', AddToBasketView.as_view(), name='add-to-basket'),
    path('remove-from-basket/', RemoveFromBasketView.as_view(), name='remove-from-basket'),
    path('update-basket/', UpdateBasketView.as_view(), name='update-basket'),
    path('confirm-order/', ConfirmOrderView.as_view(), name='confirm-order'),
    path('make-order/', MakeOrderView.as_view(), name='make-order'),
    path('search/', SearchView.as_view(), name='search'),
    path('products/<str:category>/', ProductsView.as_view(), name='products'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product'),
    path('product/<str:slug>/review/', CreateReviewView.as_view(), name='create-review'),
    path('product/<str:slug>/review/<int:pk>', UpdateReviewView.as_view(), name='update-review'),
    path('announcement/<str:slug>/', AnnouncementDetailView.as_view(), name='announcement'),    
    path('orders', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', UpdateOrderView.as_view(), name='update-order'),
]
