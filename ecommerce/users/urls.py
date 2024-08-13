from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'users'  # Add this line to namespace your URLs

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.RegisterView.as_view(template_name='users/register.html'), name='register'),
]
