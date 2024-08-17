from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import tokens
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Send welcome email after user registration
        user_email = form.cleaned_data.get('email')
        print(f"this is the user email {user_email}")
        self.send_welcome_email(user_email)
        return response

    def send_welcome_email(self, user_email):
        print("inside send mail")
        subject = 'Welcome to Our Website'
        message = 'Thank you for registering with us. We are excited to have you!'
        # email_from = settings.DEFAULT_FROM_EMAIL  # or 'no-reply@yourdomain.com'
        email_from = 'testwelcom@elmassalla.com'  # or 'no-reply@yourdomain.com'
        recipient_list = [user_email]
        send_mail(subject, message, email_from, recipient_list)


class CustomLoginView(BaseLoginView):
    def form_valid(self, form):
        # Call the original form_valid method to perform the login
        response = super().form_valid(form)

        # Generate or get the token for the user
        user = form.get_user()
        token, _ = Token.objects.get_or_create(user=user)

        # Set token as a cookie
        response.set_cookie('authToken', token.key)
        print(f"this is the token {token.key}")

        return response
