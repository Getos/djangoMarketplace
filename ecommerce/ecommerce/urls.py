"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name="home"),
    path('api/', include('api.urls')),
    path('api/products/', include('products.urls')),
    path('users/', include('users.urls')),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/", views.add_to_cart, name="add"),
    path("confirm_payment/<str:pk>", views.confirm_payment),
    path('delete_cart_item/<int:pk>/',
         views.delete_cart_item, name='delete_cart_item'),
    path('product-portal/', views.product_portal, name='product-portal'),
    path('forbidden/', views.forbidden, name='forbidden'),
]
