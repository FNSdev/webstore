from django.urls import path
from django.contrib.auth import views as auth_views

from user import views


app_name = 'user'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/update', views.UpdateProfileView.as_view(), name='update-profile'),
    path('password', views.change_passoword_view, name='change-password')
]