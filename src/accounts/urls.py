from django.urls import path
from .views.login_register import LoginView, LogoutView, RegistrationView
from django.contrib.auth.views import auth_login


urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login_url'),
    path('accounts/register/', RegistrationView.as_view(), name='register_url'),
]